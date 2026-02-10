from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models, schemas

def get_tasks(db: Session, skip: int = 0, limit: int = 10, completed: bool = None):
    """Retrieve tasks with optional filtering"""
    query = db.query(models.Task)
    
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    
    return query.order_by(desc(models.Task.created_at)).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    """Retrieve a single task by ID"""
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def create_task(db: Session, task: schemas.TaskCreate):
    """Create a new task"""
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    """Update an existing task"""
    db_task = get_task(db, task_id)
    if db_task:
        update_data = task.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    """Delete a task"""
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task