"""
Database Configuration

Configuration and initialization for the Banking RAG System database.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask
from dotenv import load_dotenv
from .banking_models import Base

# Load environment variables
load_dotenv()

# Global database session maker
SessionLocal = None
engine = None

class DatabaseConfig:
    """Database configuration management."""
    
    @staticmethod
    def get_database_url():
        """Get database URL from environment or default to SQLite."""
        # Check for environment variable first
        db_url = os.getenv('DATABASE_URL')
        
        if db_url:
            return db_url
        
        # Default to SQLite
        db_path = os.path.join(os.path.dirname(__file__), '../../data/chat_history.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        return f"sqlite:///{os.path.abspath(db_path)}"
    
    @staticmethod
    def create_engine_and_session():
        """Create SQLAlchemy engine and session maker."""
        database_url = DatabaseConfig.get_database_url()
        
        # SQLite specific configuration
        if database_url.startswith('sqlite'):
            engine = create_engine(
                database_url,
                echo=False,
                pool_pre_ping=True,
                connect_args={"check_same_thread": False}
            )
        # PostgreSQL specific configuration
        elif database_url.startswith('postgresql'):
            engine = create_engine(
                database_url,
                echo=False,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
                pool_recycle=3600,
                connect_args={
                    "connect_timeout": 10,
                    "application_name": "banking_rag_system"
                }
            )
        else:
            # Other databases (MySQL, etc.)
            engine = create_engine(
                database_url,
                echo=False,
                pool_pre_ping=True
            )
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        return engine, SessionLocal
    
    @staticmethod
    def init_database():
        """Initialize database tables."""
        engine, _ = DatabaseConfig.create_engine_and_session()
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")

def init_db(app: Flask = None):
    """
    Initialize database for Flask application.
    
    Args:
        app: Flask application instance (optional)
    """
    global engine, SessionLocal
    
    try:
        engine, SessionLocal = DatabaseConfig.create_engine_and_session()
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        if app:
            # Store database components in app config for easy access
            app.config['DATABASE_ENGINE'] = engine
            app.config['DATABASE_SESSION'] = SessionLocal
        
        return True
        
    except Exception as e:
        print(f"Database initialization failed: {str(e)}")
        raise e

def get_db_session():
    """Get a database session."""
    global SessionLocal
    if SessionLocal is None:
        _, SessionLocal = DatabaseConfig.create_engine_and_session()
    return SessionLocal()

# For compatibility with existing imports
db = SessionLocal

if __name__ == "__main__":
    # Initialize database when run as script
    DatabaseConfig.init_database()
