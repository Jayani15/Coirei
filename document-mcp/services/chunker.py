from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text):
    """
    Split text into overlapping chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk = text[start:end]

        chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks