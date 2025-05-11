from app import create_app
from models import db, Patient, Prediction
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    # Drop all tables
    db.drop_all()
    
    # Create all tables
    db.create_all()
    
    print("Database reset complete!")
    
    # Modern way to check tables
    inspector = inspect(db.engine)
    print("Existing tables:", inspector.get_table_names())