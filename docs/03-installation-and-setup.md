# 03. Installation & Setup

Follow these steps to run TenantMind AI in development or production.

## Prerequisites
- Docker & Docker Compose (v2.x)
- Python 3.10+ (for local development)
- Node.js 18+ (for frontend development)

## Setup Steps
1. Clone the repository and configure environment variables in `.env`.
2. Build and start containers:
   ```bash
   docker-compose up --build -d
   ```
3. Initialize Keycloak realm via the admin console at `http://localhost:8080` (admin/admin).
4. Run frontend dev server locally or access it through Nginx at `http://localhost`.
