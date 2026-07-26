import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from config import (
    QDRANT_HOST,
    QDRANT_PORT,
    QDRANT_COLLECTION
)

# Connect to Qdrant
client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT
)

# Create collection if it doesn't exist
collections = client.get_collections().collections
collection_names = [c.name for c in collections]

if QDRANT_COLLECTION not in collection_names:
    client.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(
            size=384,          # all-MiniLM-L6-v2 embedding size
            distance=Distance.COSINE
        )
    )


def insert_document(filename, chunks, embeddings):
    """
    Store document chunks and embeddings in Qdrant.
    """

    points = []

    for chunk, embedding in zip(chunks, embeddings):

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "filename": filename,
                    "chunk": chunk
                }
            )
        )

    client.upsert(
        collection_name=QDRANT_COLLECTION,
        points=points
    )


def search_documents(query_embedding, limit=5):
    """
    Search similar document chunks.
    """

    results = client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_embedding,
        limit=limit
    )

    documents = []

    for result in results:

        documents.append({
            "score": result.score,
            "filename": result.payload["filename"],
            "chunk": result.payload["chunk"]
        })

    return documents


def delete_document(filename):
    """
    Delete all vectors belonging to a document.
    """

    client.delete(
        collection_name=QDRANT_COLLECTION,
        points_selector={
            "filter": {
                "must": [
                    {
                        "key": "filename",
                        "match": {
                            "value": filename
                        }
                    }
                ]
            }
        }
    )


def chunk_count():
    """
    Return total number of stored chunks.
    """

    info = client.get_collection(QDRANT_COLLECTION)

    return info.points_count