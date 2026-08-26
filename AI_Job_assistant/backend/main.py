from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import create_tables
from chat import chat_with_ai
from auth import register_user, login_user

import os
import shutil
import uuid

from rag import add_job_description

app = FastAPI(title="AI Job Assistant")
create_tables()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuthRequest(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(request: AuthRequest):

    return register_user(
        request.username,
        request.password
    )

@app.post("/login")
def login(request: AuthRequest):

    return login_user(
        request.username,
        request.password
    )

class ChatRequest(BaseModel):
    message: str
    user_id: int = 1
    job_id: str | None = None

@app.get("/")
def home():
    return {
        "message": "AI Job Assistant is running!"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    response = chat_with_ai(
        request.message,
        request.user_id,
        request.job_id
    )

    return {
        "response": response
    }

@app.post("/upload-job")
async def upload_job(file: UploadFile = File(...)):

    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt"
    }

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        return {
            "error": "Only PDF, DOCX and TXT files are supported."
        }

    job_id = str(uuid.uuid4())

    upload_dir = "data/job_descriptions"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(
        upload_dir,
        f"{job_id}{extension}"
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = add_job_description(
        file_path,
        job_id
    )

    return {
        "message": "Job description uploaded successfully.",
        "job_id": job_id,
        "filename": file.filename,
        "chunks": result["chunks"]
    }