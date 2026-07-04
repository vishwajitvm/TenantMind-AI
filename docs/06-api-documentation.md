# 06. API Documentation

TenantMind AI exposes RESTful routes through a FastAPI application.

## 1. Authentication Header
All endpoints (excluding `/api/health` and general root status) verify authentication tokens using Keycloak OpenID Connect. The user must provide the JWT in the standard format:
```http
Authorization: Bearer <your-jwt-access-token>
```

---

## 2. Primary API Endpoints

### A. Chats & Assistant (`/api/chats`)
* **`POST /api/chats/message`**: Sends a text message to the AI agent.
  * **Payload**:
    ```json
    {
      "message": "Can I sublease?"
    }
    ```
  * **Response (200)**:
    ```json
    {
      "reply": "According to your lease, subleasing is permitted under Section 14 with written consent.",
      "source": "Qdrant Vector RAG"
    }
    ```

### B. Leases & Documents (`/api/documents`)
* **`POST /api/documents/upload`**: Uploads a lease agreement PDF file (Multipart/Form-Data). Triggers Celery processing task.
  * **Response (202)**:
    ```json
    {
      "task_id": "job_uuid_123",
      "status": "QUEUED"
    }
    ```
* **`GET /api/documents/status/{task_id}`**: Returns the background parser status.

### C. MCP Approvals (`/api/approvals`)
* **`GET /api/approvals/pending`**: (Landlord only) Retrieves a list of pending tool calls requiring confirmation.
* **`POST /api/approvals/action`**: Approves or denies an MCP tool call.
  * **Payload**:
    ```json
    {
      "approval_id": "string",
      "action": "approve | deny"
    }
    ```

### D. Audit Logging (`/api/audit-logs`)
* **`GET /api/audit-logs`**: (Admin only) Fetches global event trail records.

### E. Health Metrics (`/api/health`)
* **`GET /api/health`**: Returns system availability status.
* **`GET /api/health/metrics`**: Exposes Prometheus-scraplable metrics.
