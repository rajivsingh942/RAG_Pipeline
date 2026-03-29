#!/usr/bin/env python
"""
Minimal app runner for Render deployment
Starts FastAPI on the PORT environment variable
"""
import os
import sys
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get config from environment
host = os.getenv("API_HOST", "0.0.0.0")
port = int(os.getenv("PORT", "8000"))

logger.info(f"🚀 Starting Smart RAG Pipeline on {host}:{port}")

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

try:
    import uvicorn
    logger.info("✅ Uvicorn imported")
    
    # Run the app
    logger.info("Starting FastAPI application...")
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info",
        access_log=True,
    )
except Exception as e:
    logger.error(f"❌ Failed to start: {e}", exc_info=True)
    sys.exit(1)
