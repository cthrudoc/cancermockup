from app import create_app
from models import db, Patient
from sqlalchemy import inspect

app = create_app()

def initialize_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Verify Patient table exists (modern method)
        inspector = inspect(db.engine)
        if 'patient' in inspector.get_table_names():
            print("✅ Patient table exists")
        else:
            print("❌ Patient table NOT created - check model definition")

if __name__ == '__main__':
    initialize_database()