#!/usr/bin/env python
"""Run the FastAPI application"""
import uvicorn
import sys
import os

if __name__ == "__main__":
    # Get configuration from environment or use defaults
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", os.getenv("API_PORT", 8000)))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    # Render uses RENDER env variable
    is_render = "RENDER" in os.environ
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload and not is_render,  # No reload in production
        log_level="info",
    )
