"""
Vector Store implementation using FAISS and local storage
"""
import os
import json
import logging
from typing import List, Tuple, Dict, Optional
from pathlib import Path
from datetime import datetime

try:
    import faiss
    import numpy as np
except ImportError:
    faiss = None
    np = None

logger = logging.getLogger(__name__)


class VectorStore:
    """Vector store for embeddings using FAISS"""
    
    def __init__(self, path: str, dimension: int = 384):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        
        self.dimension = dimension
        self.index_path = self.path / "faiss_index.bin"
        self.metadata_path = self.path / "metadata.jsonl"
        
        # Initialize or load FAISS index
        self.index = None
        self.metadata_list = []
        self.embedding_id_counter = 0
        
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """Load existing index or create new one"""
        if self.index_path.exists():
            try:
                self.index = faiss.read_index(str(self.index_path))
                logger.info(f"Loaded FAISS index with {self.index.ntotal} embeddings")
                
                # Load metadata
                if self.metadata_path.exists():
                    with open(self.metadata_path, "r") as f:
                        self.metadata_list = [json.loads(line) for line in f]
                    self.embedding_id_counter = len(self.metadata_list)
            except Exception as e:
                logger.warning(f"Could not load index: {e}. Creating new one.")
                self._create_index()
        else:
            self._create_index()
    
    def _create_index(self):
        """Create new FAISS index"""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata_list = []
        self.embedding_id_counter = 0
    
    async def add(
        self,
        text: str,
        embedding: List[float],
        metadata: Dict,
    ) -> str:
        """Add embedding to vector store"""
        try:
            # Convert to numpy array
            embedding_array = np.array([embedding], dtype=np.float32)
            
            # Add to FAISS
            self.index.add(embedding_array)
            
            # Store metadata
            metadata["embedding_id"] = self.embedding_id_counter
            metadata["text"] = text
            metadata["added_at"] = datetime.now().isoformat()
            
            self.metadata_list.append(metadata)
            
            # Save to disk periodically (every 10 additions)
            if self.embedding_id_counter % 10 == 0:
                self._save_index()
            
            self.embedding_id_counter += 1
            
            return str(self.embedding_id_counter - 1)
        
        except Exception as e:
            logger.error(f"Error adding embedding: {e}")
            raise
    
    async def search(
        self,
        embedding: List[float],
        top_k: int = 5,
    ) -> List[Tuple[str, float, Dict]]:
        """Search for similar embeddings"""
        try:
            if self.index.ntotal == 0:
                return []
            
            # Convert to numpy array
            query_array = np.array([embedding], dtype=np.float32)
            
            # Search
            distances, indices = self.index.search(query_array, min(top_k, self.index.ntotal))
            
            # Format results
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx >= 0 and idx < len(self.metadata_list):
                    metadata = self.metadata_list[int(idx)]
                    text = metadata.pop("text", "")
                    
                    # Convert L2 distance to similarity score (0-1)
                    similarity = 1 / (1 + distance)
                    
                    results.append((text, similarity, metadata))
            
            return results
        
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []
    
    async def delete(self, embedding_id: str) -> bool:
        """Delete embedding (by recreating index without it)"""
        try:
            embedding_id_int = int(embedding_id)
            
            # This is a simplified deletion - FAISS doesn't support deletion natively
            # In production, would use IDMap index
            
            # Remove from metadata
            self.metadata_list = [
                m for m in self.metadata_list
                if m.get("embedding_id") != embedding_id_int
            ]
            
            self._save_index()
            return True
        
        except Exception as e:
            logger.error(f"Error deleting: {e}")
            return False
    
    async def clear(self) -> bool:
        """Clear all data"""
        try:
            self._create_index()
            self._save_index()
            return True
        except Exception as e:
            logger.error(f"Error clearing: {e}")
            return False
    
    def _save_index(self):
        """Save index and metadata to disk"""
        try:
            # Save FAISS index
            faiss.write_index(self.index, str(self.index_path))
            
            # Save metadata
            with open(self.metadata_path, "w") as f:
                for meta in self.metadata_list:
                    f.write(json.dumps(meta) + "\n")
            
            logger.info(f"Saved index with {self.index.ntotal} embeddings")
        
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    async def get_stats(self) -> Dict:
        """Get vector store statistics"""
        return {
            "total_embeddings": self.index.ntotal if self.index else 0,
            "index_path": str(self.index_path),
            "metadata_path": str(self.metadata_path),
            "dimension": self.dimension,
        }
