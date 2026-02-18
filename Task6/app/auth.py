from fastapi import Header, HTTPException, Depends
from sqlalchemy.future import select
from app.database import get_db
from app.models import Client

async def get_current_client(
    api_key: str = Header(...),
    db=Depends(get_db)
):
    result = await db.execute(select(Client).where(Client.api_key == api_key))
    client = result.scalar_one_or_none()

    if not client or not client.is_active:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return client
