"""
Database initialization and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from ..config import get_settings
from .models import Base


class Database:
    """Database manager"""
    
    def __init__(self):
        self.settings = get_settings()
        self.engine = None
        self.async_engine = None
        self.SessionLocal = None
        self.AsyncSessionLocal = None
    
    async def init_db(self):
        """Initialize database"""
        # Create tables
        engine = create_engine(self.settings.DATABASE_URL)
        Base.metadata.create_all(engine)
        engine.dispose()
    
    def get_session(self):
        """Get database session"""
        if not self.SessionLocal:
            engine = create_engine(self.settings.DATABASE_URL)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        return self.SessionLocal()


# Global database instance
database = Database()


async def get_db():
    """Get database session dependency"""
    db = database.get_session()
    try:
        yield db
    finally:
        db.close()
