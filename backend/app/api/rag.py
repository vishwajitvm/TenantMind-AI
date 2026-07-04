from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.database import get_db, get_tenant_slug, get_qdrant_client
from app.gateways.model_gateway import ModelGateway
from app.gateways.embedding_gateway import EmbeddingGateway
from tracenest import logger
import time

router = APIRouter(prefix="/rag", tags=["RAG"])

class RAGQueryRequest(BaseModel):
    query: str
    limit: Optional[int] = 3

@router.post("/query")
async def rag_query(payload: RAGQueryRequest):
    """Stateless RAG query execution yielding grounding sources and confidence estimation."""
    slug = get_tenant_slug()
    
    if not payload.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty"
        )
        
    # 1. Retrieve embeddings
    try:
        model_name = "all-MiniLM-L6-v2"
        vector = EmbeddingGateway.get_embedding(payload.query, model_name)
        collection_name = f"org_{slug.replace('-', '_')}_vectors"
        
        qdrant_client = get_qdrant_client()
        hits = qdrant_client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=payload.limit
        )
    except Exception as e:
        logger.warning(f"RAG search failed: {str(e)}")
        hits = []
        
    context_chunks = []
    sources = []
    confidence_score = 0.0
    
    if hits:
        scores = []
        for hit in hits:
            chunk_text = hit.payload.get("content", "")
            filename = hit.payload.get("filename", "unknown")
            doc_id = hit.payload.get("document_id", "")
            scores.append(hit.score)
            context_chunks.append(f"[Source: {filename}]\n{chunk_text}")
            sources.append({
                "document_id": doc_id,
                "filename": filename,
                "score": hit.score,
                "snippet": chunk_text[:200]
            })
        
        # Estimate overall confidence score
        confidence_score = sum(scores) / len(scores)
        rag_context = "\n\n".join(context_chunks)
    else:
        rag_context = ""
        
    # 2. Build prompt and execute multi-model gateway call
    messages = [
        {"role": "system", "content": "You are a secure, helpful AI command assistant. Answer the user query using the provided context. If you cannot find the answer, state that no reliable internal source was found. Do not hallucinate."},
        {"role": "user", "content": f"Context:\n{rag_context}\n\nQuestion: {payload.query}"}
    ]
    
    start_time = time.time()
    try:
        llm_response = await ModelGateway.generate(messages, tenant_id=slug)
        latency = time.time() - start_time
    except Exception as e:
        logger.error(f"RAG LLM call failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate response from LLM gateway."
        )
        
    warnings = []
    if not hits:
        warnings.append("No reliable internal source was found.")
        
    return {
        "answer": llm_response["content"],
        "sources": sources,
        "confidence_score": confidence_score,
        "model_used": llm_response["model"],
        "fallback_chain": llm_response.get("fallback_chain", []),
        "retrieved_chunks": [hit.payload for hit in hits] if hits else [],
        "warnings": warnings,
        "latency": latency
    }
