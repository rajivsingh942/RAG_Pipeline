# 🚀 SMART RAG PIPELINE - COMPLETE DEPLOYMENT GUIDE

**Last Updated**: March 29, 2026  
**Status**: ✅ Ready for Deployment  
**Estimated Deployment Time**: 15 minutes  

---

## 📋 PROJECT SUMMARY

This is a complete **Retrieval Augmented Generation (RAG)** application with:

- ✅ **Backend**: FastAPI with multi-LLM support (OpenAI, Gemini, OpenRouter)
- ✅ **Frontend**: React web interface with real-time chat
- ✅ **Vector Search**: FAISS-based semantic search
- ✅ **Data Sources**: Folder, Database, File, SharePoint connectors
- ✅ **Conversation Memory**: SQLite database with history
- ✅ **Production Ready**: Dockerized and optimized for cloud

---

## 📁 PROJECT STRUCTURE (50+ Files)

### **Root Level** (18 core files)
- `Dockerfile` - Container configuration
- `render.yaml` - Render.com deployment config ⭐
- `requirements.txt` - Python dependencies
- `.env.example` - Template for API keys
- `start_render.py` - Smart startup script
- Documentation files (README, QUICK_START, etc.)

### **Backend** (20+ Python files)
```
backend/
├── app/
│   ├── main.py (420+ lines, 10 API endpoints)
│   ├── config.py (Environment & LLM config)
│   ├── schemas.py (Data models)
│   ├── connectors/ (DB, File, Folder, SharePoint)
│   ├── db/ (Database & models)
│   ├── llms/ (OpenAI, Gemini, OpenRouter)
│   └── rag/ (Pipeline & vector store)
├── run.py (Entry point)
└── requirements.txt
```

### **Frontend** (React + Vite)
```
frontend/
├── index.html
└── src/
    └── components/
        └── AddSourceForm.jsx (+ more components)
```

### **Data & Configs**
- `.env` - API keys (configured)
- `backend/data/vector_store/` - FAISS database
- `backend/data/rag_pipeline.db` - Conversation history

---

## 🎯 DEPLOYMENT CHECKLIST

### ✅ Pre-Deployment (Local)
- [x] All 50+ project files present
- [x] Backend API endpoints configured  
- [x] Frontend components created
- [x] Dockerfile optimized
- [x] render.yaml configured ⭐
- [x] Environment variables template ready
- [x] Git repository initialized
- [x] All changes committed

### ⏳ To Do (You)
- [ ] Create GitHub repository (or use existing)
- [ ] Push code to GitHub
- [ ] Create Render.com free account
- [ ] Connect Render to GitHub
- [ ] Configure API keys (OpenAI/Gemini/OpenRouter)
- [ ] Deploy on Render
- [ ] Test the live app

---

## 🔑 STEP-BY-STEP DEPLOYMENT

### **STEP 1: Push to GitHub** (5 min)

```powershell
# Open PowerShell and navigate to project
cd "c:\Users\Rajiv Singh\Desktop\RAG_PIPELINE"

# Configure git remote (replace with YOUR repo URL)
git remote add origin https://github.com/YOUR_USERNAME/rag-pipeline.git
git branch -M main
git push -u origin main
```

**Create a new GitHub repo first?**
1. Go to https://github.com/new
2. Name: `rag-pipeline`
3. Make it **PUBLIC** (required for free Render)
4. Click Create
5. Copy the HTTPS URL and use in commands above

---

### **STEP 2: Deploy on Render.com** (10 min)

**2.1 Create Account**
- Go to https://render.com/register
- Sign up with GitHub (easiest)
- Authorize Render to access your GitHub

**2.2 Create Web Service**
- Go to https://dashboard.render.com
- Click "+ New" → "Web Service"
- Select your `rag-pipeline` repository
- Render auto-detects `render.yaml` ✓

**2.3 Configure Service**
```
Service Name:    smart-rag-app
Environment:     Docker
Region:          oregon (or your region)
Branch:          main
```

