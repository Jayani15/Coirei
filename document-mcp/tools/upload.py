import os
import shutil

from config import DOCUMENT_STORAGE

from services.database import add_document
from services.parser import extract_text
from services.chunker import chunk_text
from services.embeddings import generate_embeddings
from services.vectordb import insert_document


def upload_document(file_path):
    """
    Upload and index a document.
    """

    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": "File not found."
        }

    os.makedirs(DOCUMENT_STORAGE, exist_ok=True)

    filename = os.path.basename(file_path)

    destination = os.path.join(
        DOCUMENT_STORAGE,
        filename
    )

    shutil.copy(file_path, destination)

    text = extract_text(destination)

    chunks = chunk_text(text)

    embeddings = generate_embeddings(chunks)

    insert_document(
        filename,
        chunks,
        embeddings
    )

    add_document(
        title=os.path.splitext(filename)[0],
        filename=filename,
        filepath=destination,
        file_type=filename.split(".")[-1],
        file_size=os.path.getsize(destination)
    )

    return {
        "status": "success",
        "document": filename,
        "chunks_created": len(chunks),
        "message": "Document uploaded successfully."
    }