# Feature 12: Landlord Financial Analytics

## Layman Guide
Charts and tables illustrating rental yields and net profits.

## Technical Guide
FastAPI runs aggregation pipelines over MongoDB `payments` collection.

## Flow
1. User requests dashboard.
2. Aggregation pipeline executes.
3. JSON returned to Next.js chart components.

## Data Schema
```json
{
  "net_income": 45000.00,
  "expenses": 12000.00,
  "occupancy_rate": 0.94
}
```

## Edge Cases
- **Missing payment fields**: Ensure default zero fallback in aggregation queries.