**2.4 Add Environment Variables** ⚠️  **IMPORTANT**

Go to **Settings** → **Environment** → Add these:

**Choose ONE LLM Provider and set its variables:**

#### **Option A: OpenAI** (Best Quality)
```
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-your-actual-key-here
```
- Get key: https://platform.openai.com/api-keys
- Includes $5 free credit

#### **Option B: Google Gemini** (Free, Recommended ⭐)
```
LLM_PROVIDER=gemini
LLM_MODEL=gemini-1.5-pro
GOOGLE_API_KEY=your-actual-key-here
```
- Get key: https://makersuite.google.com/app/apikey
- No credit card needed

#### **Option C: OpenRouter** (Cheapest)
```
LLM_PROVIDER=openrouter
LLM_MODEL=meta-llama/llama-3-8b-instruct
OPENROUTER_API_KEY=sk-or-your-actual-key-here
```
- Get key: https://openrouter.ai/keys

**2.5 Deploy**
- Click the big **"Deploy"** button
- Wait 5-10 minutes for build to complete
- Check logs if there are issues

---

## 🌐 ACCESSING YOUR APP

Once deployed successfully, you'll see:
```
✅ Deployment successful - Live at: smart-rag-app.onrender.com
```

### **Access Points:**

| Component | URL |
|-----------|-----|
| 🖥️ Frontend (Chat UI) | `https://smart-rag-app.onrender.com` |
| 🔌 Backend API | `https://smart-rag-app.onrender.com/api/` |
| 📚 API Documentation | `https://smart-rag-app.onrender.com/docs` |
| ❤️ Health Check | `https://smart-rag-app.onrender.com/health` |

### **Quick Test:**
```bash
curl https://smart-rag-app.onrender.com/health
# Should return: {"status":"healthy"}
```

---

## 🔧 API ENDPOINTS

### **Data Sources**
```
POST /api/sources              # Create data source
GET /api/sources               # List all sources
POST /api/search-sources       # Search sources
```

### **Document Operations**
```
POST /api/index                # Index documents
POST /api/search               # Search documents
GET /api/search?q=...          # Quick search
```

### **Conversations**
```
POST /api/conversations        # Create conversation
GET /api/conversations/{id}    # Get conversation
```

### **RAG Query (Main Feature)**
```
POST /api/query                # Send query with streaming response
```

### **System**
```
GET /health                    # Health check
GET /api/stats                 # System statistics
GET /api/config                # Configuration info
```

---

## 📊 WHAT'S INCLUDED

### **Backend Features**
✅ FastAPI REST API (10+ endpoints)  
✅ Real-time streaming responses  
✅ 3 LLM providers (OpenAI, Gemini, OpenRouter)  
✅ Vector search with FAISS  
✅ 4 data connectors (DB, File, Folder, SharePoint)  
✅ Document processing (PDF, Word, Excel, Text)  
✅ Conversation memory (SQLite)  
✅ Source attribution  
✅ Health monitoring  

### **Frontend Features**
✅ React + Vite  
✅ Real-time chat interface  
✅ Data source management UI  
✅ Responsive design  
✅ Component architecture  

### **Infrastructure**
✅ Docker containerization  
✅ Render.com ready  
✅ Free tier compatible  
✅ Auto-scaling  
✅ HTTPS/SSL included  

---

## 🆓 FREE TIER DETAILS

### **Render.com Free Tier Includes:**
- ✅ **750 free hours/month** (always-on service)
- ✅ **100GB bandwidth/month**
- ✅ **Custom domain** support
- ✅ **Automatic SSL/HTTPS**
- ✅ **Git-based deployment** (auto-redeploy on push)
- ✅ **Environment variables** unlimited

### **Limitations:**
- ⚠️ App goes to sleep after 15 min of inactivity (paid: no sleep)
- ⚠️ Build time limited to 45 min (more than enough)
- ⚠️ Memory: 256MB default (enough for this app)

