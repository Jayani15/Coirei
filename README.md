# 🚀 Event-Driven Analytics & Audit API

A high-throughput, event-driven backend system built with **FastAPI**, **Redis**, and **PostgreSQL**.

This system supports secure event ingestion, background processing, idempotency handling, analytics, and audit logging using a production-style architecture.

---

## 📌 Features

### 🔐 API Key–Based Authentication
- Each client has a unique API key.
- Requests must include `X-API-Key` header.

### 🚦 Rate Limiting (Per API Key)
- Configurable per-client rate limit.
- Prevents abuse and excessive traffic.

### ⚡ Async Event Ingestion
- Non-blocking FastAPI endpoint.
- Returns `202 Accepted` immediately.
- Designed for high-throughput ingestion.

### 🔁 Idempotency Protection
- Duplicate `event_id` values are ignored.
- Prevents double processing.

### 📦 Redis Queue Integration
- Events are pushed to Redis.
- Decouples ingestion from processing.

### 🧠 Background Worker
- Consumes events from Redis.
- Calculates processing latency.
- Persists enriched data into PostgreSQL.

### 🗄 PostgreSQL Storage
- Time-series–friendly schema.
- Indexed columns for performance.
- Bulk insert support.

### 📊 Analytics APIs
- Event count by type
- Filter by time range
- Group by client / event type

### 📝 Audit Logging
Logs every API call:
- Endpoint
- Method
- Status code
- Response time

### ❤️ Health Check Endpoint
- Verifies API & DB connectivity.

---

# 🏗 Architecture Overview

Client
↓
FastAPI (Auth + Rate Limit + Idempotency)
↓
Redis Queue
↓
Background Worker
↓
PostgreSQL
↓
Analytics APIs

---


---

# 🛠 Tech Stack

- FastAPI
- Redis
- PostgreSQL
- SQLAlchemy (Async)
- asyncpg
- Docker & Docker Compose

---

# 🚀 Setup & Run

## 1️⃣ Start Infrastructure

```bash
docker-compose up

Starts:

PostgreSQL
Redis

Start FastAPI
uvicorn app.main:app --reload

Insert Test Client

Connect to Postgres:

docker exec -it task6-db-1 psql -U postgres

INSERT INTO clients (name, api_key, is_active)
VALUES ('TestClient', 'test123', true);

```
---

## 🧠 Design Principles

-Event-driven architecture
-Async ingestion
-Queue-based decoupling
-Idempotent event handling
-Per-client rate limiting
-Background processing
-Time-series optimized storage
-Audit trail logging

---

---
## 🏁 Status

✔ Event ingestion
✔ API key authentication
✔ Rate limiting
✔ Redis queue
✔ Background worker
✔ PostgreSQL storage
✔ Analytics endpoints
✔ Audit logs
✔ Idempotency protection