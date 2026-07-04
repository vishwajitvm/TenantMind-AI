# Feature 20: Integration Webhooks

## 1. Layman Guide
Enables external software platforms (such as landlord accounting tools or calendars) to subscribe to events in TenantMind AI, syncing data automatically.

---

## 2. Technical Guide
* **Signing**: Webhook requests are signed using a SHA256 HMAC signature in the `X-TenantMind-Signature` header.
* **Delivery**: Celery handles webhook deliveries, scheduling retries with exponential backoff on failure.

---

## 3. Step-by-Step Flow
1. **Trigger**: An event occurs in the system (e.g. `PAYMENT_COMPLETED`).
2. **Build**: Webhook generator builds a JSON payload and signs it.
3. **Send**: Post payload to registered subscriber URLs.
4. **Retry**: If the delivery fails, the system retries with exponential backoff.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "webhook_url": "https://external-accounting.com/hooks",
  "secret_key": "hmac-secret-hash",
  "subscribed_events": ["PAYMENT_COMPLETED"]
}
```

---

## 5. Edge Cases & Mitigations
* **Slow subscriber servers**: Requests timeout after 5 seconds to prevent slow external servers from blocking internal queues. Failed deliveries are marked for retry.
