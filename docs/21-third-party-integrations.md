# 21. Third-Party Integrations

This manual outlines the interfaces, APIs, and configurations used for TenantMind AI external service hook-ups.

## 1. Stripe & Plaid Payment Integration
For commercial invoicing and tenant ledger collection:
* **Stripe SDK**: Processes card payments. Transactions emit webhooks caught by the FastAPI webhook receiver `/api/payments/webhook`.
* **Plaid Link**: Securely connects tenant checking accounts for ACH transfers. Authenticates routing details before invoking Stripe ACH processors.

---

## 2. Notification Gateways
* **Twilio (SMS)**: Used for dispatching emergency announcements and maintenance arrival warnings. Uses JSON payload mappings inside Celery tasks.
* **SendGrid / SMTP**: Sends tenant welcome emails, rent reminders, and ledger invoices.

---

## 3. Screening & Background Checks (Checkr)
* **API Flow**: The onboarding step sends applicant credentials (encrypted SSN, DOB, name) to Checkr.
* **Callback Hook**: Checkr notifies the backend upon report finalization. The system pulls credit ratings and criminal clearances, updating MongoDB.
