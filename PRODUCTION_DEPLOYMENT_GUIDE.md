# 🚀 Smart RAG Pipeline - Production Deployment Guide

**Version**: 1.0  
**Last Updated**: March 29, 2026  
**Status**: ✅ Production Ready

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [Render.com Deployment](#rendercom-deployment)
5. [Configuration](#configuration)
6. [API Endpoints](#api-endpoints)
7. [Troubleshooting](#troubleshooting)
8. [Production Best Practices](#production-best-practices)

---

## 🎯 System Overview

**Smart RAG Pipeline** is a production-grade Retrieval-Augmented Generation (RAG) application that:

- ✅ Connects to multiple data sources (local files, databases, SharePoint)
- ✅ Indexes documents using FAISS vector search
- ✅ Provides streaming AI responses with source attribution
- ✅ Supports 3 LLM providers (OpenAI, Google Gemini, OpenRouter)
- ✅ Maintains conversation history and context
- ✅ Runs on free Render.com tier

**Technology Stack**:
- Backend: FastAPI 0.104.1 + Uvicorn
- LLM Integration: OpenAI, Google Generative AI, OpenRouter
- Vector Search: FAISS 1.7.4 + SentenceTransformers
- Database: SQLite + SQLAlchemy ORM
- Deployment: Docker + Render.com

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend React UI                     │
│            (Served as static files from /api)            │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (app_runner.py)             │
│  ┌──────────────────────────────────────────────────┐   │
│  │  /health - Health Check                         │   │
│  │  /api/sources - Data Source Management          │   │
│  │  /api/index - Document Indexing                 │   │
│  │  /api/conversations - Chat Sessions             │   │
│  │  /api/query - RAG Query with Streaming          │   │
│  │  /api/search - Vector Search                    │   │
│  │  /docs - API Documentation                      │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
         ↓                      ↓                   ↓
    ┌─────────┐        ┌──────────────┐     ┌────────────┐
    │ SQLite  │        │ FAISS Index  │     │ LLM APIs   │
    │Database │        │Vector Store  │     │(OpenAI etc)│
    └─────────┘        └──────────────┘     └────────────┘
```

---

## ⚡ Quick Start

### Local Development

```bash
# 1. Create virtual environment
python -m venv venv
./venv/Scripts/Activate.ps1  # Windows
source venv/bin/activate      # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env
# Edit .env and add your API keys:
# - OPENAI_API_KEY=sk-...
# - GOOGLE_API_KEY=...
# etc.

# 4. Run locally
python app_runner.py

# 5. Open browser
# Frontend: http://localhost:10000
# API Docs: http://localhost:10000/docs
```

### Using Docker Locally

```bash
# Build image
docker build -t rag-pipeline .

# Run container
docker run -p 10000:10000 \
  -e OPENAI_API_KEY=sk-... \
  rag-pipeline
```

---

## 🎯 Render.com Deployment

### Step 1: Prerequisites
- GitHub account with repository pushed
- Render.com account (free tier available)
- API keys for at least one LLM provider

### Step 2: Deploy to Render

1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Select your GitHub repository (`RAG_Pipeline`)
4. Render will auto-detect `render.yaml` and configure:
   - **Service Name**: rag-pipeline-7
   - **Environment**: Docker
   - **Region**: oregon (or your preference)

### Step 3: Configure Environment Variables

In Render dashboard, go to **Environment** and add:

```
PORT=10000
API_HOST=0.0.0.0
ENVIRONMENT=production
DEFAULT_LLM=openai
OPENAI_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-your-key-here    # Required!
DATABASE_PATH=/tmp/rag_pipeline.db
VECTOR_STORE_PATH=/tmp/faiss_index
```

### Step 4: Deploy

- Click **"Create Web Service"**
- Render will build and deploy automatically
- Deployment typically takes 3-5 minutes

### Step 5: Access Your App

- **Frontend**: https://rag-pipeline-7.onrender.com/
- **API Docs**: https://rag-pipeline-7.onrender.com/docs
- **Health Check**: https://rag-pipeline-7.onrender.com/health

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 10000 | Server port |
| `API_HOST` | 0.0.0.0 | Server host |
| `ENVIRONMENT` | production | Environment mode |
| `DEFAULT_LLM` | openai | Default LLM: openai \| gemini \| openrouter |
| `OPENAI_API_KEY` | - | OpenAI API key (required if using OpenAI) |
| `OPENAI_MODEL` | gpt-4o-mini | OpenAI model name |
| `DATABASE_PATH` | /tmp/rag_pipeline.db | SQLite database path |
| `VECTOR_STORE_PATH` | /tmp/faiss_index | FAISS vector store path |

### Getting API Keys

**OpenAI**:
1. Go to [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Create new API key
3. Copy and save securely

**Google Gemini**:
1. Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Create new API key
3. Copy and save securely

**OpenRouter** (use any open-source model):
1. Go to [https://openrouter.ai/keys](https://openrouter.ai/keys)
2. Create new API key
3. Copy and save securely

---

## 🔌 API Endpoints

### Health Check
```bash
GET /health
```
Returns app status and readiness.

### Data Sources
```bash
# List all sources
GET /api/sources

# Add new source
POST /api/sources
{
  "name": "My Documents",
  "source_type": "folder",
  "config": {"path": "/path/to/docs"}
}

# Delete source
DELETE /api/sources/{source_id}
```

### Document Indexing
```bash
# Start indexing
POST /api/index
{
  "data_source_id": "source-123"
}

# Get index status
GET /api/index/{session_id}
```

### Conversations
```bash
# Create conversation
POST /api/conversations
{
  "title": "Chat about my documents",
  "data_source_ids": ["source-123"]
}

# Get conversation
GET /api/conversations/{conversation_id}

# Get messages
GET /api/conversations/{conversation_id}/messages
```

### Query/Chat
```bash
# Query with streaming response
POST /api/query
{
  "conversation_id": "conv-123",
  "message": "What is the main topic?",
  "temperature": 0.7
}
```

### Search
```bash
# Search documents
POST /api/search
{
  "query": "search term",
  "top_k": 5
}
```

### API Documentation
```
GET /docs  # Swagger UI
GET /redoc # ReDoc UI
```

---

## 🔧 Troubleshooting

### App Returns 503 Service Unavailable

**Cause**: App failed to start or is crashing

**Solution**:
1. Check Render logs: Dashboard → Service → Logs
2. Verify environment variables are set
3. Ensure API keys are valid
4. Check PYTHONPATH in Dockerfile

### App Starts but /api endpoints return 500

**Cause**: Missing/invalid API key or database connection issue

**Solution**:
1. Verify `OPENAI_API_KEY` is set and valid
2. Check database write permissions in `/tmp`
3. Review application logs for specific errors

### Static Frontend Not Loading

**Cause**: Frontend files not mounted properly

**Solution**:
1. Verify `frontend/index.html` exists
2. Check Dockerfile copies frontend correctly
3. Verify FastAPI mounts static files correctly

### Vector Store/FAISS Errors

**Cause**: Dimension mismatch or corrupted index

**Solution**:
1. Delete `/tmp/faiss_index` directory
2. Restart app to recreate index
3. Re-index documents

---

## 📋 Production Best Practices

### 1. ✅ Monitoring
- Set up Render health checks
- Monitor logs regularly
- Set up error alerts

### 2. ✅ Security
- Keep API keys secret (never commit to git)
- Use Render environment variables for secrets
- Implement rate limiting for public APIs
- Use HTTPS only (Render provides this)

### 3. ✅  Performance
- Free tier: App sleeps after 15 minutes inactivity
- Upgrade to Starter plan ($7/month) for always-on
- Use vector search efficiently (limit `top_k`)
- Cache frequently used queries

### 4. ✅ Data Management
- `/tmp` storage is temporary (cleared on redeploy)
- For persistent data, set up PostgreSQL (Render)
- Regular database backups
- Implement data cleanup policies

### 5. ✅ Scaling
- Current setup: 1 instance, free tier
- To scale: Add horizontal scaling in render.yaml
- Use PostgreSQL instead of SQLite
- Implement caching layer (Redis)

---

## 📊 Performance Characteristics

| Operation | Typical Time | Notes |
|-----------|--------------|-------|
| App startup | 8-15 seconds | On free tier from cold |
| First query | 2-5 seconds | Heavy models load |
| Subsequent queries | <500ms | Models cached |
| Indexing (100 docs) | 30-60 seconds | Depends on doc size |
| Search (top-5) | <200ms | FAISS vector search |

---

## 🔄 Deployment Workflow

```
1. Make code changes locally
            ↓
2. Test with: python app_runner.py
            ↓
3. Commit: git add -A && git commit -m "..."
            ↓
4. Push: git push origin main
            ↓
5. Render auto-builds and deploys
            ↓
6. Check: https://rag-pipeline-7.onrender.com/health
            ↓
7. Done! ✅
```

---

## 📞 Support & Resources

- **API Docs**: https://rag-pipeline-7.onrender.com/docs
- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **FAISS Docs**: https://github.com/facebookresearch/faiss

---

## ✅ Verification Checklist

Before production deployment:

- [ ] All environment variables configured
- [ ] API keys are valid and active
- [ ] Database path is writable
- [ ] Frontend files exist in `/frontend`
- [ ] App starts locally without errors
- [ ] Health endpoint responds
- [ ] At least one API endpoint tested
- [ ] Docker image builds successfully
- [ ] GitHub repo is up-to-date
- [ ] Render health check passes

---

**Version**: 1.0 | **Date**: March 29, 2026 | **Status**: ✅ Production Ready
