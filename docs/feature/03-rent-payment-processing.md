# Feature 03: Rent Payment Processing

## Layman Guide
Secures digital payments for monthly rent, giving tenants options for cards or direct bank transfers.

## Technical Guide
REST API interfaces with payment processor (mocked). Emits state transitions via WebSockets and schedules retries on payment failures.

## Flow
1. Invoice generated.
2. Tenant authorizes payment.
3. Webhook catches success/failure.
4. DB updated.

## Data Schema
```json
{
  "payment_id": "uuid",
  "amount": 1200.00,
  "status": "COMPLETED"
}
```

## Edge Cases
- **Double charging due to retry clicks**: Implement idempotency keys (`Idempotency-Key`) on all POST /payment operations.
