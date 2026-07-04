# Feature 09: Tenant Screening & Background Check

## 1. Layman Guide
Applicants can submit their information (identity documents, background details) online to authorize credit and criminal background checks. Landlords can review results directly on the dashboard.

---

## 2. Technical Guide
* **API Integration**: Integrates with third-party background screening APIs (e.g. Checkr / TransUnion).
* **Security Controls**: Social Security Numbers (SSN) are encrypted before saving.
* **Webhook Receiver**: Webhook endpoints capture background check updates.

---

## 3. Step-by-Step Flow
1. **Consent**: Applicant inputs their details and signs the authorization form.
2. **Submit**: Backend triggers a check request to the verification API.
3. **Process**: The third-party service performs checks and returns results.
4. **Update**: Webhook updates the screening status in MongoDB to `APPROVED` or `MANUAL_REVIEW`.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "applicant_id": "string (UUID)",
  "credit_score": 720,
  "verdict": "APPROVED",
  "reports": [
    { "type": "criminal", "status": "clear" }
  ]
}
```

---

## 5. Edge Cases & Mitigations
* **Identity mismatches**: If the API returns validation errors, the system updates the status to `MANUAL_REVIEW` and notifies the landlord instead of auto-rejecting.
