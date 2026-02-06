# Quick Deployment Guides

Step-by-step guides for deploying the GDAL Image Processing app to various platforms.

## 🚂 Railway (Recommended - Easiest)

**Time:** 5 minutes | **Cost:** Free tier available

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `yashrahurikar23/terrascan-app`
6. Railway auto-detects Dockerfile
7. Click "Deploy"
8. Wait 2-3 minutes
9. ✅ Done! Your app is live with full GDAL support

**Auto-deploy:** Every git push automatically redeploys

---

## 🪰 Fly.io

**Time:** 10 minutes | **Cost:** Free tier (3 shared VMs)

1. Install flyctl:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. Login:
   ```bash
   flyctl auth login
   ```

3. In your project directory:
   ```bash
   cd /home/metheus/projects/terrascan-app-clone
   flyctl launch
   # Answer prompts (app name, region, etc.)
   ```

4. Deploy:
   ```bash
   flyctl deploy
   ```

5. Open your app:
   ```bash
   flyctl open
   ```

**Auto-deploy:** Set up GitHub Actions or use `flyctl deploy` manually

---

## ☁️ Google Cloud Run

**Time:** 15 minutes | **Cost:** Free tier (2M requests/month)

1. Install gcloud CLI:
   ```bash
   # Follow: https://cloud.google.com/sdk/docs/install
   ```

2. Authenticate:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. Enable APIs:
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

4. Deploy:
   ```bash
   gcloud run deploy gdal-app \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8501
   ```

5. Get URL:
   ```bash
   gcloud run services describe gdal-app --region us-central1
   ```

---

## 🐳 DigitalOcean App Platform

**Time:** 10 minutes | **Cost:** $5/month (no free tier)

1. Go to https://cloud.digitalocean.com/apps
2. Sign up/Login
3. Click "Create App"
4. Connect GitHub account
5. Select repository: `yashrahurikar23/terrascan-app`
6. App Platform detects Dockerfile automatically
7. Review settings (can leave defaults)
8. Click "Create Resources"
9. Wait for deployment
10. ✅ Done!

**Auto-deploy:** Enabled by default on git push

---

## 🌊 Render

**Time:** 5 minutes | **Cost:** Free tier (spins down after inactivity)

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect repository: `yashrahurikar23/terrascan-app`
5. Settings:
   - **Name:** gdal-app (or your choice)
   - **Environment:** Docker
   - **Region:** Choose closest
   - **Branch:** main
6. Click "Create Web Service"
7. Wait for build and deploy
8. ✅ Done!

**Note:** Free tier spins down after 15 min inactivity (takes ~30s to wake up)

---

## ☁️ AWS App Runner

**Time:** 20 minutes | **Cost:** Pay-per-use (~$0.007/vCPU-hour)

1. Go to AWS Console → App Runner
2. Create service
3. Source:
   - Option A: Connect GitHub (requires AWS CodeStar connection)
   - Option B: Use ECR (push Docker image first)
4. Configure:
   - Service name: gdal-app
   - Port: 8501
   - Auto-deploy: Enabled
5. Create service
6. Wait for deployment
7. ✅ Done!

**More complex** but good for AWS ecosystem integration

---

## 🐳 Azure Container Instances

**Time:** 20 minutes | **Cost:** $200 free credit for 30 days

1. Install Azure CLI:
   ```bash
   # Follow: https://docs.microsoft.com/cli/azure/install-azure-cli
   ```

2. Login:
   ```bash
   az login
   ```

3. Create resource group:
   ```bash
   az group create --name gdal-app-rg --location eastus
   ```

4. Build and push to Azure Container Registry (or use GitHub Actions)

5. Deploy:
   ```bash
   az container create \
     --resource-group gdal-app-rg \
     --name gdal-app \
     --image YOUR_REGISTRY/gdal-app:latest \
     --dns-name-label gdal-app \
     --ports 8501 \
     --cpu 1 \
     --memory 1.5
   ```

---

## 🚀 Vercel

**Time:** 5 minutes | **Cost:** Free tier

1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Add New" → "Project"
4. Import repository: `yashrahurikar23/terrascan-app`
5. Framework Preset: Docker
6. Click "Deploy"
7. ✅ Done!

**Note:** Vercel is optimized for frontend, but Docker support works

---

## 🌐 Netlify

**Time:** 5 minutes | **Cost:** Free tier

1. Go to https://www.netlify.com
2. Sign up with GitHub
3. Click "Add new site" → "Import an existing project"
4. Connect repository
5. Build settings:
   - Build command: (leave empty, Docker handles it)
   - Publish directory: (not needed for Docker)
6. Environment: Docker
7. Deploy!
8. ✅ Done!

---

## 🐋 Heroku (Container Registry)

**Time:** 15 minutes | **Cost:** Paid only (no free tier)

1. Install Heroku CLI:
   ```bash
   # Follow: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. Login:
   ```bash
   heroku login
   heroku container:login
   ```

3. Create app:
   ```bash
   heroku create gdal-app
   ```

4. Build and push:
   ```bash
   heroku container:push web
   heroku container:release web
   ```

5. Open:
   ```bash
   heroku open
   ```

---

## 🏠 Local Docker (Development)

**Time:** 2 minutes | **Cost:** Free

```bash
# Navigate to project
cd /home/metheus/projects/image_processing

# Build image
docker build -t gdal-app .

# Run container
docker run -p 8501:8501 gdal-app

# Or use docker-compose
docker-compose up
```

Access at: http://localhost:8501

---

## Recommendation by Use Case

- **Quickest Setup:** Railway or Render
- **Best Free Tier:** Google Cloud Run or Fly.io
- **Enterprise:** Google Cloud Run or AWS App Runner
- **Development:** Local Docker
- **Budget-Conscious:** Render (free) or DigitalOcean ($5/mo)
- **Global Edge:** Fly.io
- **Familiar Platform:** Heroku (if you've used it before)

All platforms with Docker support will have **full GDAL functionality**! 🎉
