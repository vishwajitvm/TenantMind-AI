# Feature 10: Announcements Broadcast

## 1. Layman Guide
Landlords can broadcast building-wide announcements (e.g. water maintenance or parking lot cleaning) to all active tenants in a property via email and portal notifications.

---

## 2. Technical Guide
* **REST API**: Exposes the route `POST /api/announcements`.
* **Async Dispatch**: Celery queries all active leases in a property, chunks them in batches of 100, and triggers delivery tasks.
* **Real-time Push**: Pushes updates to active WebSocket connections on the client app.

---

## 3. Step-by-Step Flow
1. **Compose**: Landlord writes the announcement and selects target properties.
2. **Execute**: API registers the announcement in MongoDB and queues Celery delivery.
3. **Notify**: WebSocket pushes the notification to active tenant screens.
4. **Email**: Celery tasks send email backups.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "title": "Scheduled Power Outage",
  "content": "Power will be cut on Monday between 9AM and 12PM for generator testing.",
  "target_property_id": "ObjectId",
  "timestamp": 1783267200
}
```

---

## 5. Edge Cases & Mitigations
* **Tenant count scaling**: To prevent database lockups at scale, Celery handles email dispatch in parallel worker threads, preventing API lag.
