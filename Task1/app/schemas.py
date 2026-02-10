from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    """Base schema for task data"""
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Title of the task",
        examples=["Buy groceries"]
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Detailed description of the task",
        examples=["Buy milk, eggs, and bread from the store"]
    )
    priority: str = Field(
        default="medium",
        description="Priority level of the task",
        examples=["high", "medium", "low"]
    )

class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    pass

class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = Field(None, description="Mark task as completed or not")
    priority: Optional[str] = None

class Task(TaskBase):
    """Schema for task response with all fields"""
    id: int = Field(..., description="Unique identifier for the task", examples=[1])
    completed: bool = Field(..., description="Whether the task is completed", examples=[False])
    created_at: datetime = Field(..., description="Timestamp when task was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when task was last updated")

    class Config:
        from_attributes = True