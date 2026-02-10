"""
Rate limiting middleware
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

from app.core.config import settings


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = asyncio.Lock()
    
    async def is_allowed(self, key: str, limit: int, window_seconds: int = 3600) -> bool:
        """Check if request is allowed based on rate limit"""
        async with self.lock:
            now = datetime.utcnow()
            cutoff = now - timedelta(seconds=window_seconds)
            
            # Clean old requests
            self.requests[key] = [req_time for req_time in self.requests[key] if req_time > cutoff]
            
            # Check limit
            if len(self.requests[key]) >= limit:
                return False
            
            # Add current request
            self.requests[key].append(now)
            return True
    
    async def get_remaining(self, key: str, limit: int, window_seconds: int = 3600) -> int:
        """Get remaining requests in current window"""
        async with self.lock:
            now = datetime.utcnow()
            cutoff = now - timedelta(seconds=window_seconds)
            
            self.requests[key] = [req_time for req_time in self.requests[key] if req_time > cutoff]
            
            return max(0, limit - len(self.requests[key]))


# Global rate limiter instance
rate_limiter = RateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware for FastAPI"""
    
    async def dispatch(self, request: Request, call_next):
        """Apply rate limiting to requests"""
        # Skip rate limiting for certain paths
        skip_paths = ["/docs", "/redoc", "/openapi.json", "/health", "/"]
        if any(request.url.path.startswith(path) for path in skip_paths):
            return await call_next(request)
        
        # Get client identifier
        client_id = request.client.host if request.client else "unknown"
        
        # Try to get user from token for better rate limiting
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            try:
                from app.core.security import decode_token
                token = auth_header.split(" ")[1]
                payload = decode_token(token)
                user_id = payload.get("sub")
                if user_id:
                    client_id = f"user_{user_id}"
            except:
                pass
        
        # Determine rate limit based on endpoint
        path = request.url.path
        limit = settings.RATE_LIMIT_GENERAL
        
        if "/upload" in path:
            limit = settings.RATE_LIMIT_UPLOAD
            key = f"upload_{client_id}"
        elif "/download" in path:
            limit = settings.RATE_LIMIT_DOWNLOAD
            key = f"download_{client_id}"
        else:
            key = f"general_{client_id}"
        
        # Check rate limit
        allowed = await rate_limiter.is_allowed(key, limit)
        
        if not allowed:
            remaining = await rate_limiter.get_remaining(key, limit)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again later.",
                headers={
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": str(remaining),
                    "Retry-After": "3600"
                }
            )
        
        # Add rate limit headers to response
        response = await call_next(request)
        remaining = await rate_limiter.get_remaining(key, limit)
        
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response