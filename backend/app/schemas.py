"""
Pydantic request/response models
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


# Data Source Models
class DataSourceConfig(BaseModel):
    """Base data source configuration"""
    name: str
    source_type: str  # folder, database, sharepoint
    config: Dict[str, Any]


class DataSourceResponse(BaseModel):
    """Data source response"""
    id: str
    name: str
    source_type: str
    indexed: bool
    document_count: int
    last_indexed: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Message Models
class MessageCreate(BaseModel):
    """Create message"""
    content: str
    role: str


class MessageResponse(BaseModel):
    """Message response"""
    id: str
    role: str
    content: str
    sources: Optional[List[Dict[str, Any]]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Conversation Models
class ConversationCreate(BaseModel):
    """Create conversation"""
    title: Optional[str] = None
    data_source_ids: List[str]


class ConversationResponse(BaseModel):
    """Conversation response"""
    id: str
    title: Optional[str] = None
    data_source_ids: List[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConversationWithMessages(ConversationResponse):
    """Conversation with messages"""
    messages: List[MessageResponse] = []


# Query Models
class QueryRequest(BaseModel):
    """Query request"""
    conversation_id: str
    message: str
    temperature: float = Field(0.7, ge=0, le=2)
    use_stream: bool = False


class QueryResponse(BaseModel):
    """Query response"""
    answer: str
    sources: List[Dict[str, Any]]
    tokens_used: Optional[int] = None
    cost: Optional[float] = None


# Indexing Models
class IndexRequest(BaseModel):
    """Request to index data source"""
    data_source_id: str


class IndexResponse(BaseModel):
    """Index response"""
    session_id: str
    status: str
    documents_processed: int
    chunks_created: int


# Settings Models
class LLMSettings(BaseModel):
    """LLM settings"""
    default_llm: str = Field("openai", description="Default LLM provider")
    default_temperature: float = Field(0.7, ge=0, le=2)
    max_tokens: int = Field(1000, ge=100, le=4000)


class RAGSettings(BaseModel):
    """RAG settings"""
    top_k_results: int = Field(5, ge=1, le=20)
    context_window: int = Field(3000, ge=500, le=10000)
    chunk_size: int = Field(1000, ge=100, le=2000)
    chunk_overlap: int = Field(200, ge=0, le=500)


class SearchRequest(BaseModel):
    """Search request"""
    query: str
    data_source_ids: List[str]
    top_k: int = 10


class SearchResult(BaseModel):
    """Search result"""
    text: str
    source: str
    source_type: str
    relevance_score: float
    metadata: Dict[str, Any]
