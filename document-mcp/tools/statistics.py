import os

from config import DOCUMENT_STORAGE

from services.database import document_count
from services.vectordb import chunk_count


def document_statistics():
    """
    Return project statistics.
    """

    total_documents = document_count()

    total_chunks = chunk_count()

    total_size = 0

    file_types = {}

    if os.path.exists(DOCUMENT_STORAGE):

        for file in os.listdir(DOCUMENT_STORAGE):

            path = os.path.join(
                DOCUMENT_STORAGE,
                file
            )

            total_size += os.path.getsize(path)

            extension = file.split(".")[-1].lower()

            file_types[extension] = (
                file_types.get(extension, 0) + 1
            )

    return {
        "status": "success",
        "total_documents": total_documents,
        "total_chunks": total_chunks,
        "storage_used_bytes": total_size,
        "file_types": file_types
    }