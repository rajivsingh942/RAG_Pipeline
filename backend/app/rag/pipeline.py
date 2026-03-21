"""
RAG Pipeline - Core retrieval and generation logic
"""
import logging
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
import hashlib

from sentence_transformers import SentenceTransformer
import numpy as np

from ..connectors import Document
from ..llms import BaseLLM
from .vector_store import VectorStore
from ..config import get_settings

logger = logging.getLogger(__name__)


class SimpleTextSplitter:
    """Simple text splitter for documents"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        if len(text) < self.chunk_size:
            return [text]
        
        chunks = []
        overlap_start = max(0, self.chunk_size - self.chunk_overlap)
        start = 0
        
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end]
            chunks.append(chunk)
            
            if end >= len(text):
                break
            
            start = start + overlap_start
        
        return chunks


class RAGPipeline:
    """Core RAG pipeline for retrieval and generation"""
    
    def __init__(self, llm: BaseLLM, vector_store: VectorStore):
        self.llm = llm
        self.vector_store = vector_store
        self.settings = get_settings()
        
        # Initialize text splitter
        self.text_splitter = SimpleTextSplitter(
            chunk_size=self.settings.CHUNK_SIZE,
            chunk_overlap=self.settings.CHUNK_OVERLAP,
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(
            self.settings.DEFAULT_EMBEDDING_MODEL
        )
        
        # System prompt for RAG
        self.system_prompt = """You are an intelligent assistant with access to specific documents and knowledge bases. 
Your role is to:
1. Answer questions based on the provided context
2. Cite sources when using information from documents
3. Be honest about what information is not available in your knowledge base
4. Provide clear, structured answers
5. If asked about something not in your knowledge base, say so explicitly

Always maintain context awareness and provide relevant, accurate information."""
    
    async def index_documents(self, documents: List[Document]) -> int:
        """Index documents into vector store"""
        chunks_added = 0
        
        for doc in documents:
            try:
                # Split document into chunks
                chunks = self.text_splitter.split_text(doc.content)
                
                for idx, chunk in enumerate(chunks):
                    # Generate embeddings
                    embedding = self.embedding_model.encode(chunk)
                    
                    # Prepare metadata
                    metadata = {
                        **doc.metadata,
                        "chunk_index": idx,
                        "document_id": doc.id,
                        "source": doc.source,
                        "source_type": doc.source_type,
                    }
                    
                    # Add to vector store
                    await self.vector_store.add(
                        text=chunk,
                        embedding=embedding.tolist(),
                        metadata=metadata,
                    )
                    
                    chunks_added += 1
                    
            except Exception as e:
                logger.error(f"Error indexing document {doc.id}: {e}")
                continue
        
        return chunks_added
    
    async def retrieve_context(self, query: str, top_k: Optional[int] = None) -> List[Tuple[str, float, Dict]]:
        """Retrieve relevant context from vector store"""
        if top_k is None:
            top_k = self.settings.TOP_K_RESULTS
        
        try:
            # Encode query
            query_embedding = self.embedding_model.encode(query)
            
            # Retrieve from vector store
            results = await self.vector_store.search(
                embedding=query_embedding.tolist(),
                top_k=top_k,
            )
            
            return results
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
    
    async def generate_answer(
        self,
        query: str,
        context: List[Tuple[str, float, Dict]],
        conversation_history: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
    ) -> str:
        """Generate answer based on query and context"""
        
        # Build context string with sources
        context_str = self._format_context(context)
        
        # Build conversation history for better context
        history_str = self._format_history(conversation_history)
        
        # Construct prompt
        prompt = f"""Based on the following context from your knowledge base, answer the user's question.

CONTEXT:
{context_str}

{history_str}

QUESTION: {query}

ANSWER:"""
        
        # Generate response
        response = await self.llm.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
            temperature=temperature,
            max_tokens=1000,
        )
        
        return response.content
    
    async def generate_answer_with_stream(
        self,
        query: str,
        context: List[Tuple[str, float, Dict]],
        conversation_history: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
    ):
        """Generate answer with streaming"""
        
        context_str = self._format_context(context)
        history_str = self._format_history(conversation_history)
        
        prompt = f"""Based on the following context from your knowledge base, answer the user's question.

CONTEXT:
{context_str}

{history_str}

QUESTION: {query}

ANSWER:"""
        
        async for chunk in self.llm.generate_with_stream(
            prompt=prompt,
            system_prompt=self.system_prompt,
            temperature=temperature,
            max_tokens=1000,
        ):
            yield chunk
    
    async def answer_question(
        self,
        query: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        use_stream: bool = False,
        temperature: float = 0.7,
    ):
        """Full RAG pipeline: retrieve and generate answer"""
        
        # Retrieve context
        context = await self.retrieve_context(query)
        
        if not context:
            yield "Sorry, I don't have relevant information to answer your question."
            return
        
        # Generate answer
        if use_stream:
            async for chunk in self.generate_answer_with_stream(
                query, context, conversation_history, temperature
            ):
                yield chunk
        else:
            answer = await self.generate_answer(
                query, context, conversation_history, temperature
            )
            yield answer
    
    def _format_context(self, context: List[Tuple[str, float, Dict]]) -> str:
        """Format context for prompt"""
        formatted = []
        
        for text, score, metadata in context:
            source = metadata.get("source", "Unknown")
            source_type = metadata.get("source_type", "document")
            
            formatted.append(f"""--- Source: {source} (Relevance: {score:.2f}) ---
{text}
""")
        
        return "\n".join(formatted)
    
    def _format_history(self, conversation_history: Optional[List[Dict]]) -> str:
        """Format conversation history for context"""
        if not conversation_history or len(conversation_history) < 2:
            return ""
        
        # Use last few exchanges
        recent_history = conversation_history[-4:]
        formatted = "Recent conversation:\n"
        
        for msg in recent_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted += f"{role.upper()}: {content}\n"
        
        return formatted
