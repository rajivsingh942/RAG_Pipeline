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
# Copy only necessary files for production
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY requirements.txt ./
COPY app_runner.py ./
COPY .env.example ./.env
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
# SET PYTHON PATH AND ENVIRONMENT
# ============================================================================
# Configure Python path and environment for production
ENV PYTHONPATH=/app:/app/backend:$PYTHONPATH
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# ============================================================================
# EXPOSE PORTS
# ============================================================================
EXPOSE 10000

# ============================================================================
# HEALTH CHECK
# ============================================================================
# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=45s --retries=3 \
    CMD curl -f http://localhost:${PORT:-10000}/health || exit 1

# ============================================================================
# RUN COMMAND
# ============================================================================
# Run app with proper error handling and logging via app_runner.py
CMD ["python", "app_runner.py"]

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
