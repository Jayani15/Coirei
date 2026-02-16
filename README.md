# 🛍 Product Management API

A RESTful Product Management Service built using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**.

This API allows users to create, read, update, and delete products with proper validation and pagination support.

---

## 🚀 Tech Stack

- **FastAPI** – Web framework
- **PostgreSQL** – Database
- **SQLAlchemy** – ORM
- **Pydantic** – Data validation
- **Alembic** – Database migrations
- **Uvicorn** – ASGI server

---

## 📂 Project Structure

```
fastapi-products/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── deps.py
│   └── routers/
│       └── products.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── alembic.ini
├── requirements.txt
└── .env
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd fastapi-products
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup PostgreSQL

Create a database:

```sql
CREATE DATABASE products_db;
```

---

### 5️⃣ Configure Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/products_db
```

---

### 6️⃣ Run Migrations

```bash
alembic revision --autogenerate -m "create products table"
alembic upgrade head
```

---

### 7️⃣ Start the Server

```bash
uvicorn app.main:app --reload
```

API will run at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

### Health Check
```
GET /health
```

---

### Create Product
```
POST /products/
```

---

### Get All Products (with pagination)
```
GET /products/?skip=0&limit=10
```

---

### Get Product by ID
```
GET /products/{id}
```

---

### Update Product
```
PUT /products/{id}
```

---

### Delete Product
```
DELETE /products/{id}
```

---

## 🔍 Validation Rules

- `price` must be **greater than 0**
- `stock` cannot be **negative**
- `name` is **unique**

---

## 🗄 Database Schema

| Column      | Type      | Constraints          |
|------------|----------|----------------------|
| id         | Integer  | Primary Key          |
| name       | String   | Unique               |
| description| String   | Optional             |
| price      | Float    | > 0                  |
| stock      | Integer  | >= 0                 |
| category   | String   | Optional             |
| created_at | DateTime | Auto-generated       |

---

## 📄 Features

- CRUD operations
- Pagination support
- Input validation with Pydantic
- Unique constraint on product name
- Database migrations using Alembic
- Health monitoring endpoint
- Clean layered architecture

---

## 🧠 Architecture Overview

```
Client → FastAPI → Pydantic → SQLAlchemy → PostgreSQL
                           ↑
                        Alembic
```
