# Real-Time AI Job Assistant

An AI-powered career assistant with:

- ChatGPT-like conversation
- Job Description Q&A
- RAG
- Persistent memory
- Voice interaction
- User authentication
- Chat history

## Architecture

User
↓
Chat Interface
↓
Backend
↓
Memory + RAG
↓
Prompt Builder
↓
LLM
↓
Response

## Setup

### Backend

```bash
cd backend
pip install -r ../requirements.txt
uvicorn main:app --reload