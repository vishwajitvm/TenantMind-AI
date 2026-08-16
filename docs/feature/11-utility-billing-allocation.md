# Feature 11: Utility Billing Allocation

## Layman Guide
Calculates and splits shared bills (water, trash) based on apartment size or residents.

## Technical Guide
Celery task computes formulas on billing data and updates tenant balances.

## Flow
1. Master bill uploaded.
2. Worker runs allocation algorithm.
3. Invoices posted.

## Data Schema
```json
{
  "bill_id": "uuid",
  "allocated_amounts": [{"tenant_id": "uuid", "amount": 45.50}]
}
```

## Edge Cases
- **Unoccupied units**: Subdue or allocate costs to landlord profile.
