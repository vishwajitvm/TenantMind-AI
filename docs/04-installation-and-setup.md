# 04. Installation & Setup

This guide walks through deploying the TenantMind AI containerized ecosystem for local development, staging, or testing.

## 1. Prerequisites
Ensure the target system meets these requirements:
* **Docker Engine** v20.10+ and **Docker Compose** v2.0+
* **Python** 3.10+ (for direct local environment development)
* **Node.js** 18+ and **npm** or **yarn** (for frontend UI changes)
* Minimum **8GB RAM** recommended (due to multiple running services: Keycloak, Qdrant, Redis, MongoDB, and FastAPI).

---

## 2. Configuration & Environment Variables

Copy the template `.env` file (or create one) in the project root:

```env
# System Configuration
ENVIRONMENT=development
SECRET_KEY=supersecretjwtkeyforlocaldevelopmentonlychangeinprod

# MongoDB Settings
MONGO_URI=mongodb://root:rootpassword@mongodb:27017/tenantmind?authSource=admin
MONGO_DB_NAME=tenantmind

# Redis & Celery Settings
REDIS_URL=redis://redis:6379/0

# Qdrant Settings
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# MinIO Object Storage
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=tenantmind-assets

# Keycloak Authentication
KEYCLOAK_SERVER_URL=http://keycloak:8080/auth
KEYCLOAK_REALM=tenantmind
KEYCLOAK_CLIENT_ID=tenantmind-app
KEYCLOAK_CLIENT_SECRET=keycloakclientsecretvalue

# LLM Providers (API Keys)
GEMINI_API_KEY=your-gemini-api-key
GROQ_API_KEY=your-groq-api-key
OPENROUTER_API_KEY=your-openrouter-api-key
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

---

## 3. Launching the Services

To spin up all services in daemon mode:

```bash
docker-compose up --build -d
```

### Port Mappings
The services are exposed on the following ports for external management:
* **Nginx Gateway**: `http://localhost:80` (main client interface)
* **Keycloak Admin**: `http://localhost:8080/auth` (admin/admin credentials)
* **MinIO Console**: `http://localhost:9001` (minioadmin/minioadmin credentials)
* **MongoDB Express / Port**: `localhost:27017`
* **Qdrant Dashboard**: `http://localhost:6333/dashboard`
* **Grafana Telemetry**: `http://localhost:3000` (admin/admin credentials)
* **Prometheus API**: `http://localhost:9090`

---

## 4. Keycloak Identity Initialization

Before logging into the application:
1. Open `http://localhost:8080/auth` and sign in to the **Master** admin console.
2. Click **Create Realm** and import or create a realm named `tenantmind`.
3. Go to **Clients** -> click **Create** -> client ID `tenantmind-app`, access type `confidential`, valid redirect URI `http://localhost/*`.
4. Go to **Roles** and create: `tenant`, `landlord`, `vendor`, and `admin`.
5. Under **Users**, create a dummy user, assign them to a role, and configure their credentials (disable "Temporary Password").
