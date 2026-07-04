# Feature 03: Rent Payment Processing

## 1. Layman Guide
Tenants can review outstanding rental bills online and execute payments using credit cards or secure direct bank transfers (ACH), automatically clearing their ledger balances.

---

## 2. Technical Guide
* **API endpoints**: Exposes routes `/api/payments/pay` and `/api/payments/webhook`.
* **Idempotency checks**: The API verifies the client's `Idempotency-Key` header against Redis.
* **Integrations**: Connects to Stripe SDK for card transactions and Plaid SDK for bank accounts.

---

## 3. Step-by-Step Flow
1. **Invoice**: Invoice document generated in MongoDB by periodic beat task.
2. **Checkout**: Tenant selects a payment method and clicks "Submit".
3. **Gateway**: Request processed by Stripe; webhook emits status code updates.
4. **Ledger Posting**: The backend posts `COMPLETED` transaction status, updating user ledger tables.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "payment_id": "string (UUID)",
  "invoice_id": "string",
  "amount": 1250.00,
  "payment_status": "COMPLETED | FAILED | PENDING",
  "transaction_hash": "string"
}
```

---

## 5. Edge Cases & Mitigations
* **Card decline or ACH failure**: The system catches webhook failure notices, marks the invoice status as `FAILED`, and sends a notice to the tenant requesting alternate payment.
