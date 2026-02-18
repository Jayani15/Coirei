import redis.asyncio as redis
import json
from app.config import settings

r = redis.from_url(settings.REDIS_URL)

async def push_event(event: dict):
    await r.lpush(
        "event_queue",
        json.dumps(event, default=str)
    )

async def pop_batch(batch_size: int):
    events = []
    for _ in range(batch_size):
        item = await r.rpop("event_queue")
        if not item:
            break
        events.append(json.loads(item))
    return events

async def mark_idempotent(key: str):
    return await r.setnx(f"idemp:{key}", 1)
