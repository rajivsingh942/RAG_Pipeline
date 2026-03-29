#!/usr/bin/env python
"""Run the FastAPI application"""
import uvicorn
import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Get configuration from environment or use defaults
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    # Check if running in Render
    is_render = "RENDER" in os.environ
    is_development = os.getenv("ENVIRONMENT", "production") == "development"
    
    logger.info(f"🚀 Starting FastAPI Server")
    logger.info(f"📍 Host: {host}:{port}")
    logger.info(f"🌍 Environment: {'Render Cloud' if is_render else 'Local'}")
    logger.info(f"🔄 Reload: {reload and not is_render}")
    
    # Run uvicorn
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload and not is_render,  # No reload in production/Render
        log_level="info",
        access_log=True,
    )
