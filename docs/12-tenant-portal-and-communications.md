# 12. Tenant Portal & Communications

The Tenant Portal is the primary web application interface for residents, designed to streamline communication and payments.

## 1. Chat Assistant interface
* **Interactive AI Console**: Tenants can chat with an assistant powered by the backend RAG pipeline.
* **Instant Lease Lookup**: Queries like *"Can I drill holes in walls?"* retrieve the corresponding lease clause automatically.
* **Action Starters**: If a tenant describes an issue (e.g., *"My faucet is leaking"*), the AI assistant offers to automatically pre-fill a maintenance ticket.

---

## 2. Maintenance Logging & Rent Panel
* **Ticket Submission**: Tenants file tickets with a title, description, category selector, and drag-and-drop image uploader.
* **Live Notifications**: A persistent WebSocket channel updates the tenant's UI instantly when a landlord or vendor changes a ticket status from `OPEN` to `ASSIGNED` or `RESOLVED`.
* **Billing & Ledger**: Displays rent invoices. Tenants can make payments via mock card/ACH fields which trigger ledger operations on the backend.
