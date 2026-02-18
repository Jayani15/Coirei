import redis.asyncio as redis
from fastapi import HTTPException
from app.config import settings

r = redis.from_url(settings.REDIS_URL)

async def check_rate_limit(api_key: str):
    key = f"rate:{api_key}"
    count = await r.incr(key)

    if count == 1:
        await r.expire(key, 60)

    if count > settings.RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
