from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.database import get_db, get_tenant_slug, get_minio_client, ensure_minio_bucket
from app.workers.tasks import process_document_task
import uuid
import time
import io
from typing import List, Dict, Any

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Uploads a document to MinIO and queues it for Celery processing."""
    slug = get_tenant_slug()
    db = get_db()
    
    # 1. Read file bytes
    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not read upload file: {str(e)}"
        )
        
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )
        
    # 2. Upload to MinIO
    try:
        bucket_name = ensure_minio_bucket()
        minio_key = f"docs/{uuid.uuid4()}_{file.filename}"
        
        minio_client = get_minio_client()
        minio_client.put_object(
            bucket_name=bucket_name,
            object_name=minio_key,
            data=io.BytesIO(file_bytes),
            length=len(file_bytes),
            content_type=file.content_type or "application/octet-stream"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document to storage: {str(e)}"
        )
        
    # 3. Create document record in MongoDB
    document_id = str(uuid.uuid4())
    doc_record = {
        "document_id": document_id,
        "tenant_id": slug,
        "filename": file.filename,
        "bucket_name": bucket_name,
        "minio_key": minio_key,
        "status": "pending",
        "error": None,
        "metadata": None,
        "created_at": time.time(),
        "updated_at": time.time()
    }
    
    await db.documents.insert_one(doc_record)
    
    # 4. Trigger Celery Task
    # Note: Use task.delay or task.apply_async. For testing when Redis isn't running,
    # we can use try-except to fallback, or let it queue.
    try:
        process_document_task.delay(
            tenant_id=slug,
            document_id=document_id,
            bucket_name=bucket_name,
            minio_key=minio_key,
            filename=file.filename
        )
    except Exception as e:
        # In testing without redis, we can process it synchronously or log the warning
        # Let's log it
        from tracenest import logger
        logger.warning(f"Celery queue not available, could not dispatch task. Error: {str(e)}")
        
    return {
        "document_id": document_id,
        "status": "pending",
        "filename": file.filename
    }

@router.get("")
async def list_documents():
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
