# TenantMind AI - Intelligent Property Management System

TenantMind AI is a next-generation property management and tenant communication platform. It utilizes LLMs, vector search, async workers, and enterprise authentication to deliver a seamless property management experience.

## Architecture Highlights
- **Backend**: FastAPI with async Motor (MongoDB) and Qdrant (vector search for lease and document queries).
- **Frontend**: Next.js with Zustand state management, Tailwind CSS, Lucide Icons, and React Query.
- **Message Broker & Queue**: Celery with Redis for asynchronous task processing and scheduled jobs.
- **Identity Provider**: Keycloak-based OpenID Connect (OIDC) integration for secure user management.
- **Monitoring & Metrics**: Prometheus metrics endpoint scraping, visualized with Grafana and logs routed to Loki.

## Getting Started
To get the system running locally:
```bash
docker-compose up --build
```
This starts the backend, worker, scheduler, frontend, database, Redis, Qdrant, MinIO, Keycloak, Prometheus, Grafana, and Nginx.

Please read the extensive manuals inside the `docs/` folder to understand deployment, security, feature setups, and the architecture in detail.
