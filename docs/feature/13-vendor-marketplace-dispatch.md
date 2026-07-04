# Feature 13: Vendor Marketplace & Dispatch

## Layman Guide
Connects local maintenance experts (plumbers, electricians) with work orders.

## Technical Guide
FastAPI interfaces with vendor directories, evaluates response time metrics, and sends job invites.

## Flow
1. Work order created.
2. Matching vendors notified.
3. First to accept gets assigned.

## Data Schema
```json
{
  "work_order_id": "uuid",
  "vendor_id": "uuid",
  "accepted_at": "timestamp"
}
```

## Edge Cases
- **No vendor accepts**: Escalate ticket to 'Emergency Admin' list after 2 hours.
