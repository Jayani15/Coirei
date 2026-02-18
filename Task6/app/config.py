import os

class Settings:
    DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/events"
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", 100))
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 100))

settings = Settings()
