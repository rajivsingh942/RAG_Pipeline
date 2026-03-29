#!/usr/bin/env python
"""
Smart RAG - Render Deployment Quick Start
Step-by-step guide to get your app live
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║           Smart RAG Pipeline - Render Deployment Checklist                 ║
║                     Everything is ready to deploy!                         ║
╚════════════════════════════════════════════════════════════════════════════╝

✅ COMPLETED:
   ✓ Backend FastAPI configured for Render
   ✓ Frontend static server configured
   ✓ Docker setup optimized for cloud
   ✓ Environment variables documented
   ✓ All dependencies installed and tested
   ✓ Git repository initialized
   ✓ Deployment files created (render.yaml, Procfile, etc.)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: CREATE GITHUB REPOSITORY (5 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1.1 Go to https://github.com/new
1.2 Repository name: RAG_PIPELINE (or your preferred name)
1.3 Description: Smart RAG - AI Document Analysis & Q&A
1.4 Choose: Public (for easy Render deployment)
1.5 Click "Create repository"

1.6 After creation, GitHub will show commands. Run these:

  git remote add origin https://github.com/YOUR_USERNAME/RAG_PIPELINE.git
  git branch -M main
  git push -u origin main

Replace YOUR_USERNAME with your actual GitHub username!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: GET API KEYS (10 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Choose ONE of the following (or use multiple for redundancy):

┌─ OPTION A: OPENAI (Best Quality) ────────────────────────────────────────┐
│                                                                             │
│ Best for: High-quality responses, preferred by enterprises                │
│ Cost: Pay-per-query (~$0.01-0.10 per question)                            │
│ Free credit: $5 for first 3 months                                        │
│                                                                             │
│ STEPS:                                                                      │
│ 1. Go to: https://platform.openai.com/signup                              │
│ 2. Sign up with email                                                      │
│ 3. Go to: https://platform.openai.com/api-keys                            │
│ 4. Click "Create new secret key"                                           │
│ 5. Copy the key (looks like: sk-proj-xxxx)                                │
│                                                                             │
│ API Key format: sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─ OPTION B: GOOGLE GEMINI (Free Tier) ───────────────────────────────────┐
│                                                                             │
│ Best for: Free tier, no credit card needed initially                       │
│ Cost: Free for first 50 requests/day, then pay-per-query                   │
│ Free tier: 1M tokens/month                                                 │
│                                                                             │
│ STEPS:                                                                      │
│ 1. Go to: https://makersuite.google.com/app/apikey                        │
│ 2. Click "Get API Key" or "Create API Key"                                │
│ 3. Select project or create new                                            │
│ 4. Copy the API key                                                        │
│                                                                             │
│ API Key format: AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─ OPTION C: OPENROUTER (CHEAPEST - RECOMMENDED) ─────────────────────────┐
│                                                                             │
│ Best for: Budget-conscious, supports multiple models                      │
│ Cost: From $0.000005 per query! (very cheap)                              │
│ Models: OpenAI, Llama, Mistral, Claude, etc.                              │
│ Free credit: Often includes free tier                                      │
│                                                                             │
│ STEPS:                                                                      │
│ 1. Go to: https://openrouter.ai/signup                                    │
│ 2. Sign up (email, Discord, or Google)                                     │
│ 3. Go to: https://openrouter.ai/keys                                      │
│ 4. Create API key                                                          │
│ 5. Copy the key                                                            │
│                                                                             │
│ API Key format: sk-or-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx                        │
│ Default model: meta-llama/llama-3-8b-instruct (very cheap!)               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

MY RECOMMENDATION: Start with Google Gemini (free) or OpenRouter (cheapest)
Then upgrade to OpenAI later if needed.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: CREATE RENDER ACCOUNT (2 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3.1 Go to: https://dashboard.render.com
3.2 Click "Sign up"
3.3 Sign in with GitHub (easiest - already have your repos)
    OR email
3.4 Authorize GitHub access (if using GitHub auth)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4: DEPLOY TO RENDER (5 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4.1 Log in to Render Dashboard: https://dashboard.render.com
4.2 Click "+ New" button (top right)
4.3 Select "Web Service"
4.4 Select "Deploy from GitHub repo" or paste repo URL
    URL: https://github.com/YOUR_USERNAME/RAG_PIPELINE
4.5 Fill in the form:
    - Name: smart-rag-app
    - Environment: Docker
    - Region: Oregon (or closest to you)
    - Branch: main
    - Root Directory: (leave empty)
    - Build Command: (leave empty - Docker handles it)
    - Start Command: (leave empty - Docker ENTRYPOINT handles it)

4.6 Click "Create Web Service"
4.7 Render will start building... (takes 3-5 minutes)
    Watch the "Logs" tab to see progress

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5: ADD ENVIRONMENT VARIABLES (2 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

While Render is building, add your LLM API keys:

5.1 In Render Dashboard, go to your Web Service
5.2 Click "Environment" in the left sidebar
5.3 Click "Add Environment Variable"
5.4 Add these variables:

┌─ FOR OPENAI ─────────────────────────────────────────────────────────────┐
│ LLM_PROVIDER     = openai                                                 │
│ LLM_MODEL        = gpt-4o-mini                                            │
│ OPENAI_API_KEY   = sk-proj-your-actual-key-here                           │
└──────────────────────────────────────────────────────────────────────────┘

OR

┌─ FOR GOOGLE GEMINI ──────────────────────────────────────────────────────┐
│ LLM_PROVIDER   = gemini                                                   │
│ LLM_MODEL      = gemini-1.5-pro                                           │
│ GOOGLE_API_KEY = AIzaSyD-your-actual-key-here                             │
└──────────────────────────────────────────────────────────────────────────┘

OR

┌─ FOR OPENROUTER (RECOMMENDED) ──────────────────────────────────────────┐
│ LLM_PROVIDER         = openrouter                                         │
│ LLM_MODEL            = meta-llama/llama-3-8b-instruct                     │
│ OPENROUTER_API_KEY   = sk-or-your-actual-key-here                         │
└──────────────────────────────────────────────────────────────────────────┘

5.5 Click "Save" after each variable
5.6 Deployment will restart automatically with new variables

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 6: VERIFY DEPLOYMENT (5 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6.1 Check the "Logs" tab in Render:
    Look for these messages:
    ✅ "Docker build successful"
    ✅ "App running on 0.0.0.0:10000"
    ✅ "Application startup complete"

6.2 Your app URL will be displayed:
    https://smart-rag-app.onrender.com/

6.3 Test your app:
    
    Browser: https://smart-rag-app.onrender.com/
             (You should see the Smart RAG chat interface)
    
    API Docs: https://smart-rag-app.onrender.com/docs
              (Interactive API documentation)
    
    Health Check: https://smart-rag-app.onrender.com/health
                 (Should return: {"status": "healthy"})

6.4 If something fails:
    - Check the Logs tab for error messages
    - Verify all environment variables are set correctly
    - Look for "Module not found" or "Import errors"
    - Restart from Render dashboard

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 7: USE YOUR APP! 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7.1 Open: https://smart-rag-app.onrender.com/
7.2 Upload a document (PDF, Word, Excel, etc.)
7.3 Click "Index Document"
7.4 Start asking questions!
7.5 Share the URL with others - they can use it too!

Features available:
✓ Upload documents
✓ Real-time AI chat
✓ Source attribution
✓ Conversation history
✓ Multiple LLM providers
✓ Search documents
✓ REST API access

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTIONAL UPGRADES (When ready)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Persistent Database (Recommended for production)
   - Free SQLite resets after each deploy
   - For permanent data: Add PostgreSQL database to Render
   - Cost: From $15/month
   - Follow: RENDER_DEPLOYMENT.md → "OPTIONAL DATABASE SERVICE"

🌍 Custom Domain
   - Instead of: smart-rag-app.onrender.com
   - Use: your-domain.com
   - Steps: Render Dashboard → Settings → Custom Domain

⚡ Higher Performance
   - Free tier: May suspend after 15 mins inactivity
   - Starter: $7/month (always running)
   - Plus: $25/month (more power)

📧 Email Notifications
   - Get alerts on deployment failures
   - Settings → Notifications

🚀 Auto-Deploy from GitHub
   - Already enabled!
   - Every push to main = automatic deployment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ "Build failed" 
   → Check Logs for specific error
   → Make sure requirements.txt is in root folder
   → Verify render.yaml is in root folder

❌ "Import error" or "Module not found"
   → All dependencies are in requirements.txt ✓
   → Try: Restart from Render dashboard
   → If persists: Clear build cache → Redeploy

❌ "API key not working"
   → Verify exact key from provider
   → Check no spaces or extra characters
   → Make sure variable name matches (e.g., OPENAI_API_KEY not OPENAI_KEY)

❌ "App is crashing"
   → Check Logs tab
   → Look for error messages
   → Restart the service
   → If still fails: Check environment variables

❌ "Completely stuck?"
   → Check RENDER_DEPLOYMENT.md for detailed guide
   → Google search the error message
   → Contact Render support: https://render.com/support

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK REFERENCE - API ENDPOINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Base URL: https://smart-rag-app.onrender.com

POST   /api/sources              Create data source
GET    /api/sources              List data sources
POST   /api/index                Index documents
POST   /api/query                Ask questions (streaming)
POST   /api/search               Search documents
GET    /api/stats                System statistics
GET    /health                   Health check
GET    /docs                     API documentation (Swagger UI)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Follow Steps 1-7 above in order
2. Once deployed: Share your URL with team/users
3. Upload test documents and verify everything works
4. Monitor the app via Render Dashboard
5. Consider PostgreSQL for permanent data storage
6. Enjoy your Smart RAG application! 🚀

Questions?
- Full guide: Read RENDER_DEPLOYMENT.md
- GitHub: https://github.com/YOUR_USERNAME/RAG_PIPELINE
- Render docs: https://render.com/docs

""")
