# Feature 17: Multi-Tenant Access Control

## Layman Guide
Ensures tenants only see their units, and landlords only see their properties.

## Technical Guide
API uses tenancy context extraction from Keycloak tokens. MongoDB queries include `landlord_id` or `tenant_id` filters.

## Flow
1. Client requests data.
2. Middleware reads JWT claims.
3. Database filters matching scope.

## Data Schema
```json
{
  "tenant_id": "uuid",
  "accessible_units": ["unit_1"]
}
```

## Edge Cases
- **Sub-lease tenant access**: Add sub-tenant mapping structure inside unit metadata to grant access.
