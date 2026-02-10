"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.routes import auth_routes, file_routes, admin_routes, user_routes
from app.middleware.rate_limit import RateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    print("🚀 Starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")
    await engine.dispose()
    print("✅ Cleanup completed")


# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Secure File Management & Sharing API with JWT Authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting Middleware
app.add_middleware(RateLimitMiddleware)

# Include routers
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(user_routes.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(file_routes.router, prefix="/api/v1/files", tags=["Files"])
app.include_router(admin_routes.router, prefix="/api/v1/admin", tags=["Admin"])


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Secure File Management API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "database": "connected"}