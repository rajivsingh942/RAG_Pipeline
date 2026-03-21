"""
Base Data Source Connector
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Document:
    """Document data model"""
    id: str
    content: str
    source: str
    source_type: str  # file, database, sharepoint, etc
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    embeddings: Optional[List[float]] = None


class BaseConnector(ABC):
    """Abstract base class for data source connectors"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.source_name = config.get("name", "unknown")
    
    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to data source"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from data source"""
        pass
    
    @abstractmethod
    async def load_documents(self) -> List[Document]:
        """Load all documents from source"""
        pass
    
    @abstractmethod
    async def search(self, query: str) -> List[Document]:
        """Search documents in source"""
        pass
    
    @abstractmethod
    async def validate_connection(self) -> bool:
        """Validate connection to data source"""
        pass
