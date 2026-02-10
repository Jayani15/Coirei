# 🗂️ Secure File Management & Sharing API

A production-ready FastAPI backend for secure file upload, storage, and sharing using JWT authentication and role-based access control.

## ✨ Features

- JWT Authentication (Admin & User roles)
- Secure async file upload and download
- File size and type validation
- File metadata stored in database
- Role-based access (users can access only their files)
- Secure download endpoints / pre-signed URLs
- Background virus scan (mock)
- Rate limiting for upload and download APIs
- File versioning (optional)
- File expiry and auto-cleanup (optional)
- AES encryption before storage
- Docker support

---

## 🚀 Quick Start

### Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
Run Application
uvicorn app.main:app --reload
```

API will be available at:
http://localhost:8000

API Documentation:

Swagger UI: /docs

ReDoc: /redoc

### 🔐 API Usage (Basic)
---
Register
POST /api/v1/auth/register

Login
POST /api/v1/auth/login

Upload File
POST /api/v1/files/upload
Authorization: Bearer <access_token>

Download File
GET /api/v1/files/{id}/download
Authorization: Bearer <access_token>

---

### 📊 Main Endpoints
```bash
Authentication

POST /auth/register

POST /auth/login

GET /auth/me

Files

POST /files/upload

GET /files/

GET /files/{id}

GET /files/{id}/download

DELETE /files/{id}

Admin

GET /admin/users

GET /admin/files

DELETE /admin/files/{id}

```

### 🐳 Docker
---
docker build -t file-management-api .
docker run -p 8000:8000 file-management-api

### 📁 Project Structure
app/
├── core/        # Config, database, security
├── models/      # Database models
├── schemas/     # Pydantic schemas
├── routes/      # API routes
├── services/    # Business logic
├── middleware/  # Rate limiting
├── utils/       # Utility helpers
└── main.py      # FastAPI app entry point

---

### 🔒 Security
```bash
Password hashing (bcrypt)

JWT-based authentication

Role-based access control

Rate limiting

File validation and encryption
```