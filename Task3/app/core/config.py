"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Project Info
    PROJECT_NAME: str = "File Management API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./file_management.db"
    
    # File Upload Settings
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB in bytes
    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg", "image/png", "image/gif", "image/webp",
        "application/pdf", 
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/plain", "text/csv"
    ]
    ALLOWED_EXTENSIONS: List[str] = [
        ".jpg", ".jpeg", ".png", ".gif", ".webp",
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", 
        ".txt", ".csv"
    ]
    
    # Rate Limiting
    RATE_LIMIT_UPLOAD: int = 10  # uploads per hour
    RATE_LIMIT_DOWNLOAD: int = 50  # downloads per hour
    RATE_LIMIT_GENERAL: int = 100  # general requests per hour
    
    # File Expiry (in days)
    DEFAULT_FILE_EXPIRY_DAYS: int = 30
    ENABLE_FILE_EXPIRY: bool = False
    
    # Pre-signed URL Settings
    PRESIGNED_URL_EXPIRY_SECONDS: int = 3600  # 1 hour
    
    # Background Tasks
    ENABLE_VIRUS_SCAN: bool = True
    ENABLE_AUTO_CLEANUP: bool = False
    
    # Encryption
    ENABLE_ENCRYPTION: bool = False
    
    # File Versioning
    ENABLE_VERSIONING: bool = False
    MAX_VERSIONS: int = 5
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Admin User
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "admin123"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)