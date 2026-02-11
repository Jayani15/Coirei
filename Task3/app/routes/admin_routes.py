"""
Admin routes: manage all users and files
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List
import os

from app.core.database import get_db
from app.core.security import get_current_admin_user
from app.models.user import User
from app.models.file import File
from app.schemas.user_schema import UserResponse
from app.schemas.file_schema import FileResponse, FileListResponse

router = APIRouter()


@router.get("/users", response_model=List[UserResponse])
async def list_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """List all users (Admin only)"""
    query = select(User).offset(skip).limit(limit).order_by(desc(User.created_at))
    result = await db.execute(query)
    users = result.scalars().all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get user by ID (Admin only)"""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user


@router.patch("/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Activate a user account (Admin only)"""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.is_active = True
    await db.commit()
    
    return {"message": f"User {user.email} activated successfully"}


@router.patch("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Deactivate a user account (Admin only)"""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.id == current_admin.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot deactivate your own account")
    
    user.is_active = False
    await db.commit()
    
    return {"message": f"User {user.email} deactivated successfully"}


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Delete a user (Admin only)"""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.id == current_admin.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete your own account")
    
    await db.delete(user)
    await db.commit()
    
    return None


@router.get("/files", response_model=FileListResponse)
async def list_all_files(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user_id: int = Query(None),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """List all files in the system (Admin only)"""
    offset = (page - 1) * page_size
    
    count_query = select(func.count(File.id))
    files_query = select(File).offset(offset).limit(page_size).order_by(desc(File.created_at))
    
    if user_id:
        count_query = count_query.filter(File.owner_id == user_id)
        files_query = files_query.filter(File.owner_id == user_id)
    
    result = await db.execute(count_query)
    total = result.scalar()
    
    result = await db.execute(files_query)
    files = result.scalars().all()
    
    total_pages = (total + page_size - 1) // page_size
    
    return FileListResponse(
        files=files,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_any_file(
    file_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Delete any file (Admin only)"""
    result = await db.execute(select(File).filter(File.id == file_id))
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    if os.path.exists(file.file_path):
        os.remove(file.file_path)
    
    await db.delete(file)
    await db.commit()
    
    return None


@router.get("/stats/system")
async def get_system_stats(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get system-wide statistics (Admin only)"""
    user_count_result = await db.execute(select(func.count(User.id)))
    total_users = user_count_result.scalar()
    
    file_count_result = await db.execute(select(func.count(File.id)))
    total_files = file_count_result.scalar()
    
    storage_result = await db.execute(select(func.sum(File.file_size)))
    total_storage = storage_result.scalar() or 0
    
    active_users_result = await db.execute(select(func.count(User.id)).filter(User.is_active == True))
    active_users = active_users_result.scalar()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_files": total_files,
        "total_storage_bytes": total_storage,
        "total_storage_mb": round(total_storage / (1024 * 1024), 2)
    }