# Feature 18: Activity Audit Logging

## Layman Guide
Logs all actions (e.g. lease updates, payments) for compliance.

## Technical Guide
FastAPI middleware captures requests, sends payload asynchronously to audit log queue in Redis.

## Flow
1. Admin performs critical action.
2. Middleware intercept.
3. Async log write to MongoDB audit collection.

## Data Schema
```json
{
  "log_id": "uuid",
  "actor": "admin_uuid",
  "action": "UPDATE_LEASE",
  "timestamp": "iso8601"
}
```

## Edge Cases
- **Audit collection offline**: Buffer audit records in local memory or Redis list; trigger alert.
