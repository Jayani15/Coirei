import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Qdrant
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")

# Embedding Model
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# Storage
DOCUMENT_STORAGE = os.getenv("DOCUMENT_STORAGE")

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100