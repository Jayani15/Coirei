import json
import uuid
from typing import Any, Dict, List

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from sentence_transformers import SentenceTransformer

import os


QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://localhost:6333"
)

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "candidate_profiles"


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


if QDRANT_API_KEY:
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )
else:
    qdrant_client = QdrantClient(
        url=QDRANT_URL
    )


def initialize_qdrant():

    exists = qdrant_client.collection_exists(
        COLLECTION_NAME
    )

    if not exists:

        vector_size = (
            embedding_model
            .get_sentence_embedding_dimension()
        )

        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,

            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )


def create_embedding(text: str) -> List[float]:

    vector = embedding_model.encode(text)

    return vector.tolist()


def create_candidate_chunks(
    resume_data: Dict[str, Any]
) -> List[Dict[str, str]]:

    chunks = []

    for field, value in resume_data.items():

        if not value:
            continue

        if isinstance(value, list):

            for index, item in enumerate(value):

                text = (
                    f"{field}: "
                    f"{json.dumps(item, ensure_ascii=False)}"
                )

                chunks.append({
                    "field": field,
                    "text": text
                })

        else:

            chunks.append({
                "field": field,
                "text": f"{field}: {value}"
            })

    return chunks


def store_candidate_profile(
    candidate_id: int,
    resume_data: Dict[str, Any]
):

    initialize_qdrant()

    chunks = create_candidate_chunks(
        resume_data
    )

    points = []

    for index, chunk in enumerate(chunks):

        vector = create_embedding(
            chunk["text"]
        )

        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_DNS,
                f"candidate-{candidate_id}-{index}"
            )
        )

        points.append(
            PointStruct(
                id=point_id,

                vector=vector,

                payload={
                    "candidate_id": candidate_id,
                    "field": chunk["field"],
                    "text": chunk["text"]
                }
            )
        )

    if points:

        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )


def search_candidate_knowledge(
    candidate_id: int,
    query: str,
    limit: int = 5
):

    initialize_qdrant()

    query_vector = create_embedding(query)

    results = qdrant_client.search(
        collection_name=COLLECTION_NAME,

        query_vector=query_vector,

        query_filter=Filter(
            must=[
                FieldCondition(
                    key="candidate_id",
                    match=MatchValue(
                        value=candidate_id
                    )
                )
            ]
        ),

        limit=limit
    )

    return [
        {
            "score": round(
                float(result.score),
                4
            ),

            "field": result.payload.get(
                "field"
            ),

            "text": result.payload.get(
                "text"
            )
        }

        for result in results
    ]