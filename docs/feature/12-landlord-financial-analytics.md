# Feature 12: Landlord Financial Analytics

## 1. Layman Guide
Landlords can view charts and reports showing property performance, monthly rental income, unpaid balances, and maintenance expenses to help track net profits.

---

## 2. Technical Guide
* **Aggregation**: Runs MongoDB aggregation pipelines to summarize transactional payments.
* **API Delivery**: REST API routes deliver formatted JSON payloads to Next.js dashboard charts.
* **Cache Strategy**: Dashboard metrics are cached in Redis with a 5-minute TTL to reduce database load.

---

## 3. Step-by-Step Flow
1. **Request**: Landlord views the analytics dashboard.
2. **Retrieve**: API fetches cached metrics from Redis or runs a MongoDB aggregation query.
3. **Format**: Returns income, occupancy, and expense logs.
4. **Render**: The Next.js dashboard renders data using visual charts.

---

## 4. Data Schema
```json
{
  "total_revenue": 145000.00,
  "occupancy_rate": 96.5,
  "expenses": [
    { "category": "maintenance", "amount": 12000.00 }
  ]
}
```

---

## 5. Edge Cases & Mitigations
* **Null records**: Aggregations use default fallbacks (`$ifNull`) to ensure that missing database records do not break dashboard rendering.
