import os

from services.database import (
    list_documents,
    get_document,
    delete_document as delete_metadata
)

from services.vectordb import delete_document as delete_vectors


def list_documents_tool():
    """
    List all uploaded documents.
    """

    documents = list_documents()

    return {
        "status": "success",
        "count": len(documents),
        "documents": documents
    }


def get_document_info(filename):
    """
    Get metadata of a document.
    """

    document = get_document(filename)

    if document is None:
        return {
            "status": "error",
            "message": "Document not found."
        }

    return {
        "status": "success",
        "document": document
    }


def delete_document_tool(filename):
    """
    Delete a document completely.
    """

    document = get_document(filename)

    if document is None:
        return {
            "status": "error",
            "message": "Document not found."
        }

    if os.path.exists(document["filepath"]):
        os.remove(document["filepath"])

    delete_vectors(filename)

    delete_metadata(filename)

    return {
        "status": "success",
        "message": f"{filename} deleted successfully."
    }