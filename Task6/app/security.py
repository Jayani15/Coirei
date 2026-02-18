from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.future import select
from app.database import get_db
from app.models import Client

api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_current_client(
    api_key: str = Security(api_key_scheme),
    db = Depends(get_db)
):
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")

    result = await db.execute(
        select(Client).where(Client.api_key == api_key)
    )
    client = result.scalar_one_or_none()

    if not client or not client.is_active:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return client
