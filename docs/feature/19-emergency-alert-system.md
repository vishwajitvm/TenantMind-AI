# Feature 19: Emergency Alert System

## 1. Layman Guide
Landlords can broadcast urgent safety alerts (e.g. fire hazard or severe weather warnings) to all tenants immediately via SMS, email, and portal notifications.

---

## 2. Technical Guide
* **High Priority Queue**: Uses a separate high-priority Celery task queue to bypass standard tasks.
* **Integrations**: Integrates with Twilio for immediate SMS delivery.

---

## 3. Step-by-Step Flow
1. **Trigger**: Landlord posts a critical safety alert.
2. **Prioritize**: The API places the task in the high-priority queue.
3. **Broadcast**: Celery triggers SMS delivery via Twilio.
4. **Push**: WebSockets display the alert overlay on active tenant screens.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "alert_level": "CRITICAL",
  "message": "Immediate evacuation ordered due to water main leak.",
  "timestamp": 1783267200
}
```

---

## 5. Edge Cases & Mitigations
* **SMS carrier failure**: If Twilio returns errors, the system logs the issue and falls back to push notifications and email to ensure delivery.
