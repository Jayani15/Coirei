from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

# Load model only once
model = SentenceTransformer(EMBEDDING_MODEL)


def generate_embedding(text):
    """
    Generate embedding for a single text.
    """

    embedding = model.encode(
        text,
        convert_to_numpy=True
    )

    return embedding.tolist()


def generate_embeddings(chunks):
    """
    Generate embeddings for multiple chunks.
    """

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True
    )

    return embeddings.tolist()