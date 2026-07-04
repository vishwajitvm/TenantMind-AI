# 22. Disaster Recovery & Backup

This document outlines the backup policies, replication configurations, and data recovery workflows for TenantMind AI.

## 1. Backup Strategies & Cadence
To prevent loss of business data, files, and vectors:
* **MongoDB (Document Store)**:
  * **Frequency**: Automated incremental backups every 4 hours; full snapshot daily.
  * **Retention**: 30 days of snapshots.
  * **Tool**: `mongodump` automated via Celery task, zipped and stored in a cold S3 bucket.
* **MinIO (Object Vault)**:
  * **Strategy**: Multi-site active-passive bucket replication. Files written to the primary bucket are asynchronously copied to a secondary bucket.
* **Qdrant (Vector Indices)**:
  * **Strategy**: Snaps are taken daily using Qdrant’s snapshot API:
    ```http
    POST /collections/lease_documents/snapshots
    ```
    Snap files are exported to MinIO.

---

## 2. Recovery Protocols
In the event of an outage or data corruption:
1. **Target RPO (Recovery Point Objective)**: 4 hours (maximum data loss window).
2. **Target RTO (Recovery Time Objective)**: 1 hour (maximum offline system window).
3. **Database Restore Command**:
   ```bash
   mongorestore --uri="mongodb://root:password@mongodb:27017" --archive=/path/to/backup.archive --gzip
   ```
4. **Vector Collection Restore**: Download snapshot from S3 and call:
   ```http
   POST /collections/lease_documents/snapshots/recover
   ```
5. **DNS Failover**: AWS Route 53 health checks trigger DNS rerouting to the secondary region if the primary site is unresponsive.
