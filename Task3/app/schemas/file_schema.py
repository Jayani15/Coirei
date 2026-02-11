"""
Pydantic schemas for File model
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.file import FileStatus


class FileBase(BaseModel):
    """Base file schema"""
    filename: str
    file_size: int
    file_type: str


class FileCreate(FileBase):
    """Schema for file creation"""
    pass


class FileUpdate(BaseModel):
    """Schema for file update"""
    filename: Optional[str] = None


class FileResponse(BaseModel):
    """Schema for file response"""
    id: int
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    file_extension: str
    status: FileStatus
    is_encrypted: bool
    version: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_accessed_at: Optional[datetime] = None
    download_count: int
    expires_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class FileListResponse(BaseModel):
    """Schema for paginated file list"""
    files: list[FileResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)


class FileUploadResponse(BaseModel):
    """Schema for file upload response"""
    id: int
    filename: str
    file_size: int
    file_type: str
    status: FileStatus
    message: str
    
    model_config = ConfigDict(from_attributes=True)


class PresignedUrlResponse(BaseModel):
    """Schema for presigned URL response"""
    url: str
    expires_in: int
    file_id: int
    filename: str


class FileStatsResponse(BaseModel):
    """Schema for file statistics"""
    total_files: int
    total_size: int
    file_types: dict[str, int]
    status_counts: dict[str, int]