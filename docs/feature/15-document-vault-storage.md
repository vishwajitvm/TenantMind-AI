# Feature 15: Document Vault Storage

## 1. Layman Guide
A secure digital filing cabinet where tenants and landlords can store and access leases, utility receipts, renter's insurance policies, and identity verifications.

---

## 2. Technical Guide
* **Asset Storage**: Uploaded files are stored in MinIO.
* **Security Controls**: Access is restricted using backend middleware validation of Keycloak OIDC user scopes.
* **Link Generation**: Generates temporary pre-signed download URLs valid for 15 minutes.

---

## 3. Step-by-Step Flow
1. **Upload**: User drags a document into the Vault UI.
2. **Transfer**: The frontend requests a pre-signed upload URL and uploads the file to MinIO.
3. **Index**: The backend saves the document metadata in MongoDB.
4. **Access**: When a user clicks to view a document, the API verifies authorization and generates a temporary view link.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "document_id": "string (UUID)",
  "owner_id": "string (UUID)",
  "filename": "renters_insurance.pdf",
  "minio_path": "leases/renters_insurance.pdf",
  "uploaded_at": 1783267200
}
```

---

## 5. Edge Cases & Mitigations
* **Expired token downloads**: Direct URLs to MinIO objects are blocked. Users must request temporary pre-signed URLs, which are only generated after verifying active OIDC tokens.
