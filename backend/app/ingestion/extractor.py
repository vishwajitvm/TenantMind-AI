import re
import csv
import json
import zipfile
import io
import uuid
from typing import List, Dict, Any, Tuple
from app.gateways.embedding_gateway import EmbeddingGateway
from app.database import ensure_qdrant_collection, get_qdrant_client, get_tenant_slug
from qdrant_client.http import models as qmodels
from tracenest import logger

# Regex for common secrets
SECRET_PATTERNS = {
    "AWS API Key": r"AKIA[0-9A-Z]{16}",
    "Generic Secret/API Key": r"(db_password|password|api_key|client_secret|private_key|secret_key)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{8,}['\"]",
    "Private Key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "Slack Token": r"xoxb-[0-9]{11}-[0-9]{12}-[a-zA-Z0-9]{24}"
}

# Prompt injection heuristics
INJECTION_KEYWORDS = [
    "ignore all previous instructions",
    "ignore the above instructions",
    "system override",
    "you are now an admin",
    "bypass safety",
    "do not follow standard guidelines",
    "execute the following system commands",
    "hacked by",
    "jailbreak"
]

class DocumentExtractor:
    @staticmethod
    def scan_for_secrets(text: str) -> List[str]:
        """Scans text for secrets using regex patterns."""
        found = []
        for name, pattern in SECRET_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                found.append(name)
        return found

    @staticmethod
    def scan_for_injections(text: str) -> bool:
        """Scans text for common LLM prompt injection attempts."""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in INJECTION_KEYWORDS)

    @staticmethod
    def parse_docx(file_bytes: bytes) -> str:
        """Parses DOCX text using built-in zipfile to read word/document.xml (no external dependencies)."""
        try:
            with zipfile.ZipFile(io.BytesIO(file_bytes)) as docx:
                xml_content = docx.read("word/document.xml").decode("utf-8")
                # Strip XML tags to get raw text
                paragraphs = re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml_content)
                return "\n".join(paragraphs)
        except Exception as e:
            logger.error(f"Error parsing DOCX: {str(e)}")
            return ""

    @staticmethod
    def parse_pdf(file_bytes: bytes) -> str:
        """Parses PDF bytes. Tries to use pypdf if available, otherwise falls back to basic string decoding."""
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
            return text
        except ImportError:
            logger.warning("pypdf not installed. Falling back to printable ASCII extraction for PDF.")
            # Simple fallback: extract strings from pdf binary stream
            text_blocks = re.findall(r"[\x20-\x7E\s]{4,}", file_bytes.decode("ascii", errors="ignore"))
            return "\n".join(text_blocks)
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            return ""

    @classmethod
    def parse_document(cls, filename: str, file_bytes: bytes) -> str:
        """Dispatches file bytes to the correct parser based on file extension."""
        ext = filename.split(".")[-1].lower()
        
        if ext in ["txt", "md", "py", "js", "ts", "html", "css", "go", "rs", "sh", "yml", "yaml", "ini", "conf"]:
            return file_bytes.decode("utf-8", errors="ignore")
            
        elif ext == "csv":
            try:
                reader = csv.reader(io.StringIO(file_bytes.decode("utf-8", errors="ignore")))
                rows = [", ".join(row) for row in reader]
                return "\n".join(rows)
            except Exception as e:
                logger.error(f"Error parsing CSV: {str(e)}")
                return ""
                
        elif ext == "json":
            try:
                data = json.loads(file_bytes.decode("utf-8", errors="ignore"))
                return json.dumps(data, indent=2)
            except Exception as e:
                logger.error(f"Error parsing JSON: {str(e)}")
                return ""
                
        elif ext == "docx":
            return cls.parse_docx(file_bytes)
            
        elif ext == "pdf":
            return cls.parse_pdf(file_bytes)
            
        else:
            # Fallback
            return file_bytes.decode("utf-8", errors="ignore")

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """Chunks text using a sliding window method."""
        chunks = []
        start = 0
        text_len = len(text)
        
        if text_len <= chunk_size:
            return [text] if text.strip() else []
            
        while start < text_len:
            end = start + chunk_size
            chunk = text[start:end]
            if chunk.strip():
                chunks.append(chunk)
            start += chunk_size - overlap
            
        return chunks

    @classmethod
    async def extract_and_index(
        cls, 
        filename: str, 
        file_bytes: bytes, 
        model_name: str = "all-MiniLM-L6-v2"
    ) -> Dict[str, Any]:
        """Extracts text, chunks, checks for security risks, embeds, and indexes to Qdrant."""
        tenant_id = get_tenant_slug()
        
        # 1. Parse text
        text = cls.parse_document(filename, file_bytes)
        if not text.strip():
            logger.warn(f"Document {filename} was parsed but returned no text.")
            return {
                "status": "failed",
                "reason": "empty_document",
                "chunks_count": 0
            }
            
        # 2. Security Scans
        secrets_found = cls.scan_for_secrets(text)
        has_injection = cls.scan_for_injections(text)
        
        if secrets_found:
            logger.warn(f"Security Alert: Secrets found in uploaded document {filename}: {secrets_found}")
        if has_injection:
            logger.warn(f"Security Alert: Potential prompt injection detected in {filename}")

        # 3. Chunk text
        chunks = cls.chunk_text(text)
        
        # 4. Generate Embeddings & Index
        dimension = EmbeddingGateway.get_dimension(model_name)
        collection_name = ensure_qdrant_collection(vector_size=dimension)
        
        qdrant_client = get_qdrant_client()
        points = []
        
        for idx, chunk in enumerate(chunks):
            vector = EmbeddingGateway.get_embedding(chunk, model_name)
            point_id = str(uuid.uuid4())
            
            payload = {
                "filename": filename,
                "tenant_id": tenant_id,
                "chunk_index": idx,
                "content": chunk,
                "secrets_detected": secrets_found,
                "injection_detected": has_injection,
                "model_name": model_name
            }
            
            points.append(
                qmodels.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            )
            
        # Upsert in Qdrant in batches
        if points:
            qdrant_client.upsert(
                collection_name=collection_name,
                points=points
            )
            logger.info(f"Indexed {len(points)} chunks for document '{filename}' in collection '{collection_name}'")
            
        return {
            "status": "success",
            "chunks_count": len(chunks),
            "secrets_detected": secrets_found,
            "injection_detected": has_injection,
            "collection_name": collection_name
        }
