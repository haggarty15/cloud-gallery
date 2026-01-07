"""
Create database tables for the coloring app
"""
from app import app, db
from app.models import ColoringProject, ColoringSession, Image

def create_tables():
    """Create all database tables"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✓ Database tables created successfully")
            
            # List tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\nCreated tables:")
            for table in tables:
                print(f"  - {table}")
                
        except Exception as e:
            print(f"✗ Error creating tables: {e}")
            raise

if __name__ == '__main__':
    create_tables()
