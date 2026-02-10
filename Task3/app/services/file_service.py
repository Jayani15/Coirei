"""
File service: validation, storage, virus scanning
"""
from fastapi import UploadFile, HTTPException, status
import aiofiles
import os
from datetime import datetime, timedelta
import asyncio

from app.core.config import settings
from app.core.security import create_access_token
from app.utils.file_utils import get_file_extension


async def validate_file(file: UploadFile) -> None:
    """Validate file size and type"""
    # Read file to get size
    contents = await file.read()
    file_size = len(contents)
    
    # Reset file pointer
    await file.seek(0)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )
    
    # Check file type
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_FILE_TYPES)}"
        )
    
    # Check file extension
    file_extension = get_file_extension(file.filename)
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File extension not allowed. Allowed extensions: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )


async def save_file(file: UploadFile, file_path: str) -> int:
    """Save uploaded file to disk"""
    file_size = 0
    
    async with aiofiles.open(file_path, 'wb') as f:
        while chunk := await file.read(1024 * 1024):  # Read in 1MB chunks
            await f.write(chunk)
            file_size += len(chunk)
    
    return file_size


def generate_presigned_url(file_id: int, expires_in: int = 3600) -> str:
    """Generate a pre-signed URL for file download"""
    token_data = {"file_id": file_id, "type": "download"}
    
    token = create_access_token(data=token_data, expires_delta=timedelta(seconds=expires_in))
    
    base_url = "http://localhost:8000"
    presigned_url = f"{base_url}/api/v1/files/download/{file_id}?token={token}"
    
    return presigned_url


async def scan_file_for_viruses(file_id: int, file_path: str) -> None:
    """Mock virus scan for uploaded files"""
    from app.core.database import AsyncSessionLocal
    from app.models.file import File, FileStatus
    from sqlalchemy import select
    
    # Simulate scanning delay
    await asyncio.sleep(2)
    
    # Mock scan result (always safe for demo)
    is_safe = True
    
    # Update file status in database
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(File).filter(File.id == file_id))
        file = result.scalar_one_or_none()
        
        if file:
            if is_safe:
                file.status = FileStatus.SAFE
                print(f"✅ File {file_id} scanned: SAFE")
            else:
                file.status = FileStatus.INFECTED
                print(f"⚠️ File {file_id} scanned: INFECTED")
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            await db.commit()


async def cleanup_expired_files() -> int:
    """Clean up expired files"""
    from app.core.database import AsyncSessionLocal
    from app.models.file import File
    from sqlalchemy import select
    
    deleted_count = 0
    
    async with AsyncSessionLocal() as db:
        now = datetime.utcnow()
        result = await db.execute(
            select(File).filter(File.expires_at.isnot(None), File.expires_at < now)
        )
        expired_files = result.scalars().all()
        
        for file in expired_files:
            if os.path.exists(file.file_path):
                os.remove(file.file_path)
            
            await db.delete(file)
            deleted_count += 1
        
        await db.commit()
        print(f"🗑️ Cleaned up {deleted_count} expired files")
    
    return deleted_count