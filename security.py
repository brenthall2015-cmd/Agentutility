import os
import secrets
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

header = APIKeyHeader(name="X-API-Key", auto_error=False)

def require_api_key(value: str | None = Security(header)):
    configured = os.environ.get("AGENTUTILITY_API_KEY", "")
    if len(configured) < 24:
        raise HTTPException(503, "API access is not configured")
    if not value or not secrets.compare_digest(value, configured):
        raise HTTPException(401, "Invalid API key")
    return True
