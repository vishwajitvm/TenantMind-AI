from langsmith import traceable
from contextvars import ContextVar
from motor.motor_asyncio import AsyncIOMotorClient
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from minio import Minio
from app.config import settings
from tracenest import logger
import re

# Context variable to hold current tenant slug
tenant_context: ContextVar[str] = ContextVar("tenant_context", default="default")

@traceable
def get_tenant_slug() -> str:
    logger.debug(f"Entering get_tenant_slug")
    """Returns the current tenant slug, sanitized for database/bucket naming."""
    slug = tenant_context.get()
    # Sanitize: alphanumeric and hyphens/underscores only
    slug = re.sub(r'[^a-zA-Z0-9_-]', '', slug).lower()
    return slug or "default"

# MongoDB dynamic routing
_mongo_client: AsyncIOMotorClient = None

@traceable
def get_mongo_client() -> AsyncIOMotorClient:
    logger.debug(f"Entering get_mongo_client")
    global _mongo_client
    if _mongo_client is None:
        uri = settings.MONGODB_ATLAS_URI or "mongodb://localhost:27017"
        _mongo_client = AsyncIOMotorClient(uri)
        logger.info(f"Initialized MongoDB AsyncIOMotorClient on {uri}")
    return _mongo_client

@traceable
def get_db():
    logger.debug(f"Entering get_db")
    client = get_mongo_client()
    slug = get_tenant_slug()
    db_name = f"org_{slug.replace('-', '_')}"
    return client[db_name]

# MinIO client and bucket helper
_minio_client: Minio = None

@traceable
def get_minio_client() -> Minio:
    logger.debug(f"Entering get_minio_client")
    global _minio_client
    if _minio_client is None:
        # MinIO endpoint should not start with http:// or https:// for Minio client initialization
        endpoint = settings.MINIO_ENDPOINT.replace("http://", "").replace("https://", "")
        _minio_client = Minio(
            endpoint=endpoint,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        logger.info(f"Initialized MinIO Client at {endpoint}")
    return _minio_client

@traceable
def ensure_minio_bucket() -> str:
    logger.debug(f"Entering ensure_minio_bucket")
    client = get_minio_client()
    slug = get_tenant_slug()
    # MinIO bucket names must follow DNS rules: only lowercase letters, numbers, and hyphens.
    bucket_name = f"org-{slug.replace('_', '-')}-bucket"
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            logger.info(f"Created MinIO bucket: {bucket_name}")
    except Exception as e:
        logger.error(f"Error ensuring MinIO bucket {bucket_name}: {str(e)}")
        raise e
    return bucket_name

# Qdrant client and collection helper
_qdrant_client: QdrantClient = None

@traceable
def get_qdrant_client() -> QdrantClient:
    logger.debug(f"Entering get_qdrant_client")
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(url=settings.QDRANT_URL)
        logger.info(f"Initialized Qdrant client at {settings.QDRANT_URL}")
    return _qdrant_client

@traceable
def ensure_qdrant_collection(vector_size: int = 1536, distance_metric: str = "Cosine") -> str:
    logger.debug(f"Entering ensure_qdrant_collection")
    client = get_qdrant_client()
    slug = get_tenant_slug()
    collection_name = f"org_{slug.replace('-', '_')}_vectors"
    
    # Map distance metric
    distance = qmodels.Distance.COSINE
    if distance_metric.upper() == "EUCLIDEAN":
        distance = qmodels.Distance.EUCLID
    elif distance_metric.upper() == "DOT":
        distance = qmodels.Distance.DOT

    try:
        collections_response = client.get_collections()
        existing_collections = [c.name for c in collections_response.collections]
        if collection_name not in existing_collections:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=qmodels.VectorParams(
                    size=vector_size,
                    distance=distance
                )
            )
            logger.info(f"Created Qdrant collection: {collection_name} (size: {vector_size})")
    except Exception as e:
        logger.error(f"Error ensuring Qdrant collection {collection_name}: {str(e)}")
        raise e
    return collection_name
