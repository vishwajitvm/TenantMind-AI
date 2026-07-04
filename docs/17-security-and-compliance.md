# 17. Security & Compliance

TenantMind AI enforces strict technical safeguards to secure customer profiles, financial transaction logs, and private documents.

## 1. Data Protection & Cryptography
* **In-Transit Encryption**: All communication is encrypted using TLS 1.3. HTTP requests are redirected to HTTPS.
* **At-Rest Encryption**: MongoDB databases and MinIO storage volumes use AES-256 block encryption.
* **Token Rotation**: OIDC Access Tokens expire in 15 minutes, forcing periodic refresh token swaps.

---

## 2. Multi-Tenant Separation & Isolation
To prevent data leaks between tenants:
* **Token Enforcement**: Every database query is scoped with `tenant_id` claims parsed directly from OIDC signatures.
* **API Validation**: Cross-tenancy verification checks are run at the middleware level before returning property or lease info.

---

## 3. Compliance Frameworks (GDPR & SOC 2)
* **Right to be Forgotten (GDPR)**: Users can submit account deletion requests. Celery scripts clear their documents from MongoDB, Keycloak, and Qdrant.
* **Auditing (SOC 2)**: All administrative, configuration, and security actions are logged to an immutable MongoDB audit trail collection.
