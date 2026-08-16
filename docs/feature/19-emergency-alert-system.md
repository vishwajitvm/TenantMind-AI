# Feature 19: Emergency Alert System

## Layman Guide
Broadcasts urgent safety alerts immediately (fires, extreme weather).

## Technical Guide
Bypasses standard queues; uses direct high-priority sockets and instant SMS APIs (Twilio).

## Flow
1. Admin triggers Emergency.
2. Direct gateway call.
3. Socket broadcast + SMS dispatch.

## Data Schema
```json
{
  "alert_id": "uuid",
  "severity": "CRITICAL",
  "message": "Evacuate building A"
}
```

## Edge Cases
- **SMS API down**: Log error, fall back to bulk email and mobile push notifications.
