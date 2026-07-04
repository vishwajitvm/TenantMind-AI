# 11. Object Storage & File Management

All unstructured files (PDF agreements, images of plumbing damages, inspection videos) are managed in **MinIO**, which provides an S3-compatible API.

## 1. Storage Buckets configuration
TenantMind AI divides file management into three distinct buckets:
1. `leases`: Holds tenant lease agreements (restricted to landlords and corresponding tenants).
2. `maintenance`: Holds media attachments for repair claims (public-read endpoints or short-term pre-signed links for vendors).
3. `inspections`: Stores inventory check sheets and checklist images.

---

## 2. File Ingestion Flow & Security

To prevent public exposure of lease files:
1. **Pre-signed URL Pattern**: The frontend requests an upload URL from the backend. The backend signs a transaction and returns an ephemeral link.
2. **Direct Upload**: The client pushes the binary payload directly to MinIO.
3. **Link Resolution**: When accessing files, the backend verifies the user's OIDC roles, fetches the S3 object reference, and generates a pre-signed download URL valid for 15 minutes.
