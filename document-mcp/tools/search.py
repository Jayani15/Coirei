from services.embeddings import generate_embedding
from services.vectordb import search_documents


def search_documents_tool(query):
    """
    Search documents using semantic similarity.
    """

    query_embedding = generate_embedding(query)

    results = search_documents(query_embedding)

    if not results:
        return {
            "status": "error",
            "message": "No matching documents found."
        }

    return {
        "status": "success",
        "query": query,
        "results": results
    }