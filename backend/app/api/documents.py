from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.database import get_db, get_tenant_slug, get_minio_client, ensure_minio_bucket
from app.workers.tasks import process_document_task
import uuid
import time
import io
from typing import List, Dict, Any
from tracenest import logger

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    logger.debug(f"Entering upload_document")
    slug = get_tenant_slug()
    logger.debug(f"Initiated document upload for tenant: {slug}")
    
    if not file.filename.endswith(('.pdf', '.txt', '.md', '.docx')):
        logger.warning(f"Tenant {slug} attempted to upload unsupported file format: {file.filename}")
        raise HTTPException(status_code=400, detail="Unsupported file format")
    logger.info(f"File validation passed. Filename: {file.filename}, Type: {file.content_type}")
        
    db = get_db()
    minio_client = get_minio_client()
    logger.debug("Successfully acquired MongoDB and MinIO connections.")
    
    bucket_name = f"org-{slug}-docs".lower()
    logger.debug(f"Target MinIO bucket for upload: {bucket_name}")
    
    # Ensure bucket exists
    try:
        logger.debug(f"Verifying existence of bucket: {bucket_name}")
        if not minio_client.bucket_exists(bucket_name):
            logger.info(f"Bucket {bucket_name} does not exist. Attempting creation...")
            minio_client.make_bucket(bucket_name)
            logger.info(f"Successfully created MinIO bucket: {bucket_name}")
    except Exception as e:
        logger.error(f"MinIO bucket verification/creation failed for {bucket_name}. Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Storage configuration error")
        
    logger.debug(f"Attempting to read file payload into memory: {file.filename}")
    file_content = await file.read()
    file_size = len(file_content)
    logger.info(f"File read complete. Size: {file_size} bytes.")
    
    document_id = str(uuid.uuid4())
    minio_key = f"{document_id}/{file.filename}"
    logger.debug(f"Generated UUID for document: {document_id}. MinIO Object Key: {minio_key}")
    
    try:
        logger.info(f"Executing MinIO put_object for {minio_key}...")
        minio_client.put_object(
            bucket_name,
            minio_key,
            io.BytesIO(file_content),
            length=file_size,
            content_type=file.content_type
        )
        logger.info("MinIO object upload succeeded.")
    except Exception as e:
        logger.error(f"Failed to upload document payload to MinIO for {slug}. Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to upload file")
        
    # Save to MongoDB
    logger.debug(f"Persisting document metadata to MongoDB for {document_id}...")
    doc_record = {
        "document_id": document_id,
        "tenant_id": slug,
        "filename": file.filename,
        "status": "pending_ingestion",
        "minio_bucket": bucket_name,
        "minio_key": minio_key,
        "uploaded_at": datetime.datetime.utcnow()
    }
    await db.documents.insert_one(doc_record)
    logger.debug("MongoDB persistence completed.")

    # Dispatch celery task
    logger.info(f"Dispatching async Celery extraction task for {document_id}...")
    try:
        process_document_task.delay(
            tenant_id=slug,
            document_id=document_id,
            bucket_name=bucket_name,
            minio_key=minio_key,
            filename=file.filename
        )
        logger.info("Celery task dispatched successfully.")
    except Exception as e:
        logger.warning(f"Celery queue not available, could not dispatch task. Error: {str(e)}")
        
    return {
        "document_id": document_id,
        "status": "pending",
        "filename": file.filename
    }

@router.get("")
async def list_documents():
    logger.debug(f"Entering list_documents")
    """Lists all uploaded documents for the current tenant."""
    slug = get_tenant_slug()
    db = get_db()
    
    cursor = db.documents.find({"tenant_id": slug}).sort("created_at", -1)
    documents = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        documents.append(doc)
        
    return documents

@router.get("/{document_id}")
async def get_document_status(document_id: str):
    logger.debug(f"Entering get_document_status")
    """Gets processing status and security scanning metadata for a document."""
    slug = get_tenant_slug()
    db = get_db()
    
    doc = await db.documents.find_one({"document_id": document_id, "tenant_id": slug})
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
        
    doc["_id"] = str(doc["_id"])
    return doc
