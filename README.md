# TenantMind AI: Intelligent Property Management System

TenantMind AI is a modern, containerized property management platform leveraging state-of-the-art AI, vector databases, and enterprise identity management to automate landlord workflows and tenant communication.

## 1. Key System Components
* **FastAPI Backend**: Hosts the REST API gateways, WebSocket connections, and RAG execution paths.
* **Next.js Frontend**: Presents a dashboard and AI chat console utilizing Zustand, React Query, and Tailwind.
* **Celery & Redis**: Background job queue processing PDF parsing, utility allocations, and rent billing checks.
* **Keycloak**: Core OpenID Connect identity provider ensuring tenant-isolation data scopes.
* **MongoDB**: Core document store managing user profiles, tickets, and payments.
* **Qdrant**: High-performance vector database storing lease document embeddings.
* **MinIO**: S3-compatible asset store.
* **Prometheus & Grafana**: Infrastructure instrumentation and telemetry logs dashboard.
* **Nginx**: Reverse proxy unifying routing.

---

## 2. Quick Start
To build and launch the platform:
```bash
docker-compose up --build -d
```
All details regarding installation and configuration can be found in [docs/04-installation-and-setup.md](file:///c:/python/TenantMind%20AI/docs/04-installation-and-setup.md).
Please check [docs/03-complete-beginner-guide.md](file:///c:/python/TenantMind%20AI/docs/03-complete-beginner-guide.md) for an overview of the AI and database technologies used in this project.
