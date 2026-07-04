import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.gateways.model_gateway import ModelGateway
from app.gateways.embedding_gateway import EmbeddingGateway
from app.gateways.mcp_gateway import MCPGateway

@pytest.mark.asyncio
async def test_model_gateway_fallback(mock_mongo):
    client, db = mock_mongo
    with patch("app.gateways.model_gateway.get_db", return_value=db):
        # We don't configure any keys, so the chain should fall back to mock
        messages = [{"role": "user", "content": "hello"}]
        resp = await ModelGateway.generate(messages, tenant_id="test_tenant")
        
        assert resp["provider"] == "MockFallback"
        assert "hello" in resp["content"]
        assert resp["latency"] > 0
        assert db.llm_metrics.insert_one.called

def test_embedding_gateway_dimensions():
    assert EmbeddingGateway.get_dimension("all-MiniLM-L6-v2") == 384
    assert EmbeddingGateway.get_dimension("text-embedding-3-small") == 1536
    assert EmbeddingGateway.get_dimension("text-embedding-3-large") == 3072
    assert EmbeddingGateway.get_dimension("unknown-model") == 384

def test_embedding_gateway_generation():
    # Test fallback vector generation
    text = "test query"
    vector = EmbeddingGateway.get_embedding(text, "text-embedding-3-small")
    assert len(vector) == 1536
    # Unit vector validation (norm should be close to 1.0)
    import numpy as np
    norm = np.linalg.norm(vector)
    assert pytest.approx(norm) == 1.0

def test_mcp_risk_classification():
    # Critical risk
    assert MCPGateway.classify_risk("run_system_command", {"command": "rm -rf /etc"}) == "critical"
    # High risk
    assert MCPGateway.classify_risk("write_file", {"path": "app.py", "content": "print()"}) == "high"
    # Medium risk
    assert MCPGateway.classify_risk("read_file", {"path": "app.py"}) == "medium"
    # Low risk
    assert MCPGateway.classify_risk("calculate_sum", {"a": 1, "b": 2}) == "low"

@pytest.mark.asyncio
async def test_mcp_process_tool_call(mock_mongo):
    client, db = mock_mongo
    with patch("app.gateways.mcp_gateway.get_db", return_value=db):
        # Low risk call (Auto-approved)
        res_low = await MCPGateway.process_tool_call("tenant1", "add", {"x": 1})
        assert res_low["status"] == "approved"
        assert res_low["requires_approval"] is False
        
        # High risk call (Pending)
        res_high = await MCPGateway.process_tool_call("tenant1", "write_file", {"path": "c.txt"})
        assert res_high["status"] == "pending"
        assert res_high["requires_approval"] is True
        
        assert db.mcp_approvals.insert_one.call_count == 2
