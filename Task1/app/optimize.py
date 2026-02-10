"""
Database optimization script
Adds indexes to improve query performance
"""
from sqlalchemy import create_engine, text
import time

SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

def measure_query_performance(query, description):
    """Measure how long a query takes"""
    with engine.connect() as conn:
        start_time = time.time()
        result = conn.execute(text(query))
        result.fetchall()
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"{description}: {duration:.2f}ms")
        return duration

def add_indexes():
    """Add indexes to improve query performance"""
    with engine.connect() as conn:
        print("\n🔍 Checking current indexes...")
        
        # Check existing indexes
        indexes = conn.execute(text("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='tasks';"))
        print("Existing indexes:", [row[0] for row in indexes])
        
        print("\n📊 Performance BEFORE optimization:")
        # Test query performance before adding index
        measure_query_performance(
            "SELECT * FROM tasks WHERE completed = 0 ORDER BY created_at DESC LIMIT 10",
            "Query for incomplete tasks"
        )
        
        print("\n✨ Adding composite index...")
        # Add composite index on completed + created_at for faster filtering and sorting
        try:
            conn.execute(text(
                "CREATE INDEX IF NOT EXISTS idx_tasks_completed_created " 
                "ON tasks(completed, created_at DESC)"
            ))
            conn.commit()
            print("✅ Index 'idx_tasks_completed_created' created successfully")
        except Exception as e:
            print(f"❌ Error creating index: {e}")
        
        print("\n📊 Performance AFTER optimization:")
        # Test query performance after adding index
        measure_query_performance(
            "SELECT * FROM tasks WHERE completed = 0 ORDER BY created_at DESC LIMIT 10",
            "Query for incomplete tasks"
        )
        
        print("\n🎯 Optimization complete!")

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE QUERY OPTIMIZATION")
    print("=" * 60)
    add_indexes()