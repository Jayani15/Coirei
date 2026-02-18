import asyncio
from datetime import datetime, timezone
from app.queue import pop_batch
from app.database import AsyncSessionLocal
from app.models import Event
from app.config import settings

async def worker():
    print("🚀 Worker started")
    print("Worker DB URL:", settings.DATABASE_URL)

    while True:
        batch = await pop_batch(settings.BATCH_SIZE)

        if not batch:
            await asyncio.sleep(1)
            continue

        print("📦 Batch received:", batch)

        events_to_insert = []

        for data in batch:
            try:
                print("Processing event:", data)

                processed_at = datetime.now(timezone.utc)

                event_timestamp = datetime.fromisoformat(data["timestamp"])

                latency = int(
                    (processed_at - event_timestamp).total_seconds() * 1000
                )

                event_obj = Event(
                    client_id=data["client_id"],
                    event_id=data["event_id"],
                    event_type=data["event_type"],
                    event_timestamp=event_timestamp,
                    processed_at=processed_at,
                    payload=data["payload"],
                    status="processed",
                    processing_latency_ms=latency
                )

                events_to_insert.append(event_obj)

            except Exception as e:
                print("❌ Error building event object:", e)

        try:
            async with AsyncSessionLocal() as db:
                await db.begin()
                db.add_all(events_to_insert)
                await db.commit()

            print("✅ Inserted batch successfully")

        except Exception as e:
            print("❌ DB INSERT ERROR:", e)


asyncio.run(worker())