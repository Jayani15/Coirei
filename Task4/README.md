# Event Booking & Management API

A FastAPI-based backend system for managing events and bookings with JWT authentication, role-based access control, PostgreSQL, Redis caching, and background tasks.

---

## 🚀 Features

- JWT Authentication (Admin, Organizer, Attendee)
- Role-Based Access Control
- CRUD APIs for Users, Events, and Bookings
- Prevents event overbooking
- Booking statuses: confirmed, cancelled, waitlisted
- Async SQLAlchemy with PostgreSQL
- Redis caching for event listings
- Pagination support
- Background tasks for:
  - Booking confirmation
  - Event reminders
- Clean Swagger/OpenAPI documentation

---

## 🛠 Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy (Async)
- Redis
- JWT (python-jose)
- Docker (optional)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd <project-folder>
2️⃣ Create Virtual Environment
python -m venv tasksenv
tasksenv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Configure Environment Variables
Create a .env file:

DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost/eventdb
REDIS_URL=redis://localhost:6379
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
5️⃣ Run PostgreSQL
Make sure PostgreSQL is running and database eventdb exists.

6️⃣ Run Redis (Docker Recommended)
docker run -d -p 6379:6379 redis
7️⃣ Start the Server
uvicorn app.main:app --reload
Open Swagger:

http://127.0.0.1:8000/docs

```
---
🔐 Authentication Flow
Register user

Login to get JWT token

Click "Authorize" in Swagger

Use protected endpoints

📌 API Highlights
Users
Register

Login

Get current user

List users (Admin only)

Events
Create event (Organizer/Admin)

List events (Cached)

Get event details

Delete event

Bookings
Create booking

Cancel booking

List my bookings

🧠 Business Logic
Automatically waitlists if event capacity is full

Prevents duplicate bookings

Enforces role-based access

Invalidates Redis cache when events change

📄 License
This project is for educational purposes.

---