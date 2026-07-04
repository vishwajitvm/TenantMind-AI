from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.middleware import TenantMiddleware, TraceNestMiddleware
from app.api import chats, documents, approvals, audit_logs, models, health
from app.config import settings
from tracenest import logger

# Initialize FastAPI App
app = FastAPI(
    title="TenantMind AI API",
    description="Multitenant AI Backend API with strict isolation, LLM fallback gateways, and MCP tool validation.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Middleware
app.add_middleware(TraceNestMiddleware)
app.add_middleware(TenantMiddleware)

# Custom Exception Handlers for logging
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global unhandled exception on {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."}
    )

# Register Routers (register both with and without '/api' prefix for routing flexibility)
for router_module in [chats, documents, approvals, audit_logs, models, health]:
    app.include_router(router_module.router, prefix="/api")
    app.include_router(router_module.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to TenantMind AI API Gateway",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/tracenest")
async def tracenest_logs():
    """Endpoint for Tracenest log verification or status."""
    return {
        "tracenest": "active",
        "enabled": settings.TRACENEST_ENABLED,
        "logging_level": "INFO"
    }
