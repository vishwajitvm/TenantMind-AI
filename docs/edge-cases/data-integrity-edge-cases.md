# Data Integrity Edge Cases

Handling unexpected schema and data updates.

## Interrupted Multi-Part MinIO upload
- **Scenario**: User uploads 50MB maintenance video, connection breaks.
- **Mitigation**: Celery cron sweeps incomplete MinIO uploads weekly.

## MongoDB / Keycloak Sync
- **Scenario**: MongoDB write fails but Keycloak user created.
- **Mitigation**: Two-phase registration process with compensation logic.
