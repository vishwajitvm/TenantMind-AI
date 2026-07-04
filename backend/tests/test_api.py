import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from app.main import app
from app.database import get_db, get_minio_client, get_qdrant_client

client = TestClient(app)

@pytest.mark.asyncio
async def test_health_endpoint(mock_mongo, mock_qdrant, mock_minio):
    # Mocking system dependencies
    with patch("app.api.health.get_db", return_value=mock_mongo[1]), \
         patch("app.api.health.get_qdrant_client", return_value=mock_qdrant), \
         patch("app.api.health.get_minio_client", return_value=mock_minio):
         
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["services"]["mongodb"] == "connected"
        assert data["services"]["qdrant"] == "connected"
        assert data["services"]["minio"] == "connected"

def test_models_endpoint():
    resp = client.get("/models")
    assert resp.status_code == 200
    data = resp.json()
    assert "llms" in data
    assert "embedding_models" in data
    assert any(m["provider"] == "Ollama" for m in data["llms"])

@pytest.mark.asyncio
async def test_audit_logs_endpoint(mock_mongo):
    _, db = mock_mongo
    with patch("app.api.audit_logs.get_db", return_value=db):
        resp = client.get("/audit-logs", headers={"X-Tenant-ID": "acme"})
        assert resp.status_code == 200
        data = resp.json()
        assert "logs" in data
        assert data["total"] == 1

@pytest.mark.asyncio
async def test_approvals_endpoints(mock_mongo):
    _, db = mock_mongo
    
    class MockCursor:
        def __init__(self, items):
            self.items = items
        def sort(self, *args, **kwargs):
            return self
        def __aiter__(self):
            return self
        async def __anext__(self):
            if not self.items:
                raise StopAsyncIteration
            return self.items.pop(0)
            
    db.mcp_approvals.find.return_value = MockCursor([{
        "_id": "mock_id",
        "approval_id": "app-123",
        "tenant_id": "acme",
        "tool_name": "run_cmd",
        "arguments": {},
        "risk_level": "high",
        "status": "pending",
        "created_at": 12345.0
    }])
    db.mcp_approvals.find_one.return_value = {
        "approval_id": "app-123",
        "tenant_id": "acme",
        "tool_name": "run_cmd",
        "arguments": {},
        "risk_level": "high",
        "status": "pending",
        "created_at": 12345.0
    }
    
    with patch("app.api.approvals.get_db", return_value=db):
        # 1. Get approvals
        resp = client.get("/approvals", headers={"X-Tenant-ID": "acme"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["approval_id"] == "app-123"

        # 2. Approve action
        action_resp = client.post(
            "/approvals/app-123/action",
            headers={"X-Tenant-ID": "acme"},
            json={"action": "approve", "reviewed_by": "tester"}
        )
        assert action_resp.status_code == 200
        action_data = action_resp.json()
        assert action_data["status"] == "executed"
        assert db.mcp_approvals.update_one.called

@pytest.mark.asyncio
async def test_document_upload_endpoint(mock_mongo, mock_minio):
    _, db = mock_mongo
    
    with patch("app.api.documents.get_db", return_value=db), \
         patch("app.api.documents.get_minio_client", return_value=mock_minio), \
         patch("app.api.documents.ensure_minio_bucket", return_value="org-acme-bucket"), \
         patch("app.api.documents.process_document_task.delay") as mock_celery:
         
        # Simulate upload
        files = {"file": ("test.txt", b"Hello, this is my test file content.", "text/plain")}
        resp = client.post(
            "/documents/upload",
            headers={"X-Tenant-ID": "acme"},
            files=files
        )
        
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "pending"
        assert data["filename"] == "test.txt"
        assert mock_minio.put_object.called
        assert db.documents.insert_one.called
        assert mock_celery.called

@pytest.mark.asyncio
async def test_chat_interaction_endpoint(mock_mongo, mock_qdrant):
    _, db = mock_mongo
    
    with patch("app.api.chats.get_db", return_value=db), \
         patch("app.api.chats.get_qdrant_client", return_value=mock_qdrant):
         
        # Test basic chat (runs multi-model fallback to MockFallback)
        payload = {
            "messages": [
                {"role": "user", "content": "Tell me about my server configuration."}
            ],
            "use_rag": True
        }
        
        resp = client.post(
            "/chats",
            headers={"X-Tenant-ID": "acme"},
            json=payload
        )
        
        assert resp.status_code == 200
        data = resp.json()
        assert "response" in data
        assert data["provider"] == "MockFallback"
        assert db.chats.insert_one.called

@pytest.mark.asyncio
async def test_chat_interaction_mcp_tool_invocation(mock_mongo):
    _, db = mock_mongo
    
    with patch("app.api.chats.get_db", return_value=db), \
         patch("app.gateways.mcp_gateway.get_db", return_value=db):
        # Trigger an MCP tool call format
        payload = {
            "messages": [
                {"role": "user", "content": "run_tool: read_file arguments: {\"path\": \".env\"}"}
            ],
            "use_rag": False
        }
        
        resp = client.post(
            "/chats",
            headers={"X-Tenant-ID": "acme"},
            json=payload
        )
        
        assert resp.status_code == 200
        data = resp.json()
        assert "mcp_verification" in data
        assert data["mcp_verification"]["risk_level"] == "medium"
        assert data["mcp_verification"]["status"] == "pending"
        assert db.mcp_approvals.insert_one.called
