# 📚 DocuMind MCP

DocuMind MCP is a **Model Context Protocol (MCP) server** for intelligent document management. It allows users to upload, index, search, summarize, and manage documents through MCP-compatible clients.

The project combines **FastMCP**, **PostgreSQL**, **Qdrant Vector Database**, and **Sentence Transformers** to provide semantic document retrieval and management.

---

## ✨ Features

- 📤 Upload and index documents
- 🔍 Semantic search using vector embeddings
- 📝 Generate document summaries
- 📋 List all uploaded documents
- ℹ️ View document metadata
- 🗑️ Delete documents
- 📊 View document statistics

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| FastMCP | MCP Server |
| PostgreSQL | Metadata Storage |
| Qdrant | Vector Database |
| Sentence Transformers | Text Embeddings |
| Docker | Qdrant Deployment |

---

# Project Structure

```
DocuMind-MCP/
│
├── db/
│   └── schema.sql
│
├── services/
│   ├── database.py
│   ├── embeddings.py
│   ├── file_parser.py
│   └── vectordb.py
│
├── storage/
│   └── documents/
│
├── tools/
│   ├── upload.py
│   ├── search.py
│   ├── summary.py
│   ├── documents.py
│   └── statistics.py
│
├── config.py
├── requirements.txt
├── server.py
└── README.md
```

---

# Database Setup

Create a PostgreSQL database.

Example:

```sql
CREATE DATABASE documind;
```

Run the schema:

```sql
db/schema.sql
```

---

# Qdrant Setup

Install Docker and start the Qdrant container.

```bash
docker run -d --name qdrant \
-p 6333:6333 \
-v qdrant_storage:/qdrant/storage \
qdrant/qdrant
```

Verify:

```
http://localhost:6333/dashboard
```

---

# Running the Server

```bash
python server.py
```

or

```bash
mcp run server.py
```

---

# Available MCP Tools

## 1. upload

Uploads and indexes a document.

**Input**

```json
{
    "file_path": "sample.txt"
}
```

---

## 2. search

Searches indexed documents using semantic similarity.

**Input**

```json
{
    "query": "leave policy"
}
```

---

## 3. summarize

Generates a concise summary of a document.

**Input**

```json
{
    "filename": "sample.txt"
}
```

---

## 4. list_documents

Returns all uploaded documents.

---

## 5. document_info

Returns metadata for a document.

**Input**

```json
{
    "filename": "sample.txt"
}
```

---

## 6. delete

Deletes a document and removes its embeddings.

**Input**

```json
{
    "filename": "sample.txt"
}
```

---

## 7. statistics

Returns document statistics.

Example output:

```json
{
    "total_documents": 5,
    "total_chunks": 42,
    "storage_used": "1.8 MB"
}
```

---

# Workflow

```
Upload Document
        │
        ▼
Extract Text
        │
        ▼
Generate Embeddings
        │
        ▼
Store Metadata → PostgreSQL
        │
Store Embeddings → Qdrant
        │
        ▼
Semantic Search / Summary / Statistics
```

---

# Example Usage

Upload a document:

```python
from tools.upload import upload_document

upload_document("sample.txt")
```

Search documents:

```python
from tools.search import search_documents_tool

search_documents_tool("company leave policy")
```

Generate summary:

```python
from tools.summary import summarize_document

summarize_document("sample.txt")
```
