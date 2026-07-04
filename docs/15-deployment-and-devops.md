# 15. Deployment & DevOps

TenantMind AI is deployed using standard container engines.

## Environments
- **Staging**: Deployed automatically via CI/CD (GitHub Actions) to AWS ECS.
- **Production**: Multi-AZ deployments with managed AWS DocumentDB, Redis, and Qdrant Cloud.
