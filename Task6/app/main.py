from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.database import engine, Base, get_db
from app.schemas import EventCreate
from app.security import get_current_client
from app.rate_limit import check_rate_limit
from app.queue import push_event, mark_idempotent
from app.services import analytics_count, analytics_group
from app.middleware import AuditMiddleware
from app.models import Client

app = FastAPI(
    title="Event-Driven Analytics API",
    version="1.0.0"
)

app.add_middleware(AuditMiddleware)
from app.config import settings

@app.on_event("startup")
async def startup():
    print("DATABASE URL:", settings.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")

@app.post("/events", status_code=202, tags=["Events"])
async def ingest_event(
    event: EventCreate,
    client: Client = Depends(get_current_client)
):
    await check_rate_limit(client.api_key)

    idemp_key = f"{client.id}:{event.event_id}"
    if not await mark_idempotent(idemp_key):
        return {"message": "Duplicate event ignored"}

    await push_event({
        "client_id": client.id,
        **event.dict()
    })

    return {"message": "Event accepted"}

@app.get("/analytics/count", tags=["Analytics"])
async def count(
    event_type: str,
    start: datetime = None,
    end: datetime = None,
    db: AsyncSession = Depends(get_db)
):
    result = await analytics_count(db, event_type, start, end)
    return {"count": result}

@app.get("/analytics/group", tags=["Analytics"])
async def group(db: AsyncSession = Depends(get_db)):
    result = await analytics_group(db)
    return {"groups": result}

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}
