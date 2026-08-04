# 📚 Corrective RAG (CRAG) Document Q&A System

A lightweight **Corrective Retrieval-Augmented Generation (CRAG)** application that allows users to upload PDF/DOCX documents, index them into a vector database, and ask questions grounded only on the uploaded documents.

The system retrieves relevant document chunks, reranks them using a CrossEncoder, evaluates the quality of the retrieved context, performs corrective retrieval when necessary, and finally generates an answer using the **Groq LLM API**.

---

## 🚀 Features

- Upload PDF and DOCX documents
- Automatic document chunking
- Sentence Transformer embeddings
- Qdrant Vector Database
- Semantic Retrieval
- CrossEncoder Reranking
- Context Quality Evaluation
- Corrective Retrieval (CRAG)
- Groq LLM Integration
- "I don't know" safety mechanism
- Streamlit Web Interface

---

## 📂 Project Structure

```
crag-document-qa/
│
├── app.py
├── rag.py
├── qdrant_db.py
├── config.py
├── requirements.txt
├── README.md
├── .env
│
└── data/
```

---

## ⚙️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| LLM | Groq (Llama 3.1) |
| Embeddings | all-MiniLM-L6-v2 |
| Reranker | ms-marco-MiniLM-L-6-v2 |
| Vector Database | Qdrant |
| PDF Reader | PyMuPDF |
| DOCX Reader | python-docx |
| Programming Language | Python |

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone <repository-url>

cd crag-document-qa
```

---

### 2. Create a virtual environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Groq API Key

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key
```

You can obtain an API key from:

https://console.groq.com

---

## ▶ Running Qdrant

Using Docker

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Qdrant will be available at

```
http://localhost:6333
```

---

## ▶ Running the Application

```bash
streamlit run app.py
```

The application opens at

```
http://localhost:8501
```

---

## 📝 Workflow

1. Upload a PDF or DOCX file.
2. Click **Index Document**.
3. The document is:
   - Loaded
   - Chunked
   - Embedded
   - Stored in Qdrant
4. Enter a question.
5. The system:
   - Retrieves relevant chunks
   - Reranks them
   - Evaluates context quality
   - Performs corrective retrieval (if required)
   - Sends the final context to Groq
6. The answer is displayed.

---

## 🔄 CRAG Pipeline

```
Upload Document
        │
        ▼
Extract Text
        │
        ▼
Chunk Document
        │
        ▼
Generate Embeddings
        │
        ▼
Store in Qdrant
────────────────────────────

User Question
        │
        ▼
Vector Retrieval
        │
        ▼
CrossEncoder Reranking
        │
        ▼
Context Evaluation
        │
 ┌──────┴─────────┐
 │                │
 ▼                ▼
GOOD          AMBIGUOUS
 │                │
 │        Corrective Retrieval
 │                │
 └──────┬─────────┘
        ▼
Groq LLM
        │
        ▼
Final Answer
```

---

## 📌 Example Questions

- What is Artificial Intelligence?
- What is Machine Learning?
- List the applications of AI.
- What are the advantages of AI?
- Explain the limitations of AI.

---

## 🛡 Safety Rule

The assistant answers **only from the uploaded document**.

If the answer cannot be found in the retrieved context, the assistant responds:

```
I don't know.
```

This helps reduce hallucinations and ensures grounded responses.

---

## 👨‍💻 Author

**Jayani Immidi**

Bachelor of Technology (Computer Science & Engineering)

CRAG Document Question Answering System using Groq, Qdrant, and Sentence Transformers.