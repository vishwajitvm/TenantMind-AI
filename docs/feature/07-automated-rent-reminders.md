# Feature 07: Automated Rent Reminders

## Layman Guide
Sends email and text notifications when rent is due.

## Technical Guide
Celery Beat cron runs every morning. Queries MongoDB for unpaid invoices, triggers email dispatch via worker.

## Flow
1. Trigger cron.
2. Fetch unpaid invoices.
3. Dispatch reminder jobs to Celery.

## Data Schema
```json
{
  "reminder_id": "uuid",
  "sent_to": "email",
  "status": "SENT"
}
```

## Edge Cases
- **Reminder sent to paid tenants**: Ensure double check state check immediately prior to triggering delivery API.
