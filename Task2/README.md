# Attendance System API

A simple employee check-in/check-out system built with FastAPI.

## What it does

- Employees check in when they arrive at work
- Employees check out when they leave
- View attendance history for any employee
- Automatically calculates work duration

## Quick Start

### Run with Python
```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open: http://localhost:8000/docs

### Run with Docker
```
docker build -t attendance-api .
docker run -p 8000:8000 attendance-api
```

Then open: http://localhost:8000/docs

## How to Test

Go to http://localhost:8000/docs and try these steps:

1. **Check in** - POST `/check-in` with `{"employee_id": "EMP001"}`
2. **Try checking in again** - Should fail (already checked in)
3. **Check status** - GET `/status/EMP001` - Shows checked in
4. **Check out** - POST `/check-out` with `{"employee_id": "EMP001"}`
5. **View history** - GET `/attendance/EMP001` - Shows all records

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/check-in` | Check in an employee |
| POST | `/check-out` | Check out an employee |
| GET | `/attendance/{employee_id}` | Get attendance history |
| GET | `/status/{employee_id}` | Check current status |

## Rules

- Can't check in twice without checking out
- Can't check out without checking in first
- Employee ID cannot be empty

## Tech Stack

FastAPI • Python 3.11 • Uvicorn • Pydantic • Docker

## Note

Data is stored in memory and will be lost when the server restarts (no database).

## Project Structure
```
attendance-system/
├── app/
│   ├── main.py          # API endpoints
│   ├── models.py        # Request/response models
│   ├── schemas.py       # Data structures
│   └── services.py      # Business logic
├── Dockerfile
├── requirements.txt
└── README.md
```

---
