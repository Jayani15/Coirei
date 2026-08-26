# AI Job Assistant

A real-time AI-powered career assistant that helps users understand job descriptions, ask career-related questions, maintain conversation memory, and interact through text and voice.

## Features

- AI-powered conversational chatbot
- General question answering
- Job Description upload
- Retrieval-Augmented Generation (RAG)
- Job-specific question answering
- Short-term conversation memory
- Long-term user memory
- Persistent chat history
- User registration and login
- User-specific conversations
- PostgreSQL database
- ChromaDB vector database
- Groq LLM integration
- Voice input
- Voice output
- FastAPI REST API
- React + Vite frontend

## Technologies Used

### Frontend
- React
- Vite
- JavaScript
- HTML
- CSS

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy

### AI and RAG
- Groq
- Large Language Model
- Embeddings
- ChromaDB
- Retrieval-Augmented Generation

### Database
- PostgreSQL

### Voice
- Browser Speech Recognition
- Browser Speech Synthesis

## System Architecture

```text
                    React Frontend
                          |
                          | REST API
                          v
                    FastAPI Backend
                          |
             +------------+------------+
             |            |            |
             v            v            v
        PostgreSQL     ChromaDB     Groq LLM
             |            |            |
          Users        JD Data      AI Response
          Messages     Embeddings
          Memory       Retrieval
```

## Setup

- 1. Clone the Repository
git clone <repository-url>
cd AI_Job_assistant
- 2. Create Python Virtual Environment
python -m venv tasksenv

Activate it on Windows:

tasksenv\Scripts\activate
- 3. Install Backend Dependencies
pip install -r requirements.txt

If required:

pip install python-multipart
- 4. Configure Environment Variables

Create a .env file:

DATABASE_URL=postgresql://username:password@localhost:5433/ai_job_assistant
GROQ_API_KEY=your_groq_api_key

Replace the values with your own PostgreSQL credentials and Groq API key.

Do not commit the .env file or API keys to GitHub.

Add .env to .gitignore:

.env
PostgreSQL Setup

Create a PostgreSQL database named:

ai_job_assistant

Make sure PostgreSQL is running.

The application uses SQLAlchemy to create the required tables.

Main tables include:

users
messages
user_memory
Running the Backend

Open a terminal in the backend directory:

cd backend

Activate the virtual environment:

tasksenv\Scripts\activate

Start the FastAPI server:

uvicorn main:app --reload

Backend:

http://127.0.0.1:8000

FastAPI documentation:

http://127.0.0.1:8000/docs
Running the Frontend

Open another terminal:

cd frontend

Install dependencies:

npm install

Start the frontend:

npm run dev

Frontend:

http://localhost:5173
API Endpoints
Register
POST /register

Example:

{
  "username": "user1",
  "password": "password123"
}
Login
POST /login

Example:

{
  "username": "user1",
  "password": "password123"
}
Chat
POST /chat

Example:

{
  "message": "What skills are required?",
  "user_id": 1,
  "job_id": "job-id"
}
Upload Job Description
POST /upload-job

Supported formats:

.pdf
.docx
.txt
How to Use
1. Create an Account

Open the frontend and create a new account.

2. Login

Login using the registered username and password.

3. Upload a Job Description

Select a PDF, DOCX, or TXT job description and click Upload Job.

The document is processed and stored in the vector database.

4. Ask Questions

Example questions:

What skills are required for this position?
Is Python required?
What technologies are mentioned?
What are the main responsibilities?
What experience is expected?
5. Use Voice

Click the microphone button and speak a question.

The speech is converted into text, sent to the AI assistant, and the response can be spoken aloud.

Memory

The application provides multiple levels of memory.

Short-Term Memory

Maintains the current conversation context and allows the assistant to understand follow-up questions.

Long-Term Memory

Stores user-specific information in PostgreSQL.

Chat History

Previous messages are stored in PostgreSQL and associated with the user's unique ID.

Voice Workflow
User speaks
     |
     v
Speech Recognition
     |
     v
Text
     |
     v
Chat API
     |
     v
Groq LLM
     |
     v
AI Response
     |
     v
Speech Synthesis
     |
     v
Voice Output
Database

PostgreSQL is used for persistent application data.

The main database tables are:

users
messages
user_memory
Users

Stores registered users and authentication information.

Messages

Stores conversation history for each user.

User Memory

Stores persistent user-specific information.

Testing

The application can be tested through the FastAPI Swagger interface:

http://127.0.0.1:8000/docs

The main functionality can be tested using:

User registration
User login
Job Description upload
RAG-based questions
General chatbot questions
Conversation memory
Long-term memory
Voice input
Voice output
Application Workflow
```
                    User
                     |
                     v
              Login / Register
                     |
                     v
             AI Job Assistant
                     |
          +----------+----------+
          |                     |
          v                     v
      Upload JD                Chat
          |                     |
          v                     v
     RAG Pipeline        Memory Retrieval
          |                     |
          v                     |
       ChromaDB                |
          |                     |
          +----------+----------+
                     |
                     v
                  Groq LLM
                     |
                     v
                AI Response
                     |
                +----+----+
                |         |
                v         v
              Text      Voice
```
