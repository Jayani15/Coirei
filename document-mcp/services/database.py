from sqlalchemy import create_engine, text
from config import DATABASE_URL

# Create PostgreSQL connection
engine = create_engine(DATABASE_URL)


def add_document(title, filename, filepath, file_type, file_size):
    """
    Insert a new document into the database.
    """
    query = text("""
        INSERT INTO documents
        (title, filename, filepath, file_type, file_size)
        VALUES
        (:title, :filename, :filepath, :file_type, :file_size)
    """)

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "title": title,
                "filename": filename,
                "filepath": filepath,
                "file_type": file_type,
                "file_size": file_size
            }
        )


def list_documents():
    """
    Return all uploaded documents.
    """
    query = text("""
        SELECT *
        FROM documents
        ORDER BY upload_date DESC
    """)

    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()

    return rows


def get_document(filename):
    """
    Get a document by filename.
    """
    query = text("""
        SELECT *
        FROM documents
        WHERE filename = :filename
    """)

    with engine.connect() as conn:
        row = conn.execute(
            query,
            {"filename": filename}
        ).mappings().first()

    return row


def delete_document(filename):
    """
    Delete a document.
    """
    query = text("""
        DELETE FROM documents
        WHERE filename = :filename
    """)

    with engine.begin() as conn:
        conn.execute(
            query,
            {"filename": filename}
        )


def document_count():
    """
    Return total number of documents.
    """
    query = text("""
        SELECT COUNT(*) AS total
        FROM documents
    """)

    with engine.connect() as conn:
        result = conn.execute(query).scalar()

    return result