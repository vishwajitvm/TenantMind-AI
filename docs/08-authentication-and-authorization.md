# 08. Authentication & Authorization

TenantMind AI deploys an enterprise-grade identity administration scheme via Keycloak OIDC.

## 1. Authentication Authentication Flow

```
[Client App] ---> Requests authentication ---> [Keycloak Login Prompt]
     ^                                                  |
     |                                                  v
Redirects to client <--- Returns JWTs & Refresh <--- Valid credentials
```

1. **Redirect**: Unauthenticated Next.js sessions redirect to `http://localhost:8080/auth/realms/tenantmind/protocol/openid-connect/auth`.
2. **Access Token Generation**: Upon verification, Keycloak redirects back to the configured URL, returning an **AccessToken**, **IDToken**, and **RefreshToken**.
3. **API Requests**: The Next.js client intercepts outgoing fetch requests and includes the Access Token in the `Authorization` header.

---

## 2. JWT Access Token Structure

FastAPI decrypts and verifies the RS256 signature using Keycloak's public keys fetched via the JSON Web Key Set (JWKS) endpoint. Below is an example payload representation:

```json
{
  "exp": 1783267200,
  "iss": "http://localhost:8080/auth/realms/tenantmind",
  "sub": "b2c9e782-fa82-411a-82c0-82a1a8c9e88d",
  "email": "john.doe@tenantmind.com",
  "resource_access": {
    "tenantmind-app": {
      "roles": ["tenant"]
    }
  },
  "tenant_id": "tenant-uuid-custom-claim"
}
```

---

## 3. Tenancy Isolation & Role Guarding

The backend extracts the token payload in standard middleware:
* **Roles Check**: Declared via decorators:
  ```python
  @app.get("/api/approvals")
  @require_role("landlord")
  async def get_approvals(request: Request):
      ...
  ```
* **Tenancy Database Scoping**: Every query filters by `tenant_id` parsed from the JWT claims to block cross-tenant database leakage.
