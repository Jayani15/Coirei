from fastapi import FastAPI

from .database import Base, engine
from .routes import router

# Import models so SQLAlchemy knows about the tables
from . import models


app = FastAPI(
    title="AI-Powered Candidate Intelligence and Job Readiness Platform",
    description=(
        "AI-powered candidate profiling, gap detection, "
        "conversational profile completion, role recommendation, "
        "adaptive assessment and job-readiness benchmarking."
    ),
    version="2.0.0"
)


# Create PostgreSQL tables
Base.metadata.create_all(
    bind=engine
)


# API routes
app.include_router(
    router,
    prefix="/api"
)


@app.get("/")
def root():
    return {
        "message": "AI Resume Assessment API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }