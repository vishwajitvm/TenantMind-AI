# 16. Deployment & DevOps

This manual details how TenantMind AI is built, tested, and deployed across environments.

## 1. CI/CD Pipeline (GitHub Actions)
Every pull request and merge to `main` triggers our GitHub Actions pipeline:
1. **Lints & Style Check**: Verifies formatting (`black` and `flake8` for Python, `eslint` for Next.js).
2. **Automated Tests**: Launches the test suite with coverage thresholds.
3. **Image Building**: Builds multi-architecture Docker images for `backend`, `frontend`, and `worker`.
4. **Registry Push**: Uploads tagged images to Amazon Elastic Container Registry (ECR).

---

## 2. Infrastructure Deployments

### A. Local / Staging Environments
* Deployed using `docker-compose.yml` on a single host. Nginx acts as the entrypoint for routing and SSL termination.

### B. Production Environment (AWS ECS & Fargate)
For enterprise scalability, Docker Compose is replaced by native cloud infrastructure:
* **API Routing**: AWS Application Load Balancer routes traffic to ECS Fargate services.
* **Database Scaling**: DocumentDB handles MongoDB scaling; Qdrant Cloud hosts vector collections.
* **Identity Management**: Keycloak is deployed on ECS connected to an AWS Aurora PostgreSQL database.
