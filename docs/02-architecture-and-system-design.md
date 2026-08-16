# 02. Architecture & System Design

TenantMind AI uses a service-oriented, containerized architecture that integrates various high-performance databases, brokers, and application servers.

## Core Container Components
1. **Nginx Reverse Proxy**: Gateway routes `/api/` to Backend, `/auth/` to Keycloak, and default `/` to Frontend.
2. **FastAPI Backend**: Hosts RESTful API and Tracenest tracing middleware.
3. **Next.js Frontend**: Built with React and Zustand, managing real-time websocket connections.
4. **Celery Worker & Scheduler**: Handles background processing (reminders, billing, scraping).
5. **Databases**: MongoDB (document storage), Qdrant (vector search), Redis (broker/cache), Postgres (Keycloak DB).
