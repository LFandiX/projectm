"""Run this script ONCE to initialize the database schema."""
from app import create_app
from services.db import init_db

app = create_app()
init_db(app)
print("✅ Database initialized successfully!")
