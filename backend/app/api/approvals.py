from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel
from app.database import get_db, get_tenant_slug
from typing import Optional, List
import time

router = APIRouter(prefix="/approvals", tags=["Approvals"])

class ApprovalActionRequest(BaseModel):
    action: str  # "approve" or "reject"
    reviewed_by: str = "admin"

@router.get("")
async def list_approvals(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by approval status: pending, approved, rejected, executed")
):
    """Lists tool call approval requests for the current tenant."""
    slug = get_tenant_slug()
    db = get_db()
    
    query = {"tenant_id": slug}
    if status_filter:
        query["status"] = status_filter
        
    cursor = db.mcp_approvals.find(query).sort("created_at", -1)
    approvals = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        approvals.append(doc)
        
    return approvals

@router.post("/{approval_id}/action")
async def review_approval(approval_id: str, payload: ApprovalActionRequest):
    """Approves or rejects a pending tool call request."""
    slug = get_tenant_slug()
    db = get_db()
    
    approval = await db.mcp_approvals.find_one({"approval_id": approval_id, "tenant_id": slug})
    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Approval request not found"
        )
        
    if approval["status"] != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update approval status. Current status is '{approval['status']}'."
        )
        
    action_lower = payload.action.lower()
    if action_lower not in ["approve", "reject"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Action must be either 'approve' or 'reject'"
        )
        
    new_status = "approved" if action_lower == "approve" else "rejected"
    
    # If approved, simulate execution and transition status to executed
    action_result = None
    if new_status == "approved":
        new_status = "executed"
        # Simulate command output
        action_result = f"Command/Tool '{approval['tool_name']}' executed successfully. Status code: 0."
        
    await db.mcp_approvals.update_one(
        {"approval_id": approval_id, "tenant_id": slug},
        {
            "$set": {
                "status": new_status,
                "reviewed_by": payload.reviewed_by,
                "updated_at": time.time(),
                "action_result": action_result
            }
        }
    )
    
    return {
        "approval_id": approval_id,
        "status": new_status,
        "action_result": action_result
    }

@router.post("/{approval_id}/approve")
async def approve_approval(approval_id: str, reviewed_by: str = "admin"):
    """Approves a pending tool call request."""
    return await review_approval(approval_id, ApprovalActionRequest(action="approve", reviewed_by=reviewed_by))

@router.post("/{approval_id}/reject")
async def reject_approval(approval_id: str, reviewed_by: str = "admin"):
    """Rejects a pending tool call request."""
    return await review_approval(approval_id, ApprovalActionRequest(action="reject", reviewed_by=reviewed_by))

