# Feature 01: Tenant Onboarding

## Layman Guide
A workflow that lets new tenants upload their details, complete verification, sign leases, and generate credentials.

## Technical Guide
Next.js workflow coordinates steps. FastAPI validates input schema, registers the user in Keycloak, creates a profile in MongoDB, and triggers a welcome email via Celery.

## Flow
1. Guest visits invite link.
2. Fills details & uploads verification documents.
3. FastAPI saves files to MinIO.
4. Keycloak registers user under the `tenant` role.

## Data Schema
```json
{
  "tenant_id": "uuid",
  "verification_status": "PENDING",
  "minio_docs": ["url1"]
}
```

## Edge Cases
- **Keycloak registration fails halfway**: Clean up MinIO uploads and roll back MongoDB entries to avoid orphaned profiles.
