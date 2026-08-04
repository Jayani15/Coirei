import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from config import (
    COLLECTION_NAME,
    VECTOR_SIZE
)

# ---------------------------------------
# Connect to Qdrant
# ---------------------------------------

client = QdrantClient(
    host="localhost",
    port=6333
)

# ---------------------------------------
# Create Collection
# ---------------------------------------

def create_collection():
    """
    Create a fresh collection for every indexing operation.
    """

    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]

    if COLLECTION_NAME in collection_names:
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )

    print("Fresh Collection Created")


# ---------------------------------------
# Insert Chunks
# ---------------------------------------

def insert_chunks(chunks, embeddings):
    """
    Insert document chunks into Qdrant.
    """

    points = []

    for chunk, embedding in zip(chunks, embeddings):

        points.append(

            PointStruct(

                id=str(uuid.uuid4()),

                vector=embedding.tolist(),

                payload={
                    "text": chunk
                }

            )

        )

    client.upsert(

        collection_name=COLLECTION_NAME,

        points=points

    )

    print(f"{len(points)} chunks inserted.")


# ---------------------------------------
# Search
# ---------------------------------------

def search_chunks(query_embedding, limit=5):
    """
    Search similar chunks.
    """

    results = client.search(

        collection_name=COLLECTION_NAME,

        query_vector=query_embedding.tolist(),

        limit=limit

    )

    retrieved = []

    for result in results:

        retrieved.append(

            {

                "text": result.payload["text"],

                "score": result.score

            }

        )

    return retrieved


# ---------------------------------------
# Delete Collection
# ---------------------------------------

def delete_collection():
    """
    Delete collection if needed.
    """

    client.delete_collection(
        collection_name=COLLECTION_NAME
    )

    print("Collection Deleted")