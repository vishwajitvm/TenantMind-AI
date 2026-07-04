from fastapi import APIRouter
from app.config import settings

router = APIRouter(prefix="/models", tags=["Models"])

@router.get("")
async def list_models():
    """Lists configured LLMs and Embedding models based on API key availability."""
    return {
        "llms": [
            {
                "provider": "Gemini",
                "model": "gemini-1.5-flash",
                "configured": bool(settings.GEMINI_API_KEY)
            },
            {
                "provider": "Groq",
                "model": "llama3-8b-8192",
                "configured": bool(settings.GROQ_API_KEY)
            },
            {
                "provider": "OpenRouter",
                "model": "meta-llama/llama-3-8b-instruct:free",
                "configured": bool(settings.OPENROUTER_API_KEY)
            },
            {
                "provider": "Ollama",
                "model": "llama3",
                "configured": True  # Defaults to localhost service
            }
        ],
        "embedding_models": [
            {
                "model": "all-MiniLM-L6-v2",
                "dimension": 384,
                "type": "local"
            },
            {
                "model": "text-embedding-3-small",
                "dimension": 1536,
                "type": "api"
            },
            {
                "model": "text-embedding-3-large",
                "dimension": 3072,
                "type": "api"
            }
        ]
    }
