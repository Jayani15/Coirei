"""
File routes: upload, download, list, delete
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File as FastAPIFile, BackgroundTasks, Query
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime, timedelta
import os
import uuid

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.file import File, FileStatus
from app.schemas.file_schema import (
    FileResponse,
    FileListResponse,
    FileUploadResponse,
    PresignedUrlResponse,
    FileStatsResponse
)
from app.services.file_service import validate_file, save_file, generate_presigned_url, scan_file_for_viruses
from app.utils.file_utils import get_file_extension, calculate_checksum

router = APIRouter()


@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = FastAPIFile(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a file"""
    # Validate file
    await validate_file(file)
    
    # Generate unique filename
    file_extension = get_file_extension(file.filename)
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, str(current_user.id))
    
    # Create user directory if doesn't exist
    os.makedirs(file_path, exist_ok=True)
    
    full_path = os.path.join(file_path, unique_filename)
    
    # Save file
    file_size = await save_file(file, full_path)
    
    # Calculate checksum
    checksum = await calculate_checksum(full_path)
    
    # Set expiry if enabled
    expires_at = None
    if settings.ENABLE_FILE_EXPIRY:
        expires_at = datetime.utcnow() + timedelta(days=settings.DEFAULT_FILE_EXPIRY_DAYS)
    
    # Create database record
    db_file = File(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=full_path,
        file_size=file_size,
        file_type=file.content_type,
        file_extension=file_extension,
        status=FileStatus.SCANNING,
        checksum=checksum,
        owner_id=current_user.id,
        expires_at=expires_at
    )
    
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    
    # Add background task for virus scanning
    if settings.ENABLE_VIRUS_SCAN:
        background_tasks.add_task(scan_file_for_viruses, db_file.id, full_path)
    else:
        db_file.status = FileStatus.SAFE
        await db.commit()
    
    return FileUploadResponse(
        id=db_file.id,
        filename=db_file.original_filename,
        file_size=db_file.file_size,
        file_type=db_file.file_type,
        status=db_file.status,
        message="File uploaded successfully. Virus scan in progress." if settings.ENABLE_VIRUS_SCAN else "File uploaded successfully."
    )


@router.get("/", response_model=FileListResponse)
async def list_files(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all files owned by current user"""
    offset = (page - 1) * page_size
    
    # Get total count
    count_query = select(func.count(File.id)).filter(File.owner_id == current_user.id)
    result = await db.execute(count_query)
    total = result.scalar()
    
    # Get files
    query = (
        select(File)
        .filter(File.owner_id == current_user.id)
        .order_by(desc(File.created_at))
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    files = result.scalars().all()
    
    total_pages = (total + page_size - 1) // page_size
    
    return FileListResponse(
        files=files,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get("/public/download",include_in_schema=False)
async def public_download(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    from app.core.security import decode_token
    
    try:
        payload = decode_token(token)
        file_id = int(payload.get("file_id"))
    except:
        raise HTTPException(status_code=403, detail="Invalid or expired link")
    
    result = await db.execute(select(File).filter(File.id == file_id))
    file = result.scalar_one_or_none()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    if not os.path.exists(file.file_path):
        raise HTTPException(status_code=404, detail="File missing on server")

    return FastAPIFileResponse(
        path=file.file_path,
        filename=file.original_filename,
        media_type=file.file_type
    )

@router.get("/{file_id}", response_model=FileResponse)
async def get_file_info(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get file metadata by ID"""
    result = await db.execute(select(File).filter(File.id == file_id))
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to access this file")
    
    return file


@router.get("/{file_id}/download")
async def download_file(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download a file"""
    result = await db.execute(select(File).filter(File.id == file_id))
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to download this file")
    
    if file.status == FileStatus.INFECTED:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="File is infected and cannot be downloaded")
    
    if not os.path.exists(file.file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found on server")
    
    # Update download count
    file.download_count += 1
    file.last_accessed_at = datetime.utcnow()
    await db.commit()
    
    return FastAPIFileResponse(
        path=file.file_path,
        filename=file.original_filename,
        media_type=file.file_type
    )

@router.get("/{file_id}/presigned-url", response_model=PresignedUrlResponse)
async def get_presigned_url(
    file_id: int,
    expires_in: int = Query(3600, ge=60, le=86400),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a pre-signed URL for file download"""
    result = await db.execute(select(File).filter(File.id == file_id))
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to access this file")
    
    presigned_url = generate_presigned_url(file.id, expires_in)
    
    return PresignedUrlResponse(
        url=presigned_url,
        expires_in=expires_in,
        file_id=file.id,
        filename=file.original_filename
    )


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a file"""
    result = await db.execute(select(File).filter(File.id == file_id))
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this file")
    
    # Delete file from storage
    if os.path.exists(file.file_path):
        os.remove(file.file_path)
    
    await db.delete(file)
    await db.commit()
    
    return None


@router.get("/stats/overview", response_model=FileStatsResponse)
async def get_file_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get file statistics for current user"""
    result = await db.execute(select(File).filter(File.owner_id == current_user.id))
    files = result.scalars().all()
    
    total_files = len(files)
    total_size = sum(f.file_size for f in files)
    
    file_types = {}
    for file in files:
        file_types[file.file_type] = file_types.get(file.file_type, 0) + 1
    
    status_counts = {}
    for file in files:
        status_counts[file.status.value] = status_counts.get(file.status.value, 0) + 1
    
    return FileStatsResponse(
        total_files=total_files,
        total_size=total_size,
        file_types=file_types,
        status_counts=status_counts
    )