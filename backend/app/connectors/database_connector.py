"""
Database Connector (SQL, NoSQL databases)
"""
from typing import List, Dict, Any, Optional
from .base import BaseConnector, Document
import asyncio


class DatabaseConnector(BaseConnector):
    """Connect to SQL and NoSQL databases"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.db_type = config.get("type")  # mysql, postgresql, mongodb, etc
        self.connection_string = config.get("connection_string")
        self.query = config.get("query")
        self.text_column = config.get("text_column", "text")
        self.id_column = config.get("id_column", "id")
        self.connection = None
    
    async def connect(self) -> bool:
        """Establish database connection"""
        try:
            if self.db_type in ["mysql", "postgresql"]:
                return await self._connect_sql()
            elif self.db_type == "mongodb":
                return await self._connect_mongodb()
            return False
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """Close database connection"""
        if self.connection:
            try:
                await self.connection.close()
                return True
            except:
                return False
        return True
    
    async def validate_connection(self) -> bool:
        """Test database connection"""
        try:
            # Implementation depends on DB type
            return self.connection is not None
        except Exception:
            return False
    
    async def load_documents(self) -> List[Document]:
        """Load all documents from database"""
        try:
            if not self.connection:
                await self.connect()
            
            if self.db_type in ["mysql", "postgresql"]:
                return await self._load_sql_documents()
            elif self.db_type == "mongodb":
                return await self._load_mongo_documents()
                
            return []
        except Exception as e:
            print(f"Error loading documents: {e}")
            return []
    
    async def search(self, query: str) -> List[Document]:
        """Search documents in database"""
        try:
            if not self.connection:
                await self.connect()
            
            if self.db_type in ["mysql", "postgresql"]:
                return await self._search_sql(query)
            elif self.db_type == "mongodb":
                return await self._search_mongo(query)
                
            return []
        except Exception as e:
            print(f"Error searching database: {e}")
            return []
    
    async def _connect_sql(self) -> bool:
        """Connect to SQL database"""
        try:
            import asyncpg
            self.connection = await asyncpg.connect(self.connection_string)
            return True
        except ImportError:
            print("asyncpg not installed")
            return False
    
    async def _connect_mongodb(self) -> bool:
        """Connect to MongoDB"""
        try:
            from motor.motor_asyncio import AsyncClient
            self.connection = AsyncClient(self.connection_string)
            await self.connection.admin.command("ping")
            return True
        except ImportError:
            print("motor not installed")
            return False
    
    async def _load_sql_documents(self) -> List[Document]:
        """Load documents from SQL database"""
        documents = []
        try:
            rows = await self.connection.fetch(self.query)
            
            for row in rows:
                doc_id = str(row[self.id_column])
                content = str(row[self.text_column])
                
                doc = Document(
                    id=doc_id,
                    content=content,
                    source=f"{self.source_name}",
                    source_type="database",
                    metadata={
                        "db_type": self.db_type,
                        "row_id": doc_id,
                    }
                )
                documents.append(doc)
        except Exception as e:
            print(f"Error loading SQL documents: {e}")
        
        return documents
    
    async def _load_mongo_documents(self) -> List[Document]:
        """Load documents from MongoDB"""
        documents = []
        try:
            db_name = self.config.get("database")
            collection_name = self.config.get("collection")
            
            db = self.connection[db_name]
            collection = db[collection_name]
            
            async for doc in collection.find():
                doc_id = str(doc.get("_id", ""))
                content = str(doc.get(self.text_column, ""))
                
                rag_doc = Document(
                    id=doc_id,
                    content=content,
                    source=f"{self.source_name}",
                    source_type="database",
                    metadata={
                        "db_type": "mongodb",
                        "mongo_id": doc_id,
                    }
                )
                documents.append(rag_doc)
        except Exception as e:
            print(f"Error loading MongoDB documents: {e}")
        
        return documents
    
    async def _search_sql(self, query: str) -> List[Document]:
        """Search SQL database"""
        search_query = f"""
        {self.query}
        AND {self.text_column} ILIKE %s
        LIMIT 10
        """
        
        try:
            rows = await self.connection.fetch(search_query, f"%{query}%")
            return [Document(
                id=str(row[self.id_column]),
                content=str(row[self.text_column]),
                source=f"{self.source_name}",
                source_type="database",
            ) for row in rows]
        except Exception as e:
            print(f"Error searching SQL: {e}")
            return []
    
    async def _search_mongo(self, query: str) -> List[Document]:
        """Search MongoDB"""
        try:
            db_name = self.config.get("database")
            collection_name = self.config.get("collection")
            
            db = self.connection[db_name]
            collection = db[collection_name]
            
            documents = []
            async for doc in collection.find({
                self.text_column: {"$regex": query, "$options": "i"}
            }).limit(10):
                documents.append(Document(
                    id=str(doc.get("_id", "")),
                    content=str(doc.get(self.text_column, "")),
                    source=f"{self.source_name}",
                    source_type="database",
                ))
            
            return documents
        except Exception as e:
            print(f"Error searching MongoDB: {e}")
            return []
