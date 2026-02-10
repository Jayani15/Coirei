"""
Seed the database with test data to demonstrate query performance
"""
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models
import random
from datetime import datetime, timedelta

def generate_test_tasks(db: Session, count: int = 1000):
    """Generate test tasks"""
    priorities = ["low", "medium", "high"]
    
    print(f"Generating {count} test tasks...")
    
    for i in range(count):
        task = models.Task(
            title=f"Task {i+1}",
            description=f"Description for task {i+1}",
            completed=random.choice([True, False]),
            priority=random.choice(priorities),
            created_at=datetime.now() - timedelta(days=random.randint(0, 365))
        )
        db.add(task)
        
        if i % 100 == 0:
            print(f"  Created {i} tasks...")
    
    db.commit()
    print(f"✅ Successfully created {count} tasks")

if __name__ == "__main__":
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if we already have data
        count = db.query(models.Task).count()
        if count > 0:
            print(f"Database already has {count} tasks")
            response = input("Do you want to delete existing data and recreate? (yes/no): ")
            if response.lower() == 'yes':
                db.query(models.Task).delete()
                db.commit()
                generate_test_tasks(db, 1000)
        else:
            generate_test_tasks(db, 1000)
    finally:
        db.close()