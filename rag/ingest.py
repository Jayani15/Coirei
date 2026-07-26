import os
import uuid

from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams
from langchain_text_splitters import RecursiveCharacterTextSplitter

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = QdrantClient(
    path="./qdrant_data"
)

client.recreate_collection(
    collection_name="customer_support",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

folder = "documents"

points = []

for file in os.listdir(folder):

    path = os.path.join(folder, file)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    print(f"\n========== {file} ==========")
    print(f"Total Chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks[:3]):   # Show first 3 chunks
        print(f"\nChunk {i+1}:")
        print(chunk)
        print("-" * 80)

    for chunk in chunks:

        if len(chunk.strip()) < 20:
            continue

        embedding = model.encode(chunk).tolist()

        print(f"\nEmbedding Length: {len(embedding)}")
        print("First 10 Values:")
        print(embedding[:10])

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "source": file
                }
            )
        )

client.upsert(
    collection_name="customer_support",
    points=points
)

print("Documents Indexed")