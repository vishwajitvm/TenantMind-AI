# Feature 08: Property Listing Manager

## Layman Guide
Enables landlords to manage apartments, list amenities, and upload photos.

## Technical Guide
CRUD endpoints in FastAPI with multipart uploads for images. Integrates with MinIO.

## Flow
1. Landlord fills property details.
2. Uploads photos.
3. Database inserts record.

## Data Schema
```json
{
  "property_id": "uuid",
  "address": "123 Main St",
  "amenities": ["Gym", "Pool"]
}
```

## Edge Cases
- **Corrupt images**: Run mime-type and magic bytes check. Reject non-image headers.
