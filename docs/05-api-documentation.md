# 05. API Documentation

TenantMind AI exposes a REST API via FastAPI. Below are key endpoints.

## Authentication
All requests (except public endpoints) require a Bearer JWT Token issued by Keycloak.

## Endpoints
- `GET /api/properties`: List properties.
- `POST /api/properties`: Create property.
- `POST /api/leases/query`: semantic vector search over lease agreements.
- `POST /api/maintenance`: Create maintenance request.
- `GET /api/metrics`: Prometheus metrics scraping target.
