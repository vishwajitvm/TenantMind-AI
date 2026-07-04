# 10. Background Jobs & Queues

TenantMind AI uses **Celery** as its asynchronous task processor and **Redis** as the message broker to handle non-blocking workloads.

## 1. Broker & Worker Configuration
* **Broker**: Redis running on port `6379`.
* **Worker Execution**: Initialized with:
  ```bash
  celery -A app.workers.tasks worker --loglevel=info
  ```
* **Task Scheduler (Celery Beat)**: Initialized with:
  ```bash
  celery -A app.workers.tasks beat --loglevel=info
  ```

---

## 2. Core Asynchronous Tasks

### A. Document Parsing & Indexing (`process_lease_document`)
* **Trigger**: Triggered via `POST /api/documents/upload`.
* **Operations**: Downloads the raw PDF from MinIO, extracts textual data, chunks it, calls the Embedding Gateway, and saves the vectors to Qdrant.

### B. Automatic Rent Reminders (`send_rent_reminders`)
* **Trigger**: Automated schedule by Celery Beat every calendar day at 08:00 AM UTC.
* **Operations**: Queries MongoDB for active leases where rent is unpaid and due within 3 days, then triggers emails to tenants.

### C. Maintenance Dispatch Notification (`notify_vendor_assignment`)
* **Trigger**: Triggered when a ticket is assigned to a vendor.
* **Operations**: Sends email/SMS containing task descriptions and property directions to the assigned vendor.
