import numpy as np
import hashlib
from typing import List, Union
from tracenest import logger

# Lazy loader/cache for local SentenceTransformer model
_transformer_model = None

class EmbeddingGateway:
    @staticmethod
    def get_dimension(model_name: str) -> int:
        """Returns the vector dimensions for standard models."""
        model_lower = model_name.lower()
        if "minilm" in model_lower:
            return 384
        elif "ada" in model_lower or "text-embedding-3-small" in model_lower or "gemini" in model_lower:
            return 1536
        elif "text-embedding-3-large" in model_lower:
            return 3072
        # Default dimension
        return 384

    @classmethod
    def get_embedding(cls, text: str, model_name: str = "all-MiniLM-L6-v2") -> List[float]:
        """Generates embedding vector for a given string of text."""
        dimension = cls.get_dimension(model_name)
        
        # Try to use sentence-transformers if it's the MiniLM model
        if "minilm" in model_name.lower():
            global _transformer_model
            try:
                if _transformer_model is None:
                    from sentence_transformers import SentenceTransformer
                    logger.info("Initializing SentenceTransformer Model: all-MiniLM-L6-v2")
                    _transformer_model = SentenceTransformer("all-MiniLM-L6-v2")
                
                vector = _transformer_model.encode(text)
                return vector.tolist()
            except Exception as e:
                logger.warning(f"Failed to use SentenceTransformer for embedding: {str(e)}. Using fallback generator.")
        
        # Fallback/mock deterministic vector generator using text hash.
        # This produces reproducible vectors for tests and guarantees no network/file system dependencies block execution.
        return cls._generate_fallback_vector(text, dimension)

    @classmethod
    def get_embeddings(cls, texts: List[str], model_name: str = "all-MiniLM-L6-v2") -> List[List[float]]:
        """Generates embeddings for a batch of texts."""
        return [cls.get_embedding(t, model_name) for t in texts]

    @staticmethod
    def _generate_fallback_vector(text: str, dimension: int) -> List[float]:
        """Generates a deterministic pseudo-random unit vector based on input text."""
        # Use sha256 to seed generator
        hasher = hashlib.sha256(text.encode("utf-8"))
        seed = int(hasher.hexdigest()[:8], 16)
        rng = np.random.default_rng(seed)
        
        vector = rng.normal(size=dimension)
        # Normalize to unit vector
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector.tolist()
