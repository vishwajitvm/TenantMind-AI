# 15. Testing & Quality Assurance

TenantMind AI enforces code quality through automated test suits run via `pytest`.

## 1. Test Suite Structure
Tests are organized inside `backend/tests/` and cover three key layers:
* **Unit Tests**: Mocks third-party APIs (Gemini, Keycloak, Qdrant) to test core FastAPI endpoint routing, middleware response headers, and helpers.
* **Integration Tests**: Launches transactional database states (in-memory or test-scoped containers) to test celery task pipelines, token decode logic, and MongoDB CRUD operations.
* **Ingestion Tests**: Assesses PDF reading, sentence chunk extraction, and database indexing.

---

## 2. Test Commands & Coverage
To execute tests locally:
```bash
# Navigate to backend and run pytest
cd backend
pytest -v --cov=app tests/
```

### Key Mocking Patterns
To guarantee test suite isolation, we mock network boundaries:
* **LLM Mocking**: Overrides the `ModelGateway.generate()` call to return fixed payloads immediately without hitting external APIs.
* **Keycloak Token Overriding**: The JWT decoder is mocked in tests using an in-memory public key verification helper to simulate authorized/unauthorized request headers.
