import fitz  # PyMuPDF
from docx import Document
import os


def parse_pdf(file_path):
    """
    Extract text from a PDF file.
    """
    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def parse_docx(file_path):
    """
    Extract text from a DOCX file.
    """
    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def parse_txt(file_path):
    """
    Extract text from a TXT file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_text(file_path):
    """
    Detect file type and extract text.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return parse_pdf(file_path)

    elif extension == ".docx":
        return parse_docx(file_path)

    elif extension == ".txt":
        return parse_txt(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")