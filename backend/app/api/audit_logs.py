from fastapi import APIRouter, Query
from app.database import get_db, get_tenant_slug
from typing import Optional, List, Dict, Any

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])

@router.get("")
async def get_audit_logs(
    provider: Optional[str] = Query(None, description="Filter by LLM provider"),
    status: Optional[str] = Query(None, description="Filter by status (success/failure)"),
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    """Retrieves audit and metrics logs of LLM attempts for the current tenant."""
    slug = get_tenant_slug()
    db = get_db()
    
    query: Dict[str, Any] = {"tenant_id": slug}
    
    if provider:
        query["provider"] = provider
    if status:
        query["status"] = status
        
    cursor = db.llm_metrics.find(query).sort("timestamp", -1).skip(skip).limit(limit)
    logs = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        logs.append(doc)
        
    total = await db.llm_metrics.count_documents(query)
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "logs": logs
    }
