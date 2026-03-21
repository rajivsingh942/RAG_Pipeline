"""
Database models for conversation history and data sources
"""
from sqlalchemy import Column, String, DateTime, Text, Integer, Boolean, JSON, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class DataSource(Base):
    """Data source configuration"""
    __tablename__ = "data_sources"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(255), nullable=False)
    source_type = Column(String(50), nullable=False)  # folder, database, sharepoint
    config = Column(JSON, nullable=False)
    indexed = Column(Boolean, default=False)
    last_indexed = Column(DateTime, nullable=True)
    document_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Conversation(Base):
    """Conversation thread"""
    __tablename__ = "conversations"
    
    id = Column(String(50), primary_key=True)
    title = Column(String(255), nullable=True)
    data_source_ids = Column(JSON, nullable=False)  # List of active data sources
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Message(Base):
    """Message in conversation"""
    __tablename__ = "messages"
    
    id = Column(String(50), primary_key=True)
    conversation_id = Column(String(50), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    
    # Sources used for this response
    sources = Column(JSON, nullable=True)
    
    # API details
    llm_model = Column(String(100), nullable=True)
    tokens_used = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class IndexSession(Base):
    """Indexing session tracking"""
    __tablename__ = "index_sessions"
    
    id = Column(String(50), primary_key=True)
    data_source_id = Column(String(50), ForeignKey("data_sources.id"), nullable=False)
    status = Column(String(20), nullable=False)  # running, completed, failed
    documents_processed = Column(Integer, default=0)
    chunks_created = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
