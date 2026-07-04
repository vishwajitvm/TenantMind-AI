import uuid
import time
from typing import Dict, Any, Tuple
from app.database import get_db
from tracenest import logger

class MCPGateway:
    @staticmethod
    def classify_risk(tool_name: str, arguments: Dict[str, Any]) -> str:
        """Classifies risk level of an MCP tool call as: low, medium, high, or critical."""
        tool_name_lower = tool_name.lower()
        args_str = str(arguments).lower()
        
        # 1. Critical risk indicators
        critical_keywords = [
            "rm -rf", "drop database", "drop_database", "drop table", "drop_table", 
            "format ", "eval(", "exec(", "subprocess.run", "shutil.rmtree", "os.system",
            "chmod", "chown", "wipe"
        ]
        if any(kw in args_str for kw in critical_keywords) or "execute_system_command" in tool_name_lower:
            return "critical"
            
        # 2. High risk indicators
        high_keywords = [
            "delete", "write", "overwrite", "update", "modify", "install", "send_email",
            "update_credentials", "change_password", "env_variables", "secret"
        ]
        if any(kw in tool_name_lower or kw in args_str for kw in high_keywords):
            return "high"
            
        # 3. Medium risk indicators
        medium_keywords = [
            "read_file", "view_file", "list_directory", "inspect", "get_logs",
            "query_db", "fetch_records"
        ]
        if any(kw in tool_name_lower or kw in args_str for kw in medium_keywords):
            return "medium"
            
        # 4. Default to Low risk
        return "low"

    @classmethod
    async def process_tool_call(
        cls, 
        tenant_id: str, 
        tool_name: str, 
        arguments: Dict[str, Any], 
        requested_by: str = "system"
    ) -> Dict[str, Any]:
        """Classifies a tool call and routes it to either auto-approval or the approval workflow."""
        risk_level = cls.classify_risk(tool_name, arguments)
        
        # Low risk is immediately approved
        if risk_level == "low":
            status = "approved"
            approval_id = str(uuid.uuid4())
            logger.info(f"MCP Tool Auto-Approved | Tenant: {tenant_id} | Tool: {tool_name} | Risk: low")
        else:
            status = "pending"
            approval_id = str(uuid.uuid4())
            logger.warn(f"MCP Tool Requires Approval | Tenant: {tenant_id} | Tool: {tool_name} | Risk: {risk_level}")
            
        approval_doc = {
            "approval_id": approval_id,
            "tenant_id": tenant_id,
            "tool_name": tool_name,
            "arguments": arguments,
            "risk_level": risk_level,
            "status": status,
            "requested_by": requested_by,
            "created_at": time.time(),
            "updated_at": time.time(),
            "reviewed_by": None,
            "action_result": None
        }
        
        # Save to database
        db = get_db()
        await db.mcp_approvals.insert_one(approval_doc)
        
        return {
            "approval_id": approval_id,
            "risk_level": risk_level,
            "status": status,
            "requires_approval": risk_level != "low"
        }
