# 10. Object Storage & File Management

MinIO provides S3-compatible object storage.

## Buckets
- `leases/`: Stores signed PDF agreements.
- `inspections/`: Photos and inspection checklists.
- `maintenance/`: Evidence images for maintenance requests.

All uploads are routed through backend pre-signed URL generator or direct API streaming.
