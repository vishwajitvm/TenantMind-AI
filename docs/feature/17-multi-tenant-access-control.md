# Feature 17: Multi-Tenant Access Control

## 1. Layman Guide
This security mechanism acts like virtual walls, ensuring tenants can only access information related to their own lease, and landlords can only view properties they own.

---

## 2. Technical Guide
* **Token Extraction**: The API extracts the user's role and tenant scope from incoming Keycloak OIDC JWT tokens.
* **Query Scoping**: Database queries include tenant filtering criteria based on the token scope.

---

## 3. Step-by-Step Flow
1. **Request**: User requests data from an API endpoint.
2. **Decode**: FastAPI middleware validates the OIDC token and extracts tenant scope.
3. **Filter**: Database queries are automatically scoped using the tenant ID.
4. **Deliver**: The API returns only the authorized subset of records.

---

## 4. Data Schema
```json
{
  "request_context": {
    "user_id": "string (UUID)",
    "role": "tenant",
    "authorized_tenant_id": "tenant-uuid-1"
  }
}
```

---

## 5. Edge Cases & Mitigations
* **Sub-tenant access permissions**: When a lease is sub-let, landlords can add sub-tenant mappings to the unit profile in MongoDB to grant access.
