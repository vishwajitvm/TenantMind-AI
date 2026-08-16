import asyncio
import time
from celery import Celery
from app.config import settings
from app.database import tenant_context, get_minio_client, get_db
from app.ingestion.extractor import DocumentExtractor
from tracenest import logger

# Initialize Celery
celery_app = Celery(
    "tenantmind_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Optional Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Helper to run async code synchronously inside Celery worker
def run_async(coro):
    logger.debug(f"Entering run_async")
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

@celery_app.task(name="app.workers.tasks.process_document_task")
def process_document_task(tenant_id: str, document_id: str, bucket_name: str, minio_key: str, filename: str):
    logger.debug(f"Entering process_document_task")
    """Asynchronously processes a document: downloads from MinIO, chunks, embeds, indexes to Qdrant."""
    logger.info(f"Starting async document processing for Tenant: {tenant_id} | Document ID: {document_id}")
    tenant_context.set(tenant_id)
    
    # 1. Update status to 'processing'
    async def update_status(status: str, error_msg: str = None, metadata: dict = None):
        logger.debug(f"Entering update_status")
        db = get_db()
        update_data = {
            "status": status,
            "updated_at": time.time()
        }
        if error_msg:
            update_data["error"] = error_msg
        if metadata:
            update_data["metadata"] = metadata
            
        await db.documents.update_one(
            {"document_id": document_id},
            {"$set": update_data}
        )
        
    run_async(update_status("processing"))
    
    try:
        # 2. Get file bytes from MinIO
        minio_client = get_minio_client()
        logger.debug(f"Successfully obtained MinIO client connection. Fetching object {minio_key} from {bucket_name}.")
        try:
            response = minio_client.get_object(bucket_name, minio_key)
            logger.debug(f"Streaming data from MinIO object {minio_key} into memory...")
            file_bytes = response.read()
            logger.info(f"Successfully retrieved {len(file_bytes)} bytes from MinIO.")
        finally:
            response.close()
            response.release_conn()
            logger.debug("Closed and released MinIO network connections.")
            
        # 3. Process, chunk, embed and index
        logger.info(f"Initiating AI Document Extraction and Indexing pipeline for {filename}")
        logger.debug(f"Passing {len(file_bytes)} bytes to DocumentExtractor.extract_and_index")
        result = run_async(DocumentExtractor.extract_and_index(filename, file_bytes))
        logger.debug(f"DocumentExtractor completed. Raw result status: {result['status']}")
        
        if result["status"] == "success":
            metadata = {
                "chunks_count": result["chunks_count"],
                "secrets_detected": result["secrets_detected"],
                "injection_detected": result["injection_detected"],
                "collection_name": result["collection_name"]
            }
            run_async(update_status("processed", metadata=metadata))
            logger.info(f"Successfully processed document: {filename} for Tenant: {tenant_id}")
        else:
            run_async(update_status("failed", error_msg=result.get("reason", "Unknown extraction error")))
            logger.error(f"Failed to process document {filename}: {result.get('reason')}")
            
    except Exception as e:
        logger.error(f"Error in process_document_task for {filename}: {str(e)}", exc_info=True)
        run_async(update_status("failed", error_msg=str(e)))

@celery_app.task(name="app.workers.tasks.sync_scheduled_cleanup")
def sync_scheduled_cleanup():
    logger.debug(f"Entering sync_scheduled_cleanup")
    """Periodic task example that can be registered with Celery Beat to clean up old temp logs or stats."""
    logger.info("Executing scheduled cleanup and sync task")
    # Clean up operations or sync metrics could go here.
    return {"status": "completed"}
