# Feature 01: Tenant Onboarding

## 1. Layman Guide
The Tenant Onboarding feature allows new residents to join the TenantMind AI platform. Once the landlord invites a tenant, the resident receives an email, fills out their profile details, signs their lease online, and receives credentials to log into their dashboard.

---

## 2. Technical Guide
This feature coordinates operations across the Next.js client, Keycloak OIDC, MongoDB, and the Celery worker:
* **Frontend**: Multi-step wizard collecting personal details and file uploads (ID cards, signatures).
* **Backend REST API**: Validates inputs via Pydantic schemas, triggers background checks, uploads images to MinIO, and creates a user record in Keycloak under the `tenant` role group.
* **Celery Workers**: Initiates welcoming tasks and creates corresponding tenancy collection profiles in MongoDB.

---

## 3. Step-by-Step Flow
1. **Invite**: The landlord registers the tenant's email address on the dashboard, generating a signed invite token.
2. **Access**: The tenant clicks the token link and completes profile details.
3. **Verify**: Files are saved to the MinIO `inspections` bucket; metadata is saved in MongoDB.
4. **Credential Setup**: Keycloak registers the user with status `active` and credentials are created.

---

## 4. Data Schema
```json
{
  "_id": "ObjectId",
  "tenant_id": "string (UUID)",
  "verification_status": "VERIFIED | PENDING | REJECTED",
  "uploaded_documents": [
    {
      "type": "ID_CARD",
      "path": "inspections/tenant_id_card.pdf"
    }
  ]
}
```

---

## 5. Edge Cases & Mitigations
* **Keycloak registration fails halfway**: If the OIDC server fails to register the credentials but MongoDB profile creation succeeded, the system invokes an automatic rollback script to remove the MongoDB profile and prompt the user to re-submit.
