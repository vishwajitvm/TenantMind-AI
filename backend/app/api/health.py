from fastapi import APIRouter, status, Response, HTTPException
from app.database import get_db, get_qdrant_client, get_minio_client
from app.config import settings
from redis import Redis
from tracenest import logger

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check(response: Response):
    """Pings MongoDB, Qdrant, MinIO, and Redis to check service health."""
    status_report = {
        "status": "healthy",
        "services": {}
    }
    
    # 1. MongoDB check
    try:
        db = get_db()
        await db.command("ping")
        status_report["services"]["mongodb"] = "connected"
    except Exception as e:
        logger.error(f"Health check: MongoDB failed: {str(e)}")
        status_report["services"]["mongodb"] = f"error: {str(e)}"
        status_report["status"] = "unhealthy"

    # 2. Qdrant check
    try:
        client = get_qdrant_client()
        client.get_collections()
        status_report["services"]["qdrant"] = "connected"
    except Exception as e:
        logger.error(f"Health check: Qdrant failed: {str(e)}")
        status_report["services"]["qdrant"] = f"error: {str(e)}"
        status_report["status"] = "unhealthy"

    # 3. MinIO check
    try:
        client = get_minio_client()
        client.list_buckets()
        status_report["services"]["minio"] = "connected"
    except Exception as e:
        logger.error(f"Health check: MinIO failed: {str(e)}")
        status_report["services"]["minio"] = f"error: {str(e)}"
        status_report["status"] = "unhealthy"

    # 4. Redis check
    try:
        redis_client = Redis.from_url(settings.REDIS_URL)
        redis_client.ping()
        status_report["services"]["redis"] = "connected"
    except Exception as e:
        logger.error(f"Health check: Redis failed: {str(e)}")
        status_report["services"]["redis"] = f"error: {str(e)}"
        status_report["status"] = "unhealthy"

    if status_report["status"] == "unhealthy":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
    return status_report

@router.get("/ready")
async def readiness_check(response: Response):
    """Readiness probe. Checks if dependencies are accessible."""
    status_report = await health_check(response)
    if status_report["status"] != "healthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="System is not ready"
        )
    return {"status": "ready"}

@router.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    # Return simple metrics payload
    from fastapi.responses import PlainTextResponse
    metrics_data = (
        "# HELP tenantmind_health_status Overall health status (1 = healthy, 0 = unhealthy)\n"
        "# TYPE tenantmind_health_status gauge\n"
        "tenantmind_health_status 1\n"
    )
    return PlainTextResponse(metrics_data)
