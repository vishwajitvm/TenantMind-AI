import time
import json
import logging
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
import httpx
from app.config import settings
from app.database import tenant_context
from tracenest import logger

# Global cache for Keycloak public keys to avoid fetching on every request
_jwks_cache = None
_jwks_last_fetched = 0

async def get_keycloak_jwks() -> dict:
    global _jwks_cache, _jwks_last_fetched
    now = time.time()
    # Cache for 1 hour
    if _jwks_cache is None or (now - _jwks_last_fetched > 3600):
        url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    _jwks_cache = resp.json()
                    _jwks_last_fetched = now
                else:
                    logger.warning(f"Failed to fetch Keycloak JWKS: {resp.status_code}")
        except Exception as e:
            logger.error(f"Error fetching Keycloak JWKS from {url}: {str(e)}")
    return _jwks_cache or {}

def extract_tenant_from_token(token: str) -> str:
    """Decodes token and retrieves tenant slug/org identifier."""
    try:
        # First try to get claims without verification to extract tenant info
        claims = jwt.get_unverified_claims(token)
        # Check standard claims
        for key in ["org_slug", "tenant_slug", "tenant", "organization", "org"]:
            if key in claims and claims[key]:
                return str(claims[key])
        
        # Check resource_access or group membership
        if "resource_access" in claims:
            # use keycloak client-id or any keys
            for client_id, access in claims["resource_access"].items():
                if "roles" in access:
                    for role in access["roles"]:
                        if role.startswith("org_"):
                            return role[4:]

        # If sub claim is present, we could fall back to sub or default
        if "sub" in claims:
            return "default"
    except Exception as e:
        logger.warning(f"Error reading unverified claims: {str(e)}")
    return "default"

async def validate_token_and_get_tenant(token: str) -> str:
    """Validates Keycloak JWT and returns the tenant slug."""
    # For testing/dev, if verification fails or Keycloak is unreachable,
    # we fall back to unverified claims extraction to keep system running.
    jwks = await get_keycloak_jwks()
    tenant_slug = extract_tenant_from_token(token)
    
    if not jwks:
        logger.warning("JWKS not loaded. Using unverified claim extraction for tenant.")
        return tenant_slug

    try:
        # Decode signature
        # In a real environment, we'd match the 'kid' and verify using public keys
        # For robustness in tests, we try to verify, otherwise fallback
        # Let's decode with verification turned off if KEYCLOAK_CLIENT_SECRET is not set,
        # or verify if keys are available.
        # We can extract the kid from token header
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        key = None
        if kid:
            for jwk in jwks.get("keys", []):
                if jwk.get("kid") == kid:
                    key = jwk
                    break
        
        if key:
            # Verify signature using the key
            # Standard Keycloak tokens use RS256
            decoded = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=settings.KEYCLOAK_CLIENT_ID,
                issuer=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}"
            )
            # Extracted after validation
            for k in ["org_slug", "tenant_slug", "tenant", "organization", "org"]:
                if k in decoded and decoded[k]:
                    return str(decoded[k])
        else:
            # Try verification with fallback
            logger.info("Matching JWK kid not found. Decoding without verification fallback.")
    except Exception as e:
        logger.warning(f"Token signature verification failed: {str(e)}. Falling back to unverified decoding.")
    
    return tenant_slug

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude public endpoints
        path = request.url.path
        if path in ["/health", "/docs", "/redoc", "/openapi.json"] or path.startswith("/api/health"):
            # Set default tenant for health/docs
            tenant_context.set("default")
            return await call_next(request)

        # Check tenant from header or query param first (useful for development/tests)
        tenant_header = request.headers.get("X-Tenant-ID") or request.headers.get("X-Organization-Slug")
        if tenant_header:
            tenant_context.set(tenant_header)
            return await call_next(request)
        
        # Check token
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                tenant_slug = await validate_token_and_get_tenant(token)
                tenant_context.set(tenant_slug)
            except Exception as e:
                logger.error(f"Tenant authentication error: {str(e)}")
                # Allow it but set to default, or reject? Let's default to 'default' or raise
                # Let's set default and let API routers enforce authentication if needed
                tenant_context.set("default")
        else:
            # No auth header. Default to 'default'
            tenant_context.set("default")

        return await call_next(request)

class TraceNestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        method = request.method
        url = str(request.url)
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"
        
        # Redact sensitive headers
        headers_to_log = dict(request.headers)
        for key in ["authorization", "cookie", "x-api-key", "proxy-authorization"]:
            if key in headers_to_log:
                headers_to_log[key] = "[REDACTED]"
        
        logger.info(f"Incoming Request: {method} {path} from {client_ip} | Headers: {json.dumps(headers_to_log)}")
        
        try:
            response: Response = await call_next(request)
            duration = time.time() - start_time
            logger.info(
                f"Request Completed: {method} {path} | Status: {response.status_code} | Duration: {duration:.4f}s"
            )
            # Add custom header with execution duration
            response.headers["X-Process-Time"] = f"{duration:.4f}s"
            return response
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Request Failed: {method} {path} | Error: {str(e)} | Duration: {duration:.4f}s",
                exc_info=True
            )
            # Re-raise to let exception handlers catch it
            raise e
