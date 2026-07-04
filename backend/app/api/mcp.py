from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.database import get_tenant_slug
from app.gateways.mcp_gateway import MCPGateway
from typing import Dict, Any, Optional

router = APIRouter(prefix="/mcp", tags=["MCP"])

class ToolExecuteRequest(BaseModel):
    tool_name: str
    arguments: Optional[Dict[str, Any]] = {}
    requested_by: Optional[str] = "admin"

@router.get("/tools")
async def list_tools():
    """Lists registered MCP tools and their risk classifications."""
    return [
        {"name": "document_read", "risk_level": "low", "description": "Read document content"},
        {"name": "document_update_proposal", "risk_level": "medium", "description": "Propose changes to a document"},
        {"name": "filesystem_readonly", "risk_level": "low", "description": "Read local filesystem configuration"},
        {"name": "mongodb_readonly", "risk_level": "low", "description": "Read platform database metrics"},
        {"name": "github_readonly", "risk_level": "low", "description": "Read GitHub issues and PR status"},
        {"name": "email_draft", "risk_level": "medium", "description": "Draft response email"},
        {"name": "web_fetch", "risk_level": "low", "description": "Fetch documentation content"},
        {"name": "knowledge_search", "risk_level": "low", "description": "Search tenant vector embeddings"}
    ]

@router.post("/execute")
async def execute_tool(payload: ToolExecuteRequest):
    """Executes a tool call, routing through the MCP Risk Engine and approvals workflow."""
    slug = get_tenant_slug()
    
    result = await MCPGateway.process_tool_call(
        tenant_id=slug,
        tool_name=payload.tool_name,
        arguments=payload.arguments,
        requested_by=payload.requested_by
    )
    
    if result["status"] == "pending":
        return {
            "status": "pending",
            "approval_id": result.get("approval_id"),
            "risk_level": result["risk_level"],
            "detail": f"Tool execution staged for approval. Action ID: {result.get('approval_id')}"
        }
        
    return {
        "status": "executed",
        "result": result.get("output")
    }
