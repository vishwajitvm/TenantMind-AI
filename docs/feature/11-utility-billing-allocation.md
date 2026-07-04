# Feature 11: Utility Billing Allocation

## 1. Layman Guide
The system splits shared building utility bills (such as water or trash collection) among tenants based on occupancy metrics or apartment size, posting details directly to tenant payment ledgers.

---

## 2. Technical Guide
* **Worker Execution**: Celery tasks run formulas to split utility bills based on occupancy data.
* **Database Updates**: Writes invoices to the MongoDB `payments` collection and updates corresponding lease ledgers.

---

## 3. Step-by-Step Flow
1. **Upload**: Landlord enters the master utility bill amount.
2. **Calculate**: Celery splits the bill based on property square footage.
3. **Bill**: Post individual invoices to MongoDB.
4. **Notify**: Email alerts notify tenants of their new bill balance.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "utility_type": "water",
  "total_bill": 800.00,
  "tenant_allocations": [
    { "tenant_id": "tenant-uuid-1", "amount": 80.00 }
  ],
  "billing_period": "2026-06"
}
```

---

## 5. Edge Cases & Mitigations
* **Unoccupied units**: The allocation script assigns unoccupied unit costs to the landlord profile to prevent overcharging active tenants.
