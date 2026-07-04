# Data Integrity Edge Cases

This document describes edge cases related to storage integrity and synchronization.

## 1. Interrupted Multi-Part Uploads
* **Scenario**: A tenant uploads a 50MB maintenance video reporting damage, but their internet drops at 80% completion.
* **Mitigation**:
  * MinIO bucket is configured with a lifecycle rule that sweeps incomplete multi-part uploads older than 7 days, freeing disk space.
  * The frontend client supports upload retries and tracks chunk status using localStorage hashes.

## 2. Keycloak and MongoDB Out-of-Sync States
* **Scenario**: The system creates a user profile in Keycloak, but MongoDB fails to save the corresponding profile record due to database unavailability.
* **Mitigation**:
  * The registration router uses a try-except structure. If the MongoDB insert fails, the backend fires an administrative deletion call to the Keycloak API to remove the tenant's auth account before raising the HTTP 500 error.
  * A periodic Celery reconciliation script checks Keycloak users against MongoDB collections, flagging orphaned users for review.
