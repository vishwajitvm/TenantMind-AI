# 18. Troubleshooting & FAQ

This handbook resolves common configuration issues and developer questions.

## 1. Diagnostics & Common Errors

### A. Keycloak Redirect Loop or Port Conflict
* **Symptom**: Page redirects repeatedly or Keycloak fails to boot.
* **Solution**: Keycloak binds to port `8080` by default. Verify that no local server (like Apache or another dev project) is running on `8080`. Ensure `KEYCLOAK_SERVER_URL` in `.env` is reachable from both host machine and docker network.

### B. Celery Worker "Connection Refused"
* **Symptom**: Tasks are not executing, logs show Redis connection failures.
* **Solution**: Redis container might be restarting or crashed. Inspect Redis status:
  ```bash
  docker-compose ps redis
  ```
  Ensure `REDIS_URL` uses the service name `redis` when running in Docker, and `localhost` only for bare-metal testing.

### C. Ollama Timeout or OOM (Out Of Memory)
* **Symptom**: LLM responses take >10 seconds or crash with status 500.
* **Solution**: Ollama models can be heavy for CPU-only systems. Change model target to a smaller model (e.g. `phi3` or `qwen2:0.5b`) or configure Gemini API keys to bypass local hosting.

---

## 2. Frequently Asked Questions

#### Q: How do I change the default admin credentials?
* **A**: Keycloak admin user/password is set in `docker-compose.yml` under `KEYCLOAK_USER` and `KEYCLOAK_PASSWORD` env variables. Change these and restart the container.

#### Q: Can I run multiple AI model providers concurrently?
* **A**: Yes. The `ModelGateway` is designed to fallback down a chain (Gemini -> Groq -> OpenRouter -> Ollama) dynamically depending on active API keys and responses.
