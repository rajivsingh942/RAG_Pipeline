# ============================================================================
# DOCKERFILE - Build container for Smart RAG Project
# ============================================================================
# This Dockerfile packages the Smart RAG application for cloud deployment
# Supports: Docker, Kubernetes, AWS ECS, Google Cloud Run, Azure Container, etc.
# ============================================================================

FROM python:3.11-slim

# ============================================================================
# SET WORKING DIRECTORY
# ============================================================================
WORKDIR /app

# ============================================================================
# INSTALL SYSTEM DEPENDENCIES
# ============================================================================
# Install necessary system packages for Python packages that need compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ============================================================================
# COPY PROJECT FILES
# ============================================================================
# Copy only necessary files (not venv, data, __pycache__, etc.)
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY .env.example ./.env
COPY requirements.txt ./
COPY frontend_server.py ./
COPY README.md ./

# ============================================================================
# INSTALL PYTHON DEPENDENCIES
# ============================================================================
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# ============================================================================
# CREATE DATA DIRECTORIES
# ============================================================================
# Create directories where data will be stored
RUN mkdir -p backend/data

# ============================================================================
# EXPOSE PORTS
# ============================================================================
# FastAPI backend on 8000
EXPOSE 8000
# Frontend on 3000
EXPOSE 3000

# ============================================================================
# HEALTH CHECK
# ============================================================================
# Check if API is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# ============================================================================
# RUN COMMAND
# ============================================================================
# Start both backend and frontend
# Note: This starts backend in foreground. For production, use separate containers
CMD ["sh", "-c", "python backend/run.py & python frontend_server.py"]

# ============================================================================
# NOTES FOR CLOUD DEPLOYMENT
# ============================================================================
# 1. Google Cloud Run:
#    - Use PORT environment variable instead of 8000
#    - Update CMD to: CMD exec python backend/run.py --host 0.0.0.0 --port $PORT
#
# 2. AWS Fargate / Lambda:
#    - Separate containers recommended (one for backend, one for frontend)
#    - Use aws s3 mount for persistent data storage
#
# 3. Azure Container Instances:
#    - Works as-is, mount Azure Files for persistent storage
#
# 4. Heroku:
#    - Create Procfile: web: python backend/run.py
#    - Procfile for background job: worker: python frontend_server.py
#
# 5. Persisten Data:
#    - Use cloud storage instead of local backend/data/
#    - Mount volumes or use managed database
# ============================================================================
