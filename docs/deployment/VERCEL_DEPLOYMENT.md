# Vercel Deployment Guide (⚠️ Not Recommended)

## ⚠️ Important Notice

**Vercel is NOT ideal for Streamlit applications** because:
- Vercel is designed for serverless functions and static sites
- Streamlit requires a persistent server process
- Long-running operations may timeout
- Better suited for Next.js, React, and other frontend frameworks

## Recommended Alternatives

For Streamlit apps, these platforms work much better:

1. **🚂 Railway** (Easiest) - https://railway.app
2. **🌊 Render** (Good free tier) - https://render.com
3. **🪰 Fly.io** (Global edge) - https://fly.io
4. **☁️ Google Cloud Run** (Enterprise) - https://cloud.google.com/run

## If You Still Want to Try Vercel

### Prerequisites

1. Vercel account (sign up at https://vercel.com)
2. GitHub repository connected
3. Dockerfile in your repository

### Deployment Steps

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/dashboard
   - Click "Add New" → "Project"

2. **Import Repository**
   - Select `yashrahurikar23/terrascan-app`
   - Click "Import"

3. **Configure Project**
   - **Framework Preset:** Docker
   - **Root Directory:** `.` (default)
   - **Build Command:** (leave empty - Docker handles it)
   - **Output Directory:** (leave empty)
   - **Install Command:** (leave empty)

4. **Environment Variables** (if needed)
   - Add any required environment variables
   - For Streamlit: Usually none needed

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete

### Known Issues

- **Timeout Issues:** Streamlit operations may timeout
- **Cold Starts:** Serverless functions have cold start delays
- **Long Operations:** Image processing may exceed function timeout limits
- **WebSocket Support:** May have issues with Streamlit's WebSocket connections

### Configuration Files

The repository includes:
- `vercel.json` - Vercel configuration
- `Dockerfile` - Docker container definition

### Troubleshooting

**Issue: "Cannot detect framework"**
- Solution: Manually select "Docker" as framework preset

**Issue: "Build timeout"**
- Solution: Vercel has build time limits. Consider using Railway or Render instead.

**Issue: "App doesn't work after deployment"**
- Solution: Vercel may not be suitable for Streamlit. Try Railway or Render.

## Better Options for Streamlit

### Railway (Recommended)
```bash
# 1. Go to railway.app
# 2. Sign up with GitHub
# 3. New Project → Deploy from GitHub
# 4. Select repository
# 5. Railway auto-detects Dockerfile
# 6. Deploy! ✅
```

### Render
```bash
# 1. Go to render.com
# 2. Sign up with GitHub
# 3. New → Web Service
# 4. Connect repository
# 5. Environment: Docker
# 6. Deploy! ✅
```

## Conclusion

While Vercel supports Docker, **it's not the best choice for Streamlit apps**. 

**For best results, use:**
- ✅ Railway (easiest, best for Streamlit)
- ✅ Render (good free tier)
- ✅ Fly.io (global edge network)
- ✅ Google Cloud Run (enterprise-grade)

These platforms are designed for long-running applications like Streamlit and will provide a much better experience.
