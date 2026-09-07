import fitz

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from all pages of a PDF resume.
    """

    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text.strip()