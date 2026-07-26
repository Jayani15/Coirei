from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = QdrantClient(
    path="./qdrant_data"
)

def retrieve(query):

    vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name="customer_support",
        query=vector,
        limit=5
    ).points

    return results