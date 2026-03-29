#!/bin/bash
# ============================================================================
# RENDER DEPLOYMENT GUIDE - Smart RAG Pipeline
# ============================================================================
# Step-by-step instructions to deploy to Render.com
# ============================================================================

## STEP 1: PREPARE YOUR GITHUB REPOSITORY
# ============================================================================

# 1.1 Make sure the project is in a GitHub repository
#     - If not already on GitHub:
#       git init
#       git add .
#       git commit -m "Initial commit"
#       git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
#       git branch -M main
#       git push -u origin main

# 1.2 Push all files to GitHub (including new render.yaml and Procfile)
#     git add .
#     git commit -m "Add Render deployment configuration"
#     git push


## STEP 2: CREATE RENDER ACCOUNT
# ============================================================================

# Go to https://render.com and sign up for free
# Connect your GitHub account to Render


## STEP 3: CREATE A NEW WEB SERVICE
# ============================================================================

# 3.1 Log in to Render Dashboard: https://dashboard.render.com
# 3.2 Click "+ New" button → "Web Service"
# 3.3 Select your GitHub repository (RAG_PIPELINE)
# 3.4 Render will auto-detect render.yaml file
# 3.5 Fill in service details:
#     - Name: smart-rag-app
#     - Environment: Docker
#     - Region: oregon (or your preferred region)
#     - Branch: main


## STEP 4: SET ENVIRONMENT VARIABLES
# ============================================================================

# In Render Dashboard, go to your Web Service → Settings → Environment
# Add these variables:

# Choose ONE of the following LLM providers:

# OPTION A: OpenAI (Best Quality)
# - LLM_PROVIDER = openai
# - LLM_MODEL = gpt-4o-mini
# - OPENAI_API_KEY = sk-your-actual-key-here
#   Get key: https://platform.openai.com/api-keys

# OPTION B: Google Gemini (Free Tier Available)
# - LLM_PROVIDER = gemini
# - LLM_MODEL = gemini-1.5-pro
# - GOOGLE_API_KEY = your-actual-key-here
#   Get key: https://makersuite.google.com/app/apikey

# OPTION C: OpenRouter (CHEAPEST - RECOMMENDED)
# - LLM_PROVIDER = openrouter
# - LLM_MODEL = meta-llama/llama-3-8b-instruct
# - OPENROUTER_API_KEY = sk-or-your-actual-key-here
#   Get key: https://openrouter.ai/keys


## STEP 5: DEPLOY
# ============================================================================

# Click "Deploy" button
# Render will:
#   1. Clone your GitHub repo
#   2. Build the Docker image
#   3. Start the container
#   4. Assign a public URL (like: smart-rag-app.onrender.com)
#   5. Start your services

# Wait 5-10 minutes for deployment to complete...


## STEP 6: VERIFY DEPLOYMENT
# ============================================================================

# Check logs:
#   - Go to Render Dashboard
#   - Select your service
#   - Click "Logs" tab
#   - Look for:
#     ✅ "Backend running on 0.0.0.0:10000"
#     ✅ "Server running on http://localhost:3000"
#     ✅ "Application startup complete"

# Test backend API:
#   curl https://smart-rag-app.onrender.com/health

# Test frontend:
#   Open: https://smart-rag-app.onrender.com in your browser


## STEP 7: TROUBLESHOOTING
# ============================================================================

# Issue: "Build failed" or "Application crashed"
# Solution:
#   1. Check Render logs for error messages
#   2. Verify all environment variables are set
#   3. Make sure render.yaml is in root directory
#   4. Try manual redeploy from Render dashboard

# Issue: "Port already in use"
# Solution:
#   Our updated code uses $PORT (Render's assigned port), not hardcoded ports
#   This is already fixed in the setup!

# Issue: "Module not found" or "import error"
# Solution:
#   1. Check requirements.txt has all dependencies
#   2. Try rebuilding from Render dashboard
#   3. Run: pip install -r requirements.txt locally to verify

# Issue: "Database errors" or "FileNotFoundError"
# Solution:
#   - SQLite uses /tmp (temporary storage - doesn't persist between deploys)
#   - For persistent database, upgrade to PostgreSQL on Render
#   - See render.yaml for database configuration


## STEP 8: OPTIONAL - USE POSTGRESQL
# ============================================================================

# For production use, switch from SQLite to PostgreSQL:
# 
# 1. In Render Dashboard, click "New +" → "PostgreSQL"
# 2. Fill in database details
# 3. Copy the database URL
# 4. Add to Web Service environment variables:
#    - DATABASE_URL = postgres://user:password@host:5432/dbname
# 5. Update backend/app/config.py to use DATABASE_URL instead of SQLite
# 6. Redeploy


## STEP 9: MONITORING & MAINTENANCE
# ============================================================================

# Real-time logs:
#   - Dashboard → Logs tab (auto-updates)
#   - Shows all API requests and errors

# Metrics:
#   - Dashboard → Metrics tab
#   - Monitor CPU, Memory, Network usage

# Email alerts:
#   - Enable in account settings
#   - Get notified of deployment failures, crashes, etc.

# Auto-deploy:
#   - Enabled by default
#   - Every push to main branch triggers new deployment
#   - Can be disabled in service settings


## STEP 10: SCALING & OPTIMIZATION
# ============================================================================

# Instance count:
#   - Settings → Instances
#   - Set to 2-3 for better reliability
#   - Auto-scales if CPU/memory spikes

# Concurrency:
#   - Current setup handles ~50 concurrent users
#   - Scale up with more instances or move to higher plan

# Performance tips:
#   - Use CDN for static frontend files
#   - Cache embeddings in vector store
#   - Use connection pooling for database


## COMMON COMMANDS
# ============================================================================

# View logs (from local terminal):
# - Go to Render dashboard → Logs (easier)

# Restart service:
#   - Dashboard → More options → Restart

# Deploy latest code:
#   - Push to GitHub
#   - Render auto-deploys (or manually trigger from dashboard)

# Check service status:
#   - Dashboard → Shows "Live" if running, "Building" if deploying


## PRICING (Render Free Tier)
# ============================================================================

# Free services get suspended after 15 mins of inactivity
# For production:
#   - Starter: $7/month (always running)
#   - Plus: $25/month (more power)
#   - Pro: $100+/month (high performance)

# Database (PostgreSQL):
#   - Free: Limited, auto-delete after 90 days
#   - Starter: $15/month onwards


## NEXT STEPS
# ============================================================================

# After deployment:
# 1. Test all API endpoints
# 2. Upload some documents to test RAG
# 3. Monitor logs and metrics
# 4. Share the public URL with users
# 5. Configure custom domain (optional)
# 6. Set up email alerts


# ============================================================================
# Questions? Issues?
# ============================================================================
# - Render Docs: https://render.com/docs
# - GitHub Issues: https://github.com/YOUR_REPO/issues
# - Community: https://discord.gg/render
# ============================================================================
