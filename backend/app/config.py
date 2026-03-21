"""
Configuration management for RAG Pipeline
"""
import os
from pathlib import Path
from functools import lru_cache
from typing import Optional
from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

# Find .env file - it should be in parent directory
def find_env_file():
    """Find .env file in parent directories"""
    current = Path.cwd()
    for _ in range(5):  # Check up to 5 parent directories
        env_file = current / ".env"
        if env_file.exists():
            return str(env_file)
        current = current.parent
    # Default to ../.env
    return str(Path(__file__).parent.parent.parent / ".env")

# Get base directory for data files
def get_data_dir():
    """Get absolute path to data directory"""
    backend_dir = Path(__file__).parent.parent
    data_dir = backend_dir / "data"
    data_dir.mkdir(exist_ok=True)
    return str(data_dir)

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    model_config = ConfigDict(
        env_file=find_env_file(),
        case_sensitive=True,
        extra='ignore'
    )
    
    # API Keys - with defaults to prevent validation errors
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key")
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    GEMINI_API_KEY: str = Field(default="", description="Gemini API key")
    GEMINI_MODEL: str = "gemini-1.5-pro"
    
    OPENROUTER_API_KEY: str = Field(default="", description="OpenRouter API key")
    OPENROUTER_MODEL: str = "meta-llama/llama-3-8b-instruct"
    
    # Firebase
    FIREBASE_PROJECT_ID: Optional[str] = None
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    FIREBASE_ENABLED: bool = False
    
    # Application Settings
    DEFAULT_LLM: str = "openai"  # openai, gemini, or openrouter
    DEFAULT_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Vector Store Settings - Using absolute paths
    VECTOR_STORE_PATH: str = Field(default_factory=lambda: os.path.join(get_data_dir(), "vector_store"))
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Database Settings - Using absolute path
    DATABASE_URL: str = Field(default_factory=lambda: f"sqlite:///{os.path.join(get_data_dir(), 'rag_pipeline.db')}")
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: list = [
        "pdf", "txt", "docx", "doc", "pptx", "ppt",
        "xlsx", "xls", "csv", "json", "md"
    ]
    
    # Data Source Settings
    DATA_SOURCES_PATH: str = Field(default_factory=lambda: os.path.join(get_data_dir(), "sources"))
    
    # RAG Settings
    TOP_K_RESULTS: int = 5
    CONTEXT_WINDOW: int = 3000
    
    # Logging
    LOG_LEVEL: str = "INFO"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    settings = Settings()
    # Ensure data directory exists
    get_data_dir()
    return settings
