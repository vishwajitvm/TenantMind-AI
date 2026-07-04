# Feature 07: Automated Rent Reminders

## 1. Layman Guide
The system monitors upcoming rent deadlines and automatically sends email/SMS reminders to tenants with unpaid invoices, helping prevent late fees.

---

## 2. Technical Guide
* **Scheduler**: Celery Beat schedules task runs daily at 08:00 AM UTC.
* **Database Query**: Queries the MongoDB `leases` and `payments` collections to identify active contracts without matching payments for the current month.
* **Notification Dispatch**: Dispatches template parameters to the Email/SMS provider.

---

## 3. Step-by-Step Flow
1. **Trigger**: Celery Beat launches the daily check.
2. **Identify**: Queries MongoDB for accounts with outstanding rent due.
3. **Dispatch**: Generates email payloads and schedules sending tasks.
4. **Log**: Records the reminder event in MongoDB.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "reminder_id": "string (UUID)",
  "tenant_id": "string (UUID)",
  "lease_id": "ObjectId",
  "due_date": "string (YYYY-MM-DD)",
  "sent_timestamp": "double"
}
```

---

## 5. Edge Cases & Mitigations
* **Reminder sent after payment**: To prevent sending reminders to users who paid moments before the run, the Celery task re-verifies invoice states immediately before sending the message.
