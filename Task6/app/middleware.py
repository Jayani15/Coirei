import time
from starlette.middleware.base import BaseHTTPMiddleware
from app.database import AsyncSessionLocal
from app.models import AuditLog

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = int((time.time() - start) * 1000)

        async with AsyncSessionLocal() as db:
            log = AuditLog(
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                response_time_ms=duration,
            )
            db.add(log)
            await db.commit()

        return response
