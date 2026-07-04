# Feature 04: Lease Document Generation

## 1. Layman Guide
Landlords can enter lease details (such as dates, rent amount, and occupant names) on their dashboard. The system compiles this information into a standardized lease agreement PDF, making it ready for online signatures.

---

## 2. Technical Guide
* **PDF rendering**: The backend merges tenant and property variables into a pre-defined LaTeX/HTML template.
* **Storage upload**: Renders output binary, uploads PDF payload directly to the MinIO `leases` bucket, and saves the file reference path in MongoDB.

---

## 3. Step-by-Step Flow
1. **Request**: Landlord fills lease variables and clicks "Generate".
2. **Retrieve**: API queries MongoDB for landlord and tenant profile details.
3. **Render**: The backend generates the PDF and uploads it to MinIO.
4. **Sign**: The system emails the tenant a secure link to view and sign the PDF.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "lease_id": "string (UUID)",
  "tenant_id": "string (UUID)",
  "minio_path": "leases/lease_uuid.pdf",
  "signature_status": "DRAFT | SIGNED | EXPIRED"
}
```

---

## 5. Edge Cases & Mitigations
* **Variable Overflow**: If fields contain long names (e.g. 100 characters), the LaTeX renderer wraps columns dynamically to prevent PDF layout breakages.
