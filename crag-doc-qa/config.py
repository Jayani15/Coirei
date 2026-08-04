# Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# CrossEncoder
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# Retrieval
TOP_K = 8
FINAL_K = 3

# Qdrant
COLLECTION_NAME = "crag_documents"

# all-MiniLM-L6-v2 embedding dimension
VECTOR_SIZE = 384