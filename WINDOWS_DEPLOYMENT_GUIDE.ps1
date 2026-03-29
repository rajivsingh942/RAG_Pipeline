#!/usr/bin/env pwsh
# ============================================================================
# SMART RAG DEPLOYMENT - STEP BY STEP GUIDE (Windows PowerShell)
# ============================================================================
# This script will help you deploy to Render.com in less than 5 minutes

Write-Host "
╔════════════════════════════════════════════════════════════════════════════╗
║                 SMART RAG - RENDER.COM DEPLOYMENT GUIDE                   ║
║                                                                            ║
║  This guide will help you deploy your RAG app for FREE on Render.com     ║
║  Estimated time: 5 minutes setup + 10 minutes deployment                  ║
╚════════════════════════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

# ============================================================================
# PRE-DEPLOYMENT CHECKS
# ============================================================================

Write-Host "`n📋 PRE-DEPLOYMENT CHECKLIST" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════════"

$checks = @{
    "Dockerfile present" = "Dockerfile"
    "render.yaml present" = "render.yaml"
    "requirements.txt present" = "requirements.txt"
    ".env.example present" = ".env.example"
    "Git repository initialized" = ".git"
}

$allOK = $true
foreach ($check in $checks.GetEnumerator()) {
    $exists = Test-Path $check.Value
    $status = if ($exists) { "✅ PASS" } else { "❌ FAIL" }
    Write-Host "$status - $($check.Name)"
    if (-not $exists) { $allOK = $false }
}

if (-not $allOK) {
    Write-Host "`n⚠️  CRITICAL: Some required files are missing!" -ForegroundColor Red
    Write-Host    "Please ensure you're in the RAG_PIPELINE directory"
    exit 1
}

# ============================================================================
# GITHUB SETUP
# ============================================================================

Write-Host "`n🔐 GITHUB SETUP (Choose Step)" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════════"

Write-Host @"

OPTION 1: New GitHub Repository
───────────────────────────────
1. Go to https://github.com/new
2. Enter repository name: rag-pipeline
3. Choose "Public" (required for Render free tier)
4. Click "Create repository"
5. You'll see these commands - run them below

OPTION 2: Existing Repository
──────────────────────────────
If you already have a repo, just follow the GitHub push instructions

"@ -ForegroundColor Cyan

# Get repository URL
$repoURL = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/rag-pipeline.git)"

if ([string]::IsNullOrWhiteSpace($repoURL)) {
    Write-Host "❌ Repository URL is required!" -ForegroundColor Red
    exit 1
}

Write-Host "`n📤 PUSHING CODE TO GITHUB" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════════"

try {
    Write-Host "Setting git remote..."
    git remote remove origin 2>$null
    git remote add origin $repoURL
    
    Write-Host "Setting main branch..."
    git branch -M main
    
    Write-Host "Pushing code..."
    git push -u origin main
    
    Write-Host "✅ Code pushed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Git push failed!" -ForegroundColor Red
    Write-Host "Make sure:"
    Write-Host "  1. Git is installed"
    Write-Host "  2. You're authenticated with GitHub"
    Write-Host "  3. The repository URL is correct"
    Write-Host "  4. Try: git push --force-with-lease"
    exit 1
}

# ============================================================================
# RENDER DEPLOYMENT INSTRUCTIONS
# ============================================================================

Write-Host "`n🚀 RENDER.COM DEPLOYMENT STEPS" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════════"

Write-Host @"

STEP 1: Create Render Account (if you don't have one)
──────────────────────────────────────────────────────
→ Go to https://render.com
→ Click "Sign up"
→ Sign up with GitHub (easiest way)
→ Authorize Render to access GitHub

STEP 2: Create a Web Service
─────────────────────────────
→ Go to Dashboard: https://dashboard.render.com
→ Click "+ New" button
→ Select "Web Service"
→ Click "Connect GitHub account" if not done
→ Select repository: rag-pipeline
→ Render will auto-detect render.yaml ✓

STEP 3: Configure Service
──────────────────────────
→ Service Name: smart-rag-app
→ Environment: Docker (auto-selected)
→ Region: oregon (free tier available)
→ Branch: main
→ Click "Create Web Service"

STEP 4: Set Environment Variables ⚠️  IMPORTANT
────────────────────────────────────────────────
Go to "Settings" tab → "Environment" → Add Variables:

CHOOSE ONE LLM PROVIDER:

═══════════════════════════════════════════════════════════════════════════

OPTION A: GOOGLE GEMINI (RECOMMENDED - FREE)
═════════════════════════════════════════════

LLM_PROVIDER         = gemini
LLM_MODEL            = gemini-1.5-pro  
GOOGLE_API_KEY       = your-key-here

How to get key:
→ Go to https://makersuite.google.com/app/apikey
→ Click "Create API Key"
→ Copy the key
→ Paste in Render dashboard

═══════════════════════════════════════════════════════════════════════════

OPTION B: OPENAI (HIGHEST QUALITY - $5 FREE CREDIT)
════════════════════════════════════════════════════

LLM_PROVIDER         = openai
LLM_MODEL            = gpt-4o-mini
OPENAI_API_KEY       = sk-your-key-here

How to get key:
→ Go to https://platform.openai.com/api-keys
→ Sign up / Login
→ Create new API key
→ Copy paste here (includes \$5 free credit)

═══════════════════════════════════════════════════════════════════════════

OPTION C: OPENROUTER (CHEAPEST)
════════════════════════════════

LLM_PROVIDER         = openrouter
LLM_MODEL            = meta-llama/llama-3-8b-instruct
OPENROUTER_API_KEY   = sk-or-your-key-here

How to get key:
→ Go to https://openrouter.ai/keys
→ Sign up with GitHub
→ Copy your API key

═══════════════════════════════════════════════════════════════════════════

STEP 5: Deploy
──────────────
→ Click "Deploy"
→ Wait 5-10 minutes for build to complete
→ Check logs for errors (if any)

STEP 6: Access Your App
────────────────────────
Once deployment completes, you'll see:
✅ "Deployment successful"

Your app will be live at:
   https://smart-rag-app.onrender.com

Access points:
- Frontend: https://smart-rag-app.onrender.com
- Backend API: https://smart-rag-app.onrender.com/api/
- API Docs: https://smart-rag-app.onrender.com/docs
- Health Check: https://smart-rag-app.onrender.com/health

"@ -ForegroundColor Cyan

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

Write-Host "`n⚙️  TROUBLESHOOTING" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════════"

Write-Host @"

❌ Deployment Failed?
────────────────────
1. Check Render Logs:
   - Go to Service → Logs
   - Look for errors
   
2. Common Issues:
   - Missing environment variables → Add them in Settings
   - Invalid API key → Check key format
   - Port issues → Already fixed in render.yaml
   
3. Check Health:
   - Wait 5 minutes after deploy
   - Refresh the page
   - Check if you can access /health endpoint

❌ App Loads But Can't Use Chat?
────────────────────────────────
- Check if API key is correct
- Check if LLM_PROVIDER matches the key
- Check Render logs for error messages

❌ DNS Error (rag-pipeline.onrender.com not found)?
───────────────────────────────────────────────────
- Render takes a few minutes to set up DNS
- Wait 2-3 minutes and try again
- Clear browser cache (Ctrl+Shift+Delete)

" -ForegroundColor Yellow

# ============================================================================
# FINAL SUMMARY
# ============================================================================

Write-Host "`n📊 DEPLOYMENT SUMMARY" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════════════"

Write-Host @"

✅ What You're Deploying:
   - FastAPI Backend (Python)
   - React Frontend (JavaScript)
   - SQLite Database
   - FAISS Vector Store
   
✅ Features Included:
   - Multi-LLM Support
   - Real-time Streaming
   - Vector Search
   - Conversation Memory
   - Source Attribution
   
✅ Free Tier Includes:
   - 750 free hours/month (always on)
   - 100GB bandwidth/month
   - Custom domain support
   - Automatic SSL/HTTPS
   
⚠️  Important Notes:
   - Render will RESTART your app if idle for 15 minutes
   - To keep it always on: upgrade to paid plan (\$7/month)
   - Or just restart when needed
   
🎯 Next Steps:
   1. Create GitHub repo
   2. Push code (done above ✓)
   3. Sign up on Render.com
   4. Deploy using render.yaml
   5. Add API keys in environment variables
   6. Access your live app! 🎉

"@ -ForegroundColor Green

Write-Host "`n✨ DEPLOYMENT GUIDE COMPLETE!" -ForegroundColor Cyan
Write-Host "Go to https://dashboard.render.com to complete deployment" -ForegroundColor Cyan
