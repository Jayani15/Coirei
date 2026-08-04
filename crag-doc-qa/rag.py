import os

import fitz  # PyMuPDF
import docx

from sentence_transformers import SentenceTransformer, CrossEncoder
from langchain.text_splitter import RecursiveCharacterTextSplitter

from qdrant_db import search_chunks
from config import TOP_K, FINAL_K

from qdrant_db import (
    create_collection,
    insert_chunks
)

from config import (
    EMBEDDING_MODEL,
    RERANKER_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------------------------------------------
# Load Models (Loaded once when app starts)
# ---------------------------------------------------

embedding_model = SentenceTransformer(EMBEDDING_MODEL)

reranker = CrossEncoder(RERANKER_MODEL)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

def load_pdf(file_path):
    """
    Extract text from PDF.
    """

    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text

def load_docx(file_path):
    """
    Extract text from DOCX.
    """

    document = docx.Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text

def load_document(file_path):
    """
    Detect file type and extract text.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    elif extension == ".docx":
        return load_docx(file_path)

    else:
        raise ValueError("Unsupported File Type")

def chunk_document(text):
    """
    Split large text into smaller chunks.
    """

    chunks = text_splitter.split_text(text)

    return chunks

def create_embeddings(chunks):
    """
    Generate embeddings for each chunk.
    """

    embeddings = embedding_model.encode(
        chunks,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings

def index_documents(file_path):
    """
    Complete ingestion pipeline.
    """

    print("Loading document...")

    text = load_document(file_path)

    print("Chunking document...")

    chunks = chunk_document(text)

    print(f"Created {len(chunks)} chunks")

    print("Generating embeddings...")

    embeddings = create_embeddings(chunks)

    print("Connecting to Qdrant...")

    create_collection()

    print("Uploading vectors...")

    insert_chunks(
        chunks,
        embeddings
    )

    print("Document Indexed Successfully!")

def retrieve_chunks(question):
    """
    Retrieve the most similar chunks from Qdrant.
    """

    question_embedding = embedding_model.encode(
        question,
        convert_to_numpy=True
    )

    results = search_chunks(
        question_embedding,
        TOP_K
    )

    return results

def rerank_chunks(question, retrieved_chunks):
    """
    Rerank retrieved chunks using CrossEncoder.
    """

    pairs = [
        (question, chunk["text"])
        for chunk in retrieved_chunks
    ]

    scores = reranker.predict(pairs)

    ranked = []

    for chunk, score in zip(retrieved_chunks, scores):

        ranked.append({
            "text": chunk["text"],
            "score": float(score)
        })

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked[:FINAL_K] 

def evaluate_context(ranked_chunks):
    """
    Evaluate whether retrieved context is good enough.
    """

    if len(ranked_chunks) == 0:
        return "BAD"

    best_score = ranked_chunks[0]["score"]

    print(f"Best Reranker Score: {best_score}")

    if best_score >= 0.75:
        return "GOOD"

    elif best_score >= 0.45:
        return "AMBIGUOUS"

    else:
        return "BAD"

def corrective_retrieval(question):
    """
    Corrective Retrieval used when context quality is low.
    """

    question_embedding = embedding_model.encode(
        question,
        convert_to_numpy=True
    )

    retrieved = search_chunks(
        question_embedding,
        limit=TOP_K * 2
    )

    reranked = rerank_chunks(
        question,
        retrieved
    )

    return reranked

def build_context(ranked_chunks):
    """
    Convert ranked chunks into a single context string.
    """

    context = "\n\n".join(
        chunk["text"]
        for chunk in ranked_chunks
    )

    return context

def retrieve_context(question):
    """
    Complete CRAG retrieval pipeline.
    """

    print("Retrieving chunks...")

    retrieved = retrieve_chunks(question)

    print("Reranking chunks...")

    ranked = rerank_chunks(
        question,
        retrieved
    )

    status = evaluate_context(ranked)

    print("Context Status:", status)

    if status == "GOOD":

        return build_context(ranked), ranked

    elif status == "AMBIGUOUS":

        print("Running Corrective Retrieval...")

        corrected = corrective_retrieval(question)

        return build_context(corrected), corrected

    else:

        return "", []

def build_prompt(context, question):
    """
    Build a grounded prompt for the LLM.
    """

    prompt = f"""
You are an intelligent AI assistant.

Answer ONLY using the information provided in the CONTEXT below.

Rules:
1. Do NOT use outside knowledge.
2. If the answer is not present in the context, reply exactly:
"I don't know."
3. Be concise and accurate.

-------------------------
CONTEXT
-------------------------
{context}

-------------------------
QUESTION
-------------------------
{question}

-------------------------
ANSWER
-------------------------
"""

    return prompt

def generate_answer(prompt):
    """
    Generate response using Groq.
    """

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2,

        max_tokens=512
    )

    return response.choices[0].message.content.strip()

def ask_question(question):
    """
    Complete CRAG pipeline.
    """

    print("=" * 50)
    print("User Question:", question)
    print("=" * 50)

    context, ranked_chunks = retrieve_context(question)

    # No context retrieved
    if context.strip() == "":

        return "I don't know.", []

    prompt = build_prompt(
        context,
        question
    )

    answer = generate_answer(prompt)
    answer = verify_answer(answer)

    retrieved_chunks = [
        chunk["text"]
        for chunk in ranked_chunks
    ]

    return answer, retrieved_chunks

def verify_answer(answer):
    """
    Simple post-processing safety check.
    """

    if answer.strip() == "":
        return "I don't know."

    banned_phrases = [
        "based on my knowledge",
        "generally",
        "typically",
        "usually",
        "in most cases"
    ]

    lower_answer = answer.lower()

    for phrase in banned_phrases:
        if phrase in lower_answer:
            return "I don't know."

    return answer