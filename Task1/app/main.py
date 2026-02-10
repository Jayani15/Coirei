from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from . import crud, models, schemas
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app with enhanced metadata
app = FastAPI(
    title="Task Management API",
    description="""
    A simple and efficient Task Management API built with FastAPI.
    
    ## Features
    
    * **Create tasks** with title, description, and priority
    * **Read tasks** with filtering and pagination
    * **Update tasks** including marking as complete
    * **Delete tasks** when no longer needed
    
    ## Authentication
    
    Currently, this API does not require authentication (for demo purposes).
    In production, you would add JWT token authentication.
    
    ## Rate Limiting
    
    The GET /tasks endpoint is rate-limited to 10 requests per minute per IP address.
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@taskapi.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API health check
    
    Returns a welcome message and API status.
    """
    return {
        "message": "Welcome to Task Management API",
        "status": "running",
        "docs": "/docs"
    }

@app.post(
    "/tasks",
    response_model=schemas.Task,
    status_code=201,
    tags=["Tasks"],
    summary="Create a new task",
    description="Create a new task with title, description, and priority level.",
    responses={
        201: {
            "description": "Task successfully created",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful task creation",
                            "value": {
                                "id": 1,
                                "title": "Buy groceries",
                                "description": "Buy milk, eggs, and bread",
                                "completed": False,
                                "priority": "high",
                                "created_at": "2024-02-05T10:30:00",
                                "updated_at": None
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation error - invalid input data"
        }
    }
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new task with the following information:
    
    - **title**: Task title (required, 1-100 characters)
    - **description**: Detailed description (optional, max 500 characters)
    - **priority**: Priority level - "low", "medium", or "high" (default: "medium")
    
    Returns the created task with assigned ID and timestamps.
    """
    return crud.create_task(db=db, task=task)

@app.get(
    "/tasks",
    response_model=List[schemas.Task],
    tags=["Tasks"],
    summary="Retrieve list of tasks",
    description="Get a paginated list of tasks with optional filtering by completion status.",
    responses={
        200: {
            "description": "List of tasks retrieved successfully",
            "content": {
                "application/json": {
                    "examples": {
                        "all_tasks": {
                            "summary": "All tasks",
                            "value": [
                                {
                                    "id": 1,
                                    "title": "Buy groceries",
                                    "description": "Buy milk and eggs",
                                    "completed": False,
                                    "priority": "high",
                                    "created_at": "2024-02-05T10:30:00",
                                    "updated_at": None
                                },
                                {
                                    "id": 2,
                                    "title": "Finish report",
                                    "description": "Complete Q4 report",
                                    "completed": True,
                                    "priority": "medium",
                                    "created_at": "2024-02-04T09:15:00",
                                    "updated_at": "2024-02-05T11:00:00"
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
)

@limiter.limit("3/minute")  # Rate limiting: 3 requests per minute
def read_tasks(
    request: Request,
    skip: int = Query(0, ge=0, description="Number of tasks to skip (for pagination)"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of tasks to return (max 100)"),
    completed: Optional[bool] = Query(None, description="Filter by completion status (true/false)"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of tasks with pagination and filtering options.
    
    **Rate Limited**: 10 requests per minute per IP address.
    
    - **skip**: Number of tasks to skip (for pagination, default: 0)
    - **limit**: Maximum number of tasks to return (1-100, default: 10)
    - **completed**: Filter by completion status (optional)
        - `true`: Only completed tasks
        - `false`: Only incomplete tasks
        - Not specified: All tasks
    
    Returns a list of tasks ordered by creation date (newest first).
    """
    tasks = crud.get_tasks(db, skip=skip, limit=limit, completed=completed)
    return tasks

@app.get(
    "/tasks/{task_id}",
    response_model=schemas.Task,
    tags=["Tasks"],
    summary="Get a specific task",
    description="Retrieve detailed information about a specific task by its ID.",
    responses={
        200: {
            "description": "Task found and returned successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Buy groceries",
                        "description": "Buy milk and eggs",
                        "completed": False,
                        "priority": "high",
                        "created_at": "2024-02-05T10:30:00",
                        "updated_at": None
                    }
                }
            }
        },
        404: {
            "description": "Task not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Task not found"}
                }
            }
        }
    }
)
def read_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific task.
    
    - **task_id**: The unique identifier of the task
    
    Returns the task if found, otherwise returns 404 error.
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.put(
    "/tasks/{task_id}",
    response_model=schemas.Task,
    tags=["Tasks"],
    summary="Update a task",
    description="Update one or more fields of an existing task.",
    responses={
        200: {
            "description": "Task updated successfully",
            "content": {
                "application/json": {
                    "examples": {
                        "mark_complete": {
                            "summary": "Mark task as complete",
                            "value": {
                                "id": 1,
                                "title": "Buy groceries",
                                "description": "Buy milk and eggs",
                                "completed": True,
                                "priority": "high",
                                "created_at": "2024-02-05T10:30:00",
                                "updated_at": "2024-02-05T15:45:00"
                            }
                        }
                    }
                }
            }
        },
        404: {"description": "Task not found"}
    }
)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing task. You can update any combination of fields:
    
    - **title**: New title for the task
    - **description**: New description
    - **completed**: Mark as complete (true) or incomplete (false)
    - **priority**: Change priority level
    
    Only provided fields will be updated; others remain unchanged.
    """
    db_task = crud.update_task(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    tags=["Tasks"],
    summary="Delete a task",
    description="Permanently delete a task from the system.",
    responses={
        204: {"description": "Task successfully deleted"},
        404: {
            "description": "Task not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Task not found"}
                }
            }
        }
    }
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Permanently delete a task.
    
    - **task_id**: The unique identifier of the task to delete
    
    Returns 204 No Content on success, 404 if task doesn't exist.
    """
    db_task = crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return JSONResponse(status_code=204, content={})