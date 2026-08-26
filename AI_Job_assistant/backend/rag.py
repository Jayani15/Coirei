import os
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from docx import Document


VECTOR_DB_PATH = os.getenv(
    "VECTOR_DB_PATH",
    "./vector_db"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path=VECTOR_DB_PATH
)

collection = client.get_or_create_collection(
    name="job_descriptions"
)


def extract_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    elif extension == ".docx":

        document = Document(file_path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    elif extension == ".txt":

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    else:
        raise ValueError(
            "Unsupported file type"
        )


def chunk_text(text, chunk_size=500):

    words = text.split()

    chunks = []

    for i in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        chunks.append(chunk)

    return chunks


def add_job_description(
    file_path,
    job_id
):

    text = extract_text(file_path)

    chunks = chunk_text(text)

    embeddings = embedding_model.encode(
        chunks
    ).tolist()

    ids = [
        f"{job_id}_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {
                "job_id": str(job_id)
            }
            for _ in chunks
        ]
    )

    return {
        "job_id": job_id,
        "chunks": len(chunks)
    }


def search_job_description(
    query,
    job_id,
    top_k=3
):

    query_embedding = embedding_model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        where={
            "job_id": str(job_id)
        }
    )

    return results["documents"][0]