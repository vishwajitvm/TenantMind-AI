import time
import httpx
from typing import List, Dict, Any, Optional
from app.config import settings
from app.database import get_db
from tracenest import logger

async def log_llm_attempt(
    tenant_id: str,
    provider: str,
    model: str,
    duration: float,
    status: str,
    input_tokens: int,
    output_tokens: int,
    error_msg: Optional[str] = None
):
    """Logs the LLM gateway attempt to MongoDB audit/model metrics and TraceNest logger."""
    metric = {
        "tenant_id": tenant_id,
        "provider": provider,
        "model": model,
        "latency_seconds": duration,
        "status": status,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "error": error_msg,
        "timestamp": time.time()
    }
    
    # Log to TraceNest
    if status == "success":
        logger.info(f"LLM Success | Tenant: {tenant_id} | Provider: {provider} | Model: {model} | Latency: {duration:.4f}s | Tokens: {metric['total_tokens']}")
    else:
        logger.error(f"LLM Failure | Tenant: {tenant_id} | Provider: {provider} | Model: {model} | Latency: {duration:.4f}s | Error: {error_msg}")
    
    # Save to MongoDB
    try:
        db = get_db()
        await db.llm_metrics.insert_one(metric)
    except Exception as e:
        logger.error(f"Failed to save LLM metric to database: {str(e)}")

class ModelGateway:
    @staticmethod
    async def try_gemini(messages: List[Dict[str, str]], tenant_id: str) -> Dict[str, Any]:
        if not settings.GEMINI_API_KEY:
            raise ValueError("Gemini API key is not configured")
        
        # Format last message content for Gemini
        prompt = messages[-1].get("content", "")
        # Build conversation representation or just the last query
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        start_time = time.time()
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            duration = time.time() - start_time
            
            if resp.status_code != 200:
                raise RuntimeError(f"Gemini API returned status {resp.status_code}: {resp.text}")
            
            data = resp.json()
            # Extract content
            try:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                raise RuntimeError(f"Unexpected response format from Gemini: {data}")
            
            # Estimate token usage
            input_tokens = len(prompt.split())  # simple heuristic
            output_tokens = len(content.split())
            
            await log_llm_attempt(tenant_id, "Gemini", "gemini-1.5-flash", duration, "success", input_tokens, output_tokens)
            return {
                "content": content,
                "provider": "Gemini",
                "model": "gemini-1.5-flash",
                "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens, "total_tokens": input_tokens + output_tokens},
                "latency": duration
            }

    @staticmethod
    async def try_groq(messages: List[Dict[str, str]], tenant_id: str) -> Dict[str, Any]:
        if not settings.GROQ_API_KEY:
            raise ValueError("Groq API key is not configured")
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        model_name = "llama3-8b-8192"
        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": 0.7
        }
        
        start_time = time.time()
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            duration = time.time() - start_time
            
            if resp.status_code != 200:
                raise RuntimeError(f"Groq API returned status {resp.status_code}: {resp.text}")
            
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            input_tokens = usage.get("prompt_tokens", len(str(messages).split()))
            output_tokens = usage.get("completion_tokens", len(content.split()))
            
            await log_llm_attempt(tenant_id, "Groq", model_name, duration, "success", input_tokens, output_tokens)
            return {
                "content": content,
                "provider": "Groq",
                "model": model_name,
                "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens, "total_tokens": input_tokens + output_tokens},
                "latency": duration
            }

    @staticmethod
    async def try_openrouter(messages: List[Dict[str, str]], tenant_id: str) -> Dict[str, Any]:
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("OpenRouter API key is not configured")
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        model_name = "meta-llama/llama-3-8b-instruct:free"
        payload = {
            "model": model_name,
            "messages": messages
        }
        
        start_time = time.time()
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            duration = time.time() - start_time
            
            if resp.status_code != 200:
                raise RuntimeError(f"OpenRouter API returned status {resp.status_code}: {resp.text}")
            
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            input_tokens = usage.get("prompt_tokens", len(str(messages).split()))
            output_tokens = usage.get("completion_tokens", len(content.split()))
            
            await log_llm_attempt(tenant_id, "OpenRouter", model_name, duration, "success", input_tokens, output_tokens)
            return {
                "content": content,
                "provider": "OpenRouter",
                "model": model_name,
                "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens, "total_tokens": input_tokens + output_tokens},
                "latency": duration
            }

    @staticmethod
    async def try_ollama(messages: List[Dict[str, str]], tenant_id: str) -> Dict[str, Any]:
        url = f"{settings.OLLAMA_BASE_URL}/api/chat"
        payload = {
            "model": "llama3",
            "messages": messages,
            "stream": False
        }
        
        start_time = time.time()
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload)
            duration = time.time() - start_time
            
            if resp.status_code != 200:
                raise RuntimeError(f"Ollama returned status {resp.status_code}: {resp.text}")
            
            data = resp.json()
            content = data["message"]["content"]
            input_tokens = len(str(messages).split())
            output_tokens = len(content.split())
            
            await log_llm_attempt(tenant_id, "Ollama", "llama3", duration, "success", input_tokens, output_tokens)
            return {
                "content": content,
                "provider": "Ollama",
                "model": "llama3",
                "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens, "total_tokens": input_tokens + output_tokens},
                "latency": duration
            }

    @classmethod
    async def generate(cls, messages: List[Dict[str, str]], tenant_id: str = "default") -> Dict[str, Any]:
        """Runs the Multi-Model fallback chain: Gemini -> Groq -> OpenRouter -> Ollama.
        If all fail or are unconfigured, we run a simulated fallback (mock LLM) to ensure system usability.
        """
        errors = []
        
        # 1. Gemini
        try:
            return await cls.try_gemini(messages, tenant_id)
        except Exception as e:
            errors.append(f"Gemini failed: {str(e)}")
            
        # 2. Groq
        try:
            return await cls.try_groq(messages, tenant_id)
        except Exception as e:
            errors.append(f"Groq failed: {str(e)}")
            
        # 3. OpenRouter
        try:
            return await cls.try_openrouter(messages, tenant_id)
        except Exception as e:
            errors.append(f"OpenRouter failed: {str(e)}")
            
        # 4. Ollama
        try:
            return await cls.try_ollama(messages, tenant_id)
        except Exception as e:
            errors.append(f"Ollama failed: {str(e)}")
            
        # 5. Local Mock Simulation Fallback
        # If we got here, all providers failed. For resilience (e.g. testing / demo),
        # return a mock LLM response instead of crashing.
        logger.warning(f"All LLM providers failed. Falling back to Mock LLM. Errors: {errors}")
        start_time = time.time()
        time.sleep(0.05) # simulate latency
        duration = time.time() - start_time
        prompt = messages[-1].get("content", "")
        mock_response = f"[Mock Fallback LLM Response] Received your message: '{prompt}'"
        input_tokens = len(str(messages).split())
        output_tokens = len(mock_response.split())
        
        await log_llm_attempt(tenant_id, "MockFallback", "mock-llama", duration, "success", input_tokens, output_tokens)
        return {
            "content": mock_response,
            "provider": "MockFallback",
            "model": "mock-llama",
            "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens, "total_tokens": input_tokens + output_tokens},
            "latency": duration
        }
