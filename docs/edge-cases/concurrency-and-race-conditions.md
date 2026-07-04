# Concurrency & Race Conditions

This document outlines configurations designed to mitigate race conditions.

## 1. Double Payment Clicking
* **Scenario**: A tenant clicks the "Pay Rent" button repeatedly when their connection is slow, sending 3 requests to Stripe simultaneously.
* **Mitigation**:
  * The React frontend disables the submission button immediately after the initial click.
  * The FastAPI backend requires an `Idempotency-Key` header. When a request starts, the key is saved in Redis with a 2-minute TTL. Subsequent requests with the same key are blocked with a `409 Conflict` response.

## 2. Maintenance Work Order Double Assignment
* **Scenario**: Two plumbers click "Accept Job" on the landlord portal at the exact same millisecond.
* **Mitigation**:
  * Backend uses MongoDB atomic update validation. Instead of fetching the ticket, checking its status, and updating, it executes the write operation in one step:
    ```python
    result = await db.maintenance_tickets.update_one(
        { "_id": ticket_id, "status": "OPEN" },
        { "$set": { "status": "ASSIGNED", "vendor_id": vendor_id } }
    )
    ```
    If another request already updated the status to `ASSIGNED`, the query fails to find a document matching `{ "status": "OPEN" }`, and `result.modified_count` will return `0`. The API then returns a clear error message.
