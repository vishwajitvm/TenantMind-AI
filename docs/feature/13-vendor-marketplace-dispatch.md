# Feature 13: Vendor Marketplace & Dispatch

## 1. Layman Guide
When a repair ticket is created, the system matches the job with local vendors, sends an invite, and assigns the task to the vendor who accepts it first.

---

## 2. Technical Guide
* **Matching**: Filters vendors by category and active work order limits.
* **Locking**: Implements atomic database checks to prevent multiple vendors from accepting the same work order.

---

## 3. Step-by-Step Flow
1. **Invite**: The matching engine sends invitations to target vendors.
2. **Accept**: A vendor accepts the job via the portal.
3. **Lock**: Backend runs atomic checks to assign the vendor.
4. **Notify**: Confirms the assignment and updates the ticket status.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "ticket_id": "string (UUID)",
  "vendor_id": "string (UUID)",
  "status": "ASSIGNED",
  "dispatch_time": 1783267200
}
```

---

## 5. Edge Cases & Mitigations
* **Assignment race condition**: If two vendors accept the job simultaneously, the system uses atomic database updates to assign the job to the first transaction, notifying the second vendor that the job is no longer available.
