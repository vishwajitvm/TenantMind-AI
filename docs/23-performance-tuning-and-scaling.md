# 23. Performance Tuning & Scaling

This guide covers performance tuning strategies to maintain sub-second response times as tenant and document counts scale.

## 1. Database Indexing & Optimizations
* **MongoDB Indexes**: Ensure fast query performance under multi-tenant workloads:
  * Compound index `{ tenant_id: 1, created_at: -1 }` on `maintenance_tickets` and `payments`.
  * Index on `keycloak_id` in `users` collection.
* **Qdrant Vector Payload Indexes**:
  * Create a payload index on `tenant_id` within the `lease_documents` collection. This allows Qdrant to filter out irrelevant tenant documents *before* calculating cosine similarities, reducing vector search overhead.

---

## 2. Queue Tuning & Caching
* **Redis Caching**: Cache common endpoints (like property details or landlord dashboard financial summaries) using standard Redis key-value storage with an eviction policy of `volatile-lru` and a 5-minute TTL.
* **Celery Worker Prefork**: Set worker prefetch limits:
  ```bash
  celery -A app.workers.tasks worker -c 4 --prefetch-multiplier=1
  ```
  This ensures that long-running PDF OCR and text embedding tasks do not block fast notification dispatches or email reminders.
