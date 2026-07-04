# Feature 15: Document Vault Storage

## Layman Guide
Safe digital cabinet for leases, receipts, and identification.

## Technical Guide
Uploads are stored in MinIO. Access control list verified at FastAPI middleware level.

## Flow
1. User uploads document.
2. MinIO storage confirmed.
3. Record saved in MongoDB Vault collection.

## Data Schema
```json
{
  "doc_id": "uuid",
  "owner_id": "uuid",
  "acl": "private"
}
```

## Edge Cases
- **Direct MinIO access**: Implement time-limited pre-signed URLs; direct URLs are forbidden.