### **Upgrade Options (Optional):**
- **Starter ($7/month)**: No auto-sleep, 2GB RAM
- **Standard ($12/month)**: More resources
- **Professional ($26/month)**: Production-grade

---

## ⚠️ IMPORTANT NOTES

### **Before Deploying:**
1. ✅ Repository must be **PUBLIC** on GitHub
2. ✅ Render.yaml must be at root of repository
3. ✅ All environment variables must be set
4. ✅ API keys should be valid (test before deploying)

### **During Deployment:**
- Building Docker image takes 3-5 minutes
- First startup takes 2-3 minutes additional
- Total time: ~10 minutes usually

### **After Deployment:**
- Check `https://smart-rag-app.onrender.com/health` to verify
- First request might be slow (cold start)
- Subsequent requests are fast
- App sleeps after 15 min inactivity (free tier)

---

## 🐛 TROUBLESHOOTING

### ❌ Deployment Failed

**Check these:**
```
1. Logs: Service → Logs tab
2. Environment variables: Settings → Environment
3. API keys: Try pasting exact key again
4. Repository: Must be public and have render.yaml
```

### ❌ App Runs But Chat Doesn't Work

```
Likely causes:
- API key is invalid
- Wrong LLM provider selected
- API quota exceeded
- Network issue

Check: /api/stats endpoint for diagnostics
```

### ❌ Slow First Load

```
Normal! This is cold start.
- First load: 10-30 seconds
- Subsequent: <2 seconds
- Restart app if needed: Service → More → Restart
```

### ❌ DNS Error (Domain Not Found)

```
DNS takes a few minutes to propagate.
- Wait 2-3 minutes
- Clear browser cache
- Try incognito window
```

---

## 📞 QUICK REFERENCE

### **Important URLs:**
- Render Dashboard: https://dashboard.render.com
- Your App: https://smart-rag-app.onrender.com
- GitHub Repo: https://github.com/YOUR_USERNAME/rag-pipeline
- API Docs: https://smart-rag-app.onrender.com/docs

### **LLM Provider URLs:**
- OpenAI Keys: https://platform.openai.com/api-keys
- Gemini Keys: https://makersuite.google.com/app/apikey
- OpenRouter Keys: https://openrouter.ai/keys

### **Important Files:**
- Backend: `backend/app/main.py`
- Config: `backend/app/config.py`
- Deployment: `render.yaml`
- Dockerfile: `Dockerfile`

---

## 📈 NEXT STEPS

After successful deployment:

1. **Test the App**
   - Go to your app URL
   - Add a data source
   - Index some documents
   - Try a query

2. **Customize**
   - Modify frontend colors/branding
   - Add more data connectors
   - Scale vector store
   - Add more LLM providers

3. **Upgrade (Optional)**
   - Add custom domain
   - Upgrade to paid plan for always-on
   - Set up auto-backup
   - Add monitoring

4. **Share**
   - Share your app URL with users
   - Gather feedback
   - Deploy improvements

---

## ✨ FINAL CHECKLIST

Before you click deploy:

```powershell
# ✓ Code is committed
git status

# ✓ Code is pushed
git log --oneline

# ✓ Dockerfile exists
Test-Path Dockerfile

# ✓ render.yaml exists  
Test-Path render.yaml

# ✓ API keys are ready (from OpenAI/Gemini/OpenRouter)

# ✓ GitHub repo is PUBLIC

# ✓ Render account created
# Go to: https://render.com/register

# ✓ You're ready to deploy! 🚀
```

---

## 🎉 YOU'RE ALL SET!

Your Smart RAG Pipeline is ready to deploy!

**Next action:** Create your GitHub repository and push the code using the commands in STEP 1 above, then deploy on Render.com.

Need help? Check:
- [Render.com Docs](https://render.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Docker Docs](https://docs.docker.com/)

**Good luck! Your app will be live in 15 minutes! 🚀**

---

*Generated: March 29, 2026*
