"""
Main FastAPI Application
"""
import logging
import uuid
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import asyncio

from .config import get_settings
from .db import database, get_db, DataSource, Conversation, Message, IndexSession
from .connectors import get_connector, FolderConnector
from .llms import get_llm
from .rag import RAGPipeline, VectorStore
from .schemas import (
    DataSourceConfig, DataSourceResponse, QueryRequest, QueryResponse,
    ConversationCreate, ConversationResponse, ConversationWithMessages,
    MessageResponse, SearchRequest, SearchResult, IndexRequest, IndexResponse
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Settings
settings = get_settings()

# Initialize FastAPI
app = FastAPI(
    title="Smart RAG Pipeline",
    description="AI-powered document retrieval and generation",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
rag_pipeline = None
vector_store = None
active_llm = None


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    global rag_pipeline, vector_store, active_llm
    
    # Initialize database
    await database.init_db()
    logger.info("Database initialized")
    
    # Initialize vector store
    vector_store = VectorStore(settings.VECTOR_STORE_PATH)
    logger.info("Vector store initialized")
    
    # Initialize LLM
    active_llm = get_llm(
        settings.DEFAULT_LLM,
        getattr(settings, f"{settings.DEFAULT_LLM.upper()}_API_KEY"),
        getattr(settings, f"{settings.DEFAULT_LLM.upper()}_MODEL"),
    )
    logger.info(f"LLM initialized: {settings.DEFAULT_LLM}")
    
    # Initialize RAG pipeline
    rag_pipeline = RAGPipeline(active_llm, vector_store)
    logger.info("RAG pipeline initialized")


# ==================== Data Source Endpoints ====================

@app.post("/api/sources", response_model=DataSourceResponse)
async def add_data_source(source_config: DataSourceConfig, db=Depends(get_db)):
    """Add a new data source"""
    try:
        source_id = str(uuid.uuid4())
        
        # Validate connection
        connector = get_connector(source_config.source_type, source_config.config)
        is_connected = await connector.connect()
        
        if not is_connected:
            raise HTTPException(status_code=400, detail="Cannot connect to data source")
        
        await connector.disconnect()
        
        # Save to database
        db_source = DataSource(
            id=source_id,
            name=source_config.name,
            source_type=source_config.source_type,
            config=source_config.config,
        )
        db.add(db_source)
        db.commit()
        db.refresh(db_source)
        
        return DataSourceResponse.from_orm(db_source)
    
    except Exception as e:
        logger.error(f"Error adding data source: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sources", response_model=list[DataSourceResponse])
async def list_data_sources(db=Depends(get_db)):
    """List all data sources"""
    try:
        sources = db.query(DataSource).all()
        return [DataSourceResponse.from_orm(s) for s in sources]
    except Exception as e:
        logger.error(f"Error listing sources: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/sources/{source_id}")
async def delete_data_source(source_id: str, db=Depends(get_db)):
    """Delete a data source"""
    try:
        source = db.query(DataSource).filter(DataSource.id == source_id).first()
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        
        db.delete(source)
        db.commit()
        
        return {"status": "deleted"}
    except Exception as e:
        logger.error(f"Error deleting source: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Indexing Endpoints ====================

@app.post("/api/index", response_model=IndexResponse)
async def start_indexing(request: IndexRequest, background_tasks: BackgroundTasks, db=Depends(get_db)):
    """Start indexing a data source"""
    try:
        source = db.query(DataSource).filter(DataSource.id == request.data_source_id).first()
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        
        session_id = str(uuid.uuid4())
        
        # Create indexing session
        session = IndexSession(
            id=session_id,
            data_source_id=source.id,
            status="running",
        )
        db.add(session)
        db.commit()
        
        # Start indexing in background
        background_tasks.add_task(
            _index_data_source,
            source_id=source.id,
            session_id=session_id,
            db=database.get_session()
        )
        
        return IndexResponse(
            session_id=session_id,
            status="running",
            documents_processed=0,
            chunks_created=0,
        )
    
    except Exception as e:
        logger.error(f"Error starting indexing: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def _index_data_source(source_id: str, session_id: str, db):
    """Background task to index data source"""
    try:
        source = db.query(DataSource).filter(DataSource.id == source_id).first()
        session = db.query(IndexSession).filter(IndexSession.id == session_id).first()
        
        if not source or not session:
            return
        
        # Connect to data source
        connector = get_connector(source.source_type, source.config)
        await connector.connect()
        
        # Load documents
        documents = await connector.load_documents()
        session.documents_processed = len(documents)
        
        # Index documents
        chunks_created = await rag_pipeline.index_documents(documents)
        session.chunks_created = chunks_created
        
        # Update source
        source.indexed = True
        source.document_count = len(documents)
        source.last_indexed = __import__('datetime').datetime.utcnow()
        
        # Update session
        session.status = "completed"
        
        await connector.disconnect()
        
        db.commit()
        logger.info(f"Indexed {len(documents)} documents, created {chunks_created} chunks")
    
    except Exception as e:
        logger.error(f"Indexing error: {e}")
        session = db.query(IndexSession).filter(IndexSession.id == session_id).first()
        if session:
            session.status = "failed"
            session.error_message = str(e)
            db.commit()


# ==================== Conversation Endpoints ====================

@app.post("/api/conversations", response_model=ConversationResponse)
async def create_conversation(config: ConversationCreate, db=Depends(get_db)):
    """Create new conversation"""
    try:
        conv_id = str(uuid.uuid4())
        
        conversation = Conversation(
            id=conv_id,
            title=config.title,
            data_source_ids=config.data_source_ids,
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        return ConversationResponse.from_orm(conversation)
    
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/conversations/{conv_id}", response_model=ConversationWithMessages)
async def get_conversation(conv_id: str, db=Depends(get_db)):
    """Get conversation with messages"""
    try:
        conversation = db.query(Conversation).filter(Conversation.id == conv_id).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = db.query(Message).filter(Message.conversation_id == conv_id).all()
        
        return ConversationWithMessages(
            **ConversationResponse.from_orm(conversation).dict(),
            messages=[MessageResponse.from_orm(m) for m in messages]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Query Endpoints ====================

@app.post("/api/query")
async def query(request: QueryRequest, db=Depends(get_db)):
    """Query RAG pipeline with streaming response"""
    try:
        # Get or create message
        msg_id = str(uuid.uuid4())
        
        # Store user message
        user_msg = Message(
            id=str(uuid.uuid4()),
            conversation_id=request.conversation_id,
            role="user",
            content=request.message,
        )
        db.add(user_msg)
        db.commit()
        
        # Get conversation history
        history = db.query(Message).filter(
            Message.conversation_id == request.conversation_id
        ).order_by(Message.created_at).all()
        
        history_list = [{"role": m.role, "content": m.content} for m in history[:-1]]
        
        async def response_generator():
            """Generate streaming response"""
            full_answer = ""
            sources = []
            
            try:
                # Get context through RAG
                context = await rag_pipeline.retrieve_context(request.message)
                sources = [
                    {
                        "text": text[:200],
                        "source": meta.get("source", "Unknown"),
                        "relevance": float(score),  # Convert numpy types to Python float
                    }
                    for text, score, meta in context
                ]
                
                # Generate answer with streaming
                async for chunk in rag_pipeline.answer_question(
                    request.message,
                    history_list,
                    use_stream=True,
                    temperature=request.temperature,
                ):
                    yield chunk
                    full_answer += chunk
                
                # Store assistant response
                assistant_msg = Message(
                    id=str(uuid.uuid4()),
                    conversation_id=request.conversation_id,
                    role="assistant",
                    content=full_answer,
                    sources=sources,
                )
                db.add(assistant_msg)
                db.commit()
            
            except Exception as e:
                logger.error(f"Error in query: {e}")
                yield f"Error: {str(e)}"
        
        return StreamingResponse(response_generator(), media_type="text/event-stream")
    
    except Exception as e:
        logger.error(f"Error handling query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search", response_model=list[SearchResult])
async def search_documents(request: SearchRequest):
    """Search documents without generating answer"""
    try:
        context = await rag_pipeline.retrieve_context(request.query, request.top_k)
        
        results = [
            SearchResult(
                text=text,
                source=meta.get("source", "Unknown"),
                source_type=meta.get("source_type", "document"),
                relevance_score=float(score),  # Convert numpy types to Python float
                metadata=meta,
            )
            for text, score, meta in context
        ]
        
        return results
    
    except Exception as e:
        logger.error(f"Error searching: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Mount Static Files
# Serve React frontend - this should be last so API routes take precedence
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")
    logger.info(f"Static files mounted from {frontend_path}")
else:
    logger.warning(f"Frontend directory not found at {frontend_path}")


# ==================== Health & Info Endpoints ====================

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "ok",
        "rag_pipeline": rag_pipeline is not None,
        "vector_store": vector_store is not None,
    }


@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    try:
        vector_stats = await vector_store.get_stats()
        
        return {
            "vector_store": vector_stats,
            "llm": {
                "provider": settings.DEFAULT_LLM,
                "model": getattr(settings, f"{settings.DEFAULT_LLM.upper()}_MODEL"),
            },
            "settings": {
                "chunk_size": settings.CHUNK_SIZE,
                "chunk_overlap": settings.CHUNK_OVERLAP,
                "top_k_results": settings.TOP_K_RESULTS,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
