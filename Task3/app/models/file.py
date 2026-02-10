"""
File database model
"""
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class FileStatus(str, enum.Enum):
    """File status enumeration"""
    UPLOADING = "uploading"
    SCANNING = "scanning"
    SAFE = "safe"
    INFECTED = "infected"
    FAILED = "failed"


class File(Base):
    """File model for storing file metadata"""
    
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger, nullable=False)  # Size in bytes
    file_type = Column(String(100), nullable=False)  # MIME type
    file_extension = Column(String(20), nullable=False)
    
    # File status and security
    status = Column(Enum(FileStatus), default=FileStatus.UPLOADING, nullable=False)
    is_encrypted = Column(Boolean, default=False, nullable=False)
    checksum = Column(String(64), nullable=True)  # SHA-256 hash
    
    # Versioning
    version = Column(Integer, default=1, nullable=False)
    parent_file_id = Column(Integer, ForeignKey("files.id"), nullable=True)
    
    # Expiry
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    last_accessed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Download tracking
    download_count = Column(Integer, default=0, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="files")
    versions = relationship("File", remote_side=[parent_file_id], backref="parent")
    
    def __repr__(self):
        return f"<File(id={self.id}, filename={self.filename}, owner_id={self.owner_id})>"