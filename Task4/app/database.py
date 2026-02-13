from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import redis.asyncio as redis
import os

# Get from environment variables (set by docker-compose)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:Jayani@localhost/eventdb")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def get_db():
    async with async_session_maker() as session:
        yield session