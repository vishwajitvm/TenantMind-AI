# Feature 02: Maintenance Request Routing

## Layman Guide
Allows tenants to file tickets with pictures. The system automatically categorizes and sends it to the right vendor.

## Technical Guide
FastAPI handles multi-part form uploads. Celery workers parse text to auto-tag categories (plumbing, electrical) using zero-shot classification, and dispatch to matched vendor.

## Flow
1. Tenant uploads issue.
2. File goes to MinIO, metadata to MongoDB.
3. Worker runs classification.
4. Matches vendor ID.

## Data Schema
```json
{
  "ticket_id": "uuid",
  "category": "plumbing",
  "vendor_id": "uuid",
  "status": "ASSIGNED"
}
```

## Edge Cases
- **No matching vendor found**: Route ticket to fallback 'General Admin' bucket and alert dashboard.
