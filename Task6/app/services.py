from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from app.models import Event
from datetime import datetime

async def bulk_insert_events(db, events):
    db.add_all(events)
    await db.commit()

async def analytics_count(db, event_type: str, start=None, end=None):
    query = select(func.count()).select_from(Event).where(
        Event.event_type == event_type
    )

    if start:
        query = query.where(Event.event_timestamp >= start)
    if end:
        query = query.where(Event.event_timestamp <= end)

    result = await db.execute(query)
    return result.scalar()

async def analytics_group(db):
    query = select(
        Event.client_id,
        Event.event_type,
        func.count().label("count")
    ).group_by(Event.client_id, Event.event_type)

    result = await db.execute(query)
    rows = result.all()

    return [
        {
            "client_id": row.client_id,
            "event_type": row.event_type,
            "count": row.count
        }
        for row in rows
    ]

