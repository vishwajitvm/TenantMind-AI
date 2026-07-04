# 02. Architecture & System Design

TenantMind AI utilizes a service-oriented, containerized architecture designed to support scale, security, and high reliability. The platform is decoupled into dedicated services for routing, presentation, API logic, asynchronous task execution, storage, and telemetry.

## 1. High-Level Container Breakdown

The system is defined and orchestrated using a unified `docker-compose.yml` containing the following services:

### A. Routing & Gateway Layer
* **Nginx Gateway**: Serves as the single entrypoint for all incoming traffic. Routes `/` to the Next.js Frontend, `/api/` to the FastAPI Backend, `/auth/` to Keycloak OIDC, and `/tracenest` to backend telemetry.

### B. Application Layer
* **FastAPI Backend**: Powered by ASGI (Uvicorn), this service handles HTTP request resolution, tenancy context extraction, and interfaces with databases.
* **Next.js Frontend**: A modern web client using React, Tailwind CSS, and Zustand. Fetches state via REST APIs and holds persistent connections via WebSockets.
* **Celery Worker**: Asynchronous worker pool executing file processing (OCR, vector chunking), email dispatches, and third-party integrations.
* **Celery Scheduler (Beat)**: Emits periodic heartbeat tasks for invoicing, cron jobs, and ledger balance reconciliation.

### C. Data & Search Layer
* **MongoDB**: A document store hosting property inventories, lease metadata, tenant profiles, maintenance tickets, and audit logs.
* **Qdrant**: A high-performance vector database storing embedding vectors generated from lease clauses to enable semantic context retrieval.
* **Redis**: Serves as the message broker for Celery and a transient caching tier for API endpoints.
* **PostgreSQL**: The relational database backend dedicated to Keycloak for storing user identity, roles, credentials, and client configurations.

### D. Security & Storage Layer
* **Keycloak**: OpenID Connect (OIDC) identity provider managing tenant registration, multi-tenant group mappings, and JWT token signatures.
* **MinIO**: S3-compatible object storage repository for documents, inspection checklists, receipts, and maintenance images.

### E. Telemetry & Observability Layer
* **Prometheus**: Metrics aggregator pulling instrumentation endpoints from the backend and Nginx.
* **Grafana**: Web console containing pre-configured dashboard views monitoring the system's operational health.

---

## 2. Dynamic Component Interaction & Data Flows

The system relies on asynchronous patterns to ensure UI responsiveness. Below is the main sequence of a RAG query flow:

```
[Next.js Client] -> (JWT Token) -> [Nginx Gateway] -> [FastAPI Backend]
                                                            |
                                                   (Tenancy Filter)
                                                            |
                                                            v
[Qdrant (Vectors)] <--- (Embedding) <--- [Embedding Gateway (sentence-transformers)]
        |
        +--> (Text Chunks) -> [Model Gateway (LLM Fallbacks)] -> [Next.js Client]
```
All details on specific modules, database configurations, and code interactions are outlined in the subsequent chapters.
