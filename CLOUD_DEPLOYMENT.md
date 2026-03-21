# 🌐 Cloud Deployment Guide - Smart RAG Project

Complete guide to deploy your Smart RAG project to any major cloud platform.

---

## 📋 Quick Navigation

- **[Google Cloud Run](#google-cloud-run)** - Serverless, easiest start
- **[AWS (EC2, ECS, Fargate)](#aws-deployment)** - Traditional VPS, containerized, serverless
- **[Azure (App Service, Container Instances)](#azure-deployment)** - Enterprise-grade
- **[Heroku](#heroku-deployment)** - Fastest setup, free alternatives available
- **[DigitalOcean](#digitalocean-deployment)** - Affordable, simple
- **[Railway](#railway-deployment)** - Modern, simple deployment
- **[Render](#render-deployment)** - Quick, cheap, good for learning
- **[Replit](#replit-deployment)** - Browser-based, instant sharing

---

## 🚀 Pre-Deployment Checklist

Before deploying to ANY cloud platform:

- [ ] Create API key with your chosen LLM provider (OpenAI, Gemini, or OpenRouter)
- [ ] Test locally with `START_ALL_WEB.bat` or `docker-compose up`
- [ ] Create `.env` file with your API keys (don't share this file!)
- [ ] Verify all tests pass: `python test_app_simple.py`
- [ ] Review `requirements.txt` for your Python version compatibility
- [ ] Decide on storage: local (smaller) or cloud storage (scalable)
- [ ] Plan for data persistence (database + vector store)

---

## 🏆 Recommended Platforms by Use Case

### For Learning / Testing
**Best:** Replit, Railway, Render
- Free tier available
- Quick deployment (minutes)
- No credit card needed initially

### For Small Production
**Best:** Heroku Free Alternative, DigitalOcean, Railway
- Affordable ($0-$20/month)
- Easy to manage
- Good persistance

### For High Traffic
**Best:** AWS, Google Cloud, Azure
- Scalable
- Higher cost
- Professional features

### For Enterprise
**Best:** Azure, AWS
- Security features
- Compliance tracking
- Enterprise support

---

## 🏃 Google Cloud Run (RECOMMENDED FOR START)

**Why Google Cloud Run?**
- ✅ Easiest serverless deployment
- ✅ Free tier: 2 million requests/month
- ✅ Scales automatically
- ✅ Pay only for what you use
- ⏱️ Setup time: 10 minutes

### Step-by-Step Deployment

#### 1. **Create Google Cloud Account**
```
https://cloud.google.com
Click "Get started for free"
Set up billing (required, but free tier available)
```

#### 2. **Enable APIs**
```
- Go to Cloud Console
- Enable "Cloud Run API"
- Enable "Container Registry API"
```

#### 3. **install Google Cloud CLI**
```powershell
# Download from: https://cloud.google.com/sdk/docs/install-windows
# Or use Windows installer

# Verify installation
gcloud --version
```

#### 4. **Authenticate**
```powershell
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### 5. **Create .env file**
```powershell
# Create .env with your API keys
Copy-Item .env.example .env
# Edit .env with your actual API keys
```

#### 6. **Build and Deploy**
```powershell
# Deploy directly from source
gcloud run deploy smart-rag `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars OPENAI_API_KEY=your-key,GOOGLE_API_KEY=your-key

# OR build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT/smart-rag
gcloud run deploy smart-rag `
  --image gcr.io/YOUR_PROJECT/smart-rag `
  --platform managed `
  --region us-central1
```

#### 7. **Set Environment Variables**
```
In Google Cloud Console:
- Go to Cloud Run
- Click on your service
- Click "Edit"
- Add environment variables from .env
- Deploy
```

#### 8. **Access Your App**
```
https://smart-rag-[random].run.app
```

### Important Notes for Cloud Run

**Data Persistence:**
- Cloud Run doesn't have persistent disk
- For persistent data, use:
  - Cloud Firestore (managed database)
  - Cloud Storage (for vector store)
  - Cloud SQL (traditional database)

**Alternative: Simple Setup (stateless)**
```
# If you don't need to persist documents:
# Just upload documents in one session
# Data stays for that session only
# Good for: Testing, demos, learning
```

---

## 🏗️ AWS Deployment

**Options:**
1. **EC2** - Full control, cheapest for always-on
2. **ECS Fargate** - Containerized, scalable, moderate cost
3. **Elastic Beanstalk** - Managed environment, easiest

### Option 1: EC2 (Simplest)

#### 1. **Create EC2 Instance**
```
- Go to AWS Console → EC2
- Launch Instance
- Choose: Ubuntu Server 22.04 LTS (free tier eligible)
- Instance type: t2.micro (free tier) or t2.small (better)
- Security Group: Allow HTTP (80), HTTPS (443), SSH (22)
```

#### 2. **Connect to Server**
```powershell
# Download key pair (save as .pem file)
# Connect via SSH or AWS Systems Manager

# Optional: Use PuTTY (Windows SSH client)
```

#### 3. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3.11 python3-pip git -y

# Clone your project
git clone https://github.com/your-username/smart-rag.git
cd smart-rag
```

#### 4. **Setup Virtual Environment**
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

#### 5. **Create .env File**
```bash
cp .env.example .env
# Edit .env with your API keys (use nano or vi)
nano .env
```

#### 6. **Run Application**
```bash
# Start backend (background)
nohup python backend/run.py > backend.log 2>&1 &

# Start frontend (background)
nohup python frontend_server.py > frontend.log 2>&1 &

# Check logs
tail -f backend.log
tail -f frontend.log
```

#### 7. **Access Your App**
```
http://your-ec2-public-ip:3000
```

### Option 2: AWS ECS with Docker

#### 1. **Push to ECR (Elastic Container Registry)**
```powershell
# Create ECR repository
aws ecr create-repository --repository-name smart-rag --region us-east-1

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [your-account-id].dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t smart-rag .
docker tag smart-rag:latest [your-account-id].dkr.ecr.us-east-1.amazonaws.com/smart-rag:latest
docker push [your-account-id].dkr.ecr.us-east-1.amazonaws.com/smart-rag:latest
```

#### 2. **Create ECS Cluster**
```
- AWS Console → ECS
- Create Cluster
- Choose EC2 or Fargate
- Configure instances
```

#### 3. **Create Task Definition**
```
- ECS → Task Definitions
- Create new task
- Container image: your ECR image URL
- Memory: 512 MB
- CPU: 256
```

#### 4. **Create Service**
```
- Create Service from task definition
- Load balancer: Application Load Balancer
- Set environment variables
```

---

## ☁️ Azure Deployment

### Option 1: Azure Container Instances (Simplest)

```powershell
# 1. Create resource group
az group create --name smart-rag-rg --location eastus

# 2. Create container registry
az acr create -g smart-rag-rg -n smartragacr --sku Basic

# 3. Build and push image
az acr build -r smartragacr --image smart-rag:latest .

# 4. Deploy container
az container create `
  --resource-group smart-rag-rg `
  --name smart-rag-container `
  --image smartragacr.azurecr.io/smart-rag:latest `
  --cpu 1 `
  --memory 1 `
  --ports 8000 3000 `
  --environment-variables OPENAI_API_KEY=your-key
```

### Option 2: Azure App Service

```powershell
# Create App Service Plan
az appservice plan create `
  --name smart-rag-plan `
  --resource-group smart-rag-rg `
  --sku B1 `
  --is-linux

# Create Web App
az webapp create `
  --resource-group smart-rag-rg `
  --plan smart-rag-plan `
  --name smart-rag-app `
  --runtime "PYTHON|3.11"

# Configure environment variables
az webapp config appsettings set `
  --resource-group smart-rag-rg `
  --name smart-rag-app `
  --settings OPENAI_API_KEY=your-key
```

---

## 🎈 Heroku Deployment (Easiest Alternative)

**Why Heroku?**
- Simplest setup
- Just push to git
- Free alternatives available (like Railway)

### Step-by-Step

#### 1. **Create Procfile**
```
Create file: Procfile (no extension)
Content:
web: python backend/run.py --host 0.0.0.0 --port $PORT
worker: python frontend_server.py
```

#### 2. **Create runtime.txt**
```
python-3.11.7
```

#### 3. **Create Heroku Account**
```
https://www.heroku.com
Sign up (free account available)
```

#### 4. **Install Heroku CLI**
```powershell
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login
```

#### 5. **Deploy**
```powershell
# Create app
heroku create smart-rag-app

# Set environment variables
heroku config:set OPENAI_API_KEY=your-key
heroku config:set GOOGLE_API_KEY=your-key
heroku config:set OPENROUTER_API_KEY=your-key

# Deploy (push to Heroku git)
git push heroku main

# View logs
heroku logs --tail
```

---

## 💻 DigitalOcean Deployment

### $4-6/month App Platform

```powershell
# 1. Create DigitalOcean account
# https://www.digitalocean.com

# 2. Create App Platform project
# - Connect GitHub repo
# - Auto-detects Python app
# - Configure build command: pip install -r requirements.txt

# 3. Configure components
# - Service: backend (python backend/run.py)
# - Service: frontend (python frontend_server.py)
# - Database: PostgreSQL (optional)

# 4. Set environment variables
# Go to App Settings → Environment Variables
# Add: OPENAI_API_KEY, etc.

# 5. Deploy (automatic on git push)
```

---

## 🚄 Railway Deployment (Modern & Easy)

**Why Railway?**
- ✅ Super simple (5 minutes)
- ✅ $5 free/month
- ✅ Pay-as-you-go after
- ✅ GitHub integration

```powershell
# 1. Go to https://railway.app
# 2. Sign up with GitHub
# 3. New Project → Deploy Dockerfile
# 4. Connect GitHub repository
# 5. Set environment variables
# 6. Deploy! (automatic)
```

---

## 🎯 Render Deployment

```
1. Go to https://render.com
2. New Web Service
3. Connect GitHub
4. Choose Docker
5. Configure:
   - Build command: docker build -t smart-rag .
   - Start command: python backend/run.py
6. Add environment variables
7. Deploy!
```

---

## 💾 Data Persistence Options

### Option 1: Local Storage (Simplest)
```
- Data stored in container
- Lost when container restarts
- Good for: Testing, demos
```

### Option 2: Cloud Storage (Best)

**AWS S3:**
```python
# In your code:
import boto3
s3 = boto3.client('s3')
# Store FAISS index and DB in S3
```

**Google Cloud Storage:**
```python
from google.cloud import storage
client = storage.Client()
# Store in GCS buckets
```

**Azure Blob Storage:**
```python
from azure.storage.blob import BlobServiceClient
# Store in Azure Blob
```

### Option 3: Managed Database

**AWS RDS:** PostgreSQL/MySQL database
**Azure Database:** Managed SQL
**Google Cloud SQL:** PostgreSQL/MySQL

---

## 🔒 Security Best Practices for Cloud

1. **Never commit .env file**
   - Use .env.example as template
   - Add .env to .gitignore
   - Set env vars in cloud platform UI

2. **Use Environment Variables**
   - Store API keys as env vars
   - Don't hardcode secrets
   - Rotate keys regularly

3. **Use HTTPS**
   - All cloud platforms provide free HTTPS
   - Redirect HTTP to HTTPS

4. **Database Security**
   - Use strong passwords
   - Enable encryption at rest
   - Regular backups

5. **Monitor Logs**
   - Review error logs regularly
   - Set up alerts for crashes
   - Monitor API usage

---

## 📊 Cost Comparison

| Platform | Free Tier | Paid (Min) | Notes |
|----------|-----------|-----------|-------|
| Google Cloud Run | 2M req/mo | $0.40/M req | Serverless, scales |
| Heroku | ❌ Limited | $7/mo | Simple, easiest |
| Railway | $5/mo | Start low | Modern, friendly |
| Render | ❌ Maybe | $7/mo | Good free tier |
| DigitalOcean | ❌ | $4/mo | Always on, cheapest |
| AWS EC2 | 12 mo | $11/mo+ | Full control |
| Azure | First $200 | $15/mo+ | Enterprise |

---

## 🆘 Troubleshooting Cloud Deployment

### Issue: "ModuleNotFoundError"
- Check requirements.txt is in root
- Ensure all dependencies listed
- Rebuild container: `docker build --no-cache .`

### Issue: "API key not working"
- Verify env var name matches code
- Check key is correct (not truncated)
- Restart container after setting vars

### Issue: "Port already in use"
- Change port in .env or env vars
- Use 8000+ for backend, 3000+ for frontend
- Cloud platforms expose specific ports

### Issue: "No space left in container"
- Delete old vector stores: `rm -rf backend/data/*`
- Use cloud storage instead
- Increase container size allocation

### Issue: "Timeout on first request"
- Backend takes time to start
- Cloud platforms kill slow starts
- Add healthcheck endpoint
- Increase startup timeout

---

## 🎓 Recommended Learning Path

**Total Time: 2-3 hours**

1. **Local Testing (20 min)**
   - Run `docker-compose up` locally
   - Verify everything works

2. **Free Platform (30 min)**
   - Deploy to Railway or Render
   - Share link with friends

3. **Scalable Platform (1 hour)**
   - Migrate to Google Cloud Run
   - Set up cloud storage

4. **Production Setup (1 hour)**
   - Use AWS or Azure
   - Set up monitoring/alerts
   - Configure backups

---

## 📞 Platform Support Links

- **Google Cloud:** https://cloud.google.com/support
- **AWS:** https://aws.amazon.com/support
- **Azure:** https://azure.microsoft.com/support
- **Heroku:** https://help.heroku.com
- **Railway:** https://railway.app/support
- **DigitalOcean:** https://www.digitalocean.com/support
- **Render:** https://docs.render.com

---

## ✅ Deployment Verification

After deploying, verify:
- [ ] App loads without errors
- [ ] Can upload documents
- [ ] Can ask questions
- [ ] Answers appear in chat
- [ ] Data persists after restart
- [ ] No sensitive data in logs
- [ ] Error handling works

---

## 🎉 Next Steps

1. Choose a platform based on your needs
2. Follow the step-by-step guide above
3. Test thoroughly before sharing
4. Monitor costs and usage
5. Scale as needed

**Your Smart RAG project is now ready for the world!** 🚀
