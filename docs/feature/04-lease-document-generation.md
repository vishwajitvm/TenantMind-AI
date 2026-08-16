# Feature 04: Lease Document Generation

## Layman Guide
Dynamically generates standard lease agreements in PDF format based on unit and tenant variables.

## Technical Guide
FastAPI Backend compiles LaTeX/HTML templates, inserts MongoDB variables, renders to PDF, and uploads output to MinIO.

## Flow
1. Landlord triggers generation.
2. Backend queries MongoDB.
3. Render PDF, upload to MinIO.
4. Return URL.

## Data Schema
```json
{
  "lease_id": "uuid",
  "minio_path": "leases/lease_uuid.pdf",
  "status": "DRAFT"
}
```

## Edge Cases
- **Name length overflow**: Wrap tables and limit characters in dynamic fields to prevent layout corruption.
