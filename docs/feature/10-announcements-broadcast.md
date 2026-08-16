# Feature 10: Announcements Broadcast

## Layman Guide
Sends bulk messages to all tenants in a building or property.

## Technical Guide
FastAPI receives request, fetches list of active tenants, queues individual notifications.

## Flow
1. Admin posts announcement.
2. System fetches tenant lists.
3. Delivers via WebSockets and Email.

## Data Schema
```json
{
  "broadcast_id": "uuid",
  "title": "Water Shutdown",
  "target_property": "uuid"
}
```

## Edge Cases
- **Massive subscriber list blocking loop**: Chunk distributions in batch sizes of 100 via Celery.
