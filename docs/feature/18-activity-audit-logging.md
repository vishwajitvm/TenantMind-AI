# Feature 18: Activity Audit Logging

## 1. Layman Guide
The system logs every administrative action (such as changes to leases or payment overrides) to create a clear, unalterable trail of who did what and when.

---

## 2. Technical Guide
* **Interception**: FastAPI middleware intercepts incoming HTTP requests.
* **Logging**: Critical actions write log events to a dedicated MongoDB collection.
* **Propagation**: Request trace IDs (`X-Trace-ID`) are passed to Celery workers to group logs across services.

---

## 3. Step-by-Step Flow
1. **Action**: Landlord updates a tenant's monthly lease price.
2. **Intercept**: Middleware captures details about the user and request.
3. **Write**: The backend logs the event to the MongoDB audit collection.
4. **Complete**: The system applies the change and returns a success status.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "trace_id": "string (UUID)",
  "actor_id": "string (UUID)",
  "action": "UPDATE_LEASE_RENT",
  "details": { "lease_id": "ObjectId", "old_rent": 1200.0, "new_rent": 1300.0 },
  "timestamp": 1783267200
}
```

---

## 5. Edge Cases & Mitigations
* **Database offline log buffer**: If the audit database goes offline, logs are buffered in Redis until connection is restored, preventing data loss.
