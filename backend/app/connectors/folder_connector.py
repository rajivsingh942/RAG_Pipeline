"""
Folder/File System Connector
"""
import os
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from .base import BaseConnector, Document
from .file_processor import FileProcessor


class FolderConnector(BaseConnector):
    """Connect to local folder or network drive"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.folder_path = config.get("path")
        self.file_processor = FileProcessor()
        self.supported_extensions = config.get(
            "extensions",
            ["pdf", "txt", "docx", "doc", "pptx", "xlsx", "csv"]
        )
        self.recursive = config.get("recursive", True)
    
    async def connect(self) -> bool:
        """Verify folder exists and is accessible"""
        try:
            return await self.validate_connection()
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """No cleanup needed for folder connector"""
        return True
    
    async def validate_connection(self) -> bool:
        """Check if folder exists and is readable"""
        path = Path(self.folder_path)
        return path.exists() and path.is_dir() and os.access(path, os.R_OK)
    
    async def load_documents(self) -> List[Document]:
        """Load all documents from folder"""
        documents = []
        path = Path(self.folder_path)
        
        if self.recursive:
            file_paths = path.rglob("*")
        else:
            file_paths = path.glob("*")
        
        for file_path in file_paths:
            if file_path.is_file():
                ext = file_path.suffix.lstrip(".").lower()
                if ext in self.supported_extensions:
                    try:
                        doc = await self._process_file(file_path)
                        if doc:
                            documents.append(doc)
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
        
        return documents
    
    async def search(self, query: str) -> List[Document]:
        """Search in file names and metadata"""
        all_docs = await self.load_documents()
        query_lower = query.lower()
        
        results = [
            doc for doc in all_docs
            if query_lower in doc.content.lower()
            or query_lower in doc.metadata.get("filename", "").lower()
        ]
        
        return results[:10]  # Limit results
    
    async def _process_file(self, file_path: Path) -> Optional[Document]:
        """Process a single file"""
        try:
            content = await self.file_processor.process(file_path)
            
            if not content:
                return None
            
            doc_id = self._generate_id(file_path)
            stat = file_path.stat()
            
            return Document(
                id=doc_id,
                content=content,
                source=str(file_path),
                source_type="file",
                metadata={
                    "filename": file_path.name,
                    "file_type": file_path.suffix,
                    "size": stat.st_size,
                    "path": str(file_path),
                },
                created_at=datetime.fromtimestamp(stat.st_ctime),
                updated_at=datetime.fromtimestamp(stat.st_mtime),
            )
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return None
    
    def _generate_id(self, file_path: Path) -> str:
        """Generate unique document ID"""
        content = f"{file_path}_{file_path.stat().st_mtime}"
        return hashlib.md5(content.encode()).hexdigest()
