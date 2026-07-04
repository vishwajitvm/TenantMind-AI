import pytest
from unittest.mock import MagicMock, AsyncMock
from app.database import tenant_context

@pytest.fixture(autouse=True)
def reset_tenant_context():
    """Resets the tenant context to 'default' before each test."""
    tenant_context.set("default")
    yield
    tenant_context.set("default")

@pytest.fixture
def mock_mongo():
    """Fixture to mock Motor AsyncIOMotorClient and database operations."""
    mock_db = MagicMock()
    mock_db.command = AsyncMock(return_value={"ok": 1})
    
    # Mock collections
    mock_db.llm_metrics = MagicMock()
    mock_db.llm_metrics.insert_one = AsyncMock(return_value=MagicMock())
    mock_db.llm_metrics.find = MagicMock()
    mock_db.llm_metrics.count_documents = AsyncMock(return_value=1)
    
    mock_db.mcp_approvals = MagicMock()
    mock_db.mcp_approvals.insert_one = AsyncMock(return_value=MagicMock())
    mock_db.mcp_approvals.find_one = AsyncMock()
    mock_db.mcp_approvals.update_one = AsyncMock()
    mock_db.mcp_approvals.find = MagicMock()
    
    mock_db.documents = MagicMock()
    mock_db.documents.insert_one = AsyncMock(return_value=MagicMock())
    mock_db.documents.update_one = AsyncMock()
    mock_db.documents.find_one = AsyncMock()
    mock_db.documents.find = MagicMock()

    mock_db.chats = MagicMock()
    mock_db.chats.insert_one = AsyncMock(return_value=MagicMock())
    mock_db.chats.find = MagicMock()

    # Mock client
    mock_client = MagicMock()
    mock_client.__getitem__.return_value = mock_db
    
    return mock_client, mock_db

@pytest.fixture
def mock_qdrant():
    """Fixture to mock QdrantClient operations."""
    mock_client = MagicMock()
    mock_client.get_collections.return_value = MagicMock(collections=[])
    mock_client.create_collection.return_value = True
    mock_client.upsert.return_value = True
    
    mock_hit = MagicMock()
    mock_hit.payload = {"content": "Sample document content.", "filename": "test.txt"}
    mock_client.search.return_value = [mock_hit]
    
    return mock_client

@pytest.fixture
def mock_minio():
    """Fixture to mock MinIO Client operations."""
    mock_client = MagicMock()
    mock_client.bucket_exists.return_value = False
    mock_client.make_bucket.return_value = True
    mock_client.put_object.return_value = MagicMock()
    
    # Mock download file object
    mock_response = MagicMock()
    mock_response.read.return_value = b"Hello, this is a test document with AWS key AKIA1234567890123456."
    mock_response.close = MagicMock()
    mock_response.release_conn = MagicMock()
    mock_client.get_object.return_value = mock_response
    mock_client.list_buckets.return_value = []
    
    return mock_client
