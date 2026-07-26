from services.database import get_document
from services.parser import extract_text


def summarize_document(filename):
    """
    Generate a simple summary of a document.
    """

    document = get_document(filename)

    if document is None:
        return {
            "status": "error",
            "message": "Document not found."
        }

    text = extract_text(document["filepath"])

    paragraphs = text.split("\n")

    summary = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if paragraph:
            summary += paragraph + "\n"

        if len(summary) >= 1000:
            break

    return {
        "status": "success",
        "document": filename,
        "summary": summary.strip()
    }