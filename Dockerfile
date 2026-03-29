# ============================================================================
# DOCKERFILE - Build container for Smart RAG Project
# ============================================================================
# This Dockerfile packages the Smart RAG application for cloud deployment
# Supports: Docker, Kubernetes, AWS ECS, Google Cloud Run, Render, Azure Container, etc.
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
COPY start_render.py ./
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
# Render assigns a port dynamically via $PORT environment variable
# We use 10000 as a fallback/default
EXPOSE 10000

# ============================================================================
# HEALTH CHECK
# ============================================================================
# Check if API is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-10000}/health || exit 1

# ============================================================================
# RUN COMMAND
# ============================================================================
# Use the smart startup script that handles both local and Render deployment
CMD ["python", "start_render.py"]

# ============================================================================
# NOTES FOR CLOUD DEPLOYMENT
# ============================================================================
# 1. Render.com (PRIMARY):
#    - Uses PORT environment variable (auto-assigned)
#    - Data stored in /tmp (temporary - use PostgreSQL for persistence)
#    - Auto-scales based on usage
#    - Free tier: suspended after 15 mins inactivity
#
# 2. Google Cloud Run:
#    - Use PORT environment variable
#    - Container must be stateless (use Cloud Storage for data)
#
# 3. AWS Fargate / Lambda:
#    - Use PORT environment variable
#    - Separate containers recommended (one for backend, one for frontend)
#    - Use S3 or EBS for persistent data storage
#
# 4. Azure Container Instances:
#    - Works as-is, mount Azure Files for persistent storage
#
# ============================================================================
