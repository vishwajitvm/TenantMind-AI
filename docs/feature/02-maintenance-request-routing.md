# Feature 02: Maintenance Request Routing

## 1. Layman Guide
When a tenant submits a repair request (such as a leaking pipe or broken heater), the system automatically analyzes the text, assigns the issue to the appropriate category, and alerts a pre-matched vendor in the local area.

---

## 2. Technical Guide
* **FASTAPI Endpoint**: Receives multi-part file uploads and forms.
* **Celery Classification Pipeline**: Uses a NLP text classifier model. It evaluates the ticket's title and description to extract categories (e.g. `plumbing`, `electrical`).
* **Vendor Match Engine**: Evaluates vendor ratings, specialties, and active workloads in the properties region, auto-assigning the task to the highest-scoring match.

---

## 3. Step-by-Step Flow
1. **Submit**: Tenant describes the maintenance issue and uploads a photo.
2. **Upload**: Media uploaded to MinIO `maintenance` bucket; references saved to MongoDB.
3. **Classify**: Celery worker identifies category as `electrical`.
4. **Match**: The engine queries MongoDB for local electrical vendors and assigns the ticket.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "ticket_id": "string (UUID)",
  "category": "electrical",
  "assigned_vendor_id": "string (UUID)",
  "status": "ASSIGNED",
  "priority": "high"
}
```

---

## 5. Edge Cases & Mitigations
* **No local vendor matches**: If no electrician is available within a 20-mile radius, the ticket category falls back to a general administrator status and alerts the landlord for manual override.
