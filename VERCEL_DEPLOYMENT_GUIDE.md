# 🚀 Vercel Deployment Guide - Todo Application

This guide will help you deploy the Phase II Todo application to Vercel (frontend) and Railway (backend) so everyone can access it online!

## 📋 Prerequisites

Before you start, you'll need:
- ✅ GitHub account (already configured)
- ✅ Vercel account (free at https://vercel.com)
- ✅ Railway account (free at https://railway.app)
- ✅ Project pushed to GitHub (already done ✓)

---

## 🎯 Deployment Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                     PRODUCTION ARCHITECTURE                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Vercel (Frontend)           Railway (Backend)              │
│  ─────────────────           ──────────────                 │
│                                                               │
│  https://todo.vercel.app ←──→ https://api-todo.railway.app │
│  (Next.js React App)          (FastAPI Backend)            │
│                                                               │
│  • Auto-deploys on push      • Auto-deploys on push        │
│  • Global CDN                • Automatic scaling            │
│  • Serverless Functions      • Environment variables        │
│  • Custom domain support     • PostgreSQL/Database support │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Part 1: Deploy Frontend to Vercel

### Step 1: Go to Vercel
1. Visit https://vercel.com
2. Click **"Sign up"** or **"Log in"** with GitHub
3. Authorize Vercel to access your GitHub repositories

### Step 2: Import Project
1. Click **"New Project"** (or "Add New" → "Project")
2. Select **"Import Git Repository"**
3. Search for: `hackathin-II-phase-2`
4. Click **"Import"**

### Step 3: Configure Project
1. **Project Name:** `todo-app` (or your preferred name)
2. **Framework:** Should auto-detect as **Next.js** ✓
3. **Root Directory:** Select `frontend`

### Step 4: Environment Variables
1. Click **"Environment Variables"**
2. Add the following variables:

```
NEXT_PUBLIC_API_URL = https://your-backend-url.railway.app
NEXT_PUBLIC_DEBUG = false
```

(We'll set the backend URL after deploying the backend)

### Step 5: Deploy
1. Click **"Deploy"**
2. Wait for deployment to complete (usually 2-3 minutes)
3. You'll see a success message with your URL: `https://todo-app.vercel.app`

### Step 6: Add Custom Domain (Optional)
1. Go to **Settings** → **Domains**
2. Add your custom domain
3. Follow the DNS configuration instructions

---

## 🔧 Part 2: Deploy Backend to Railway

### Step 1: Go to Railway
1. Visit https://railway.app
2. Click **"Start Project"**
3. Choose **"Deploy from GitHub repo"**

### Step 2: Connect GitHub
1. Click **"Connect GitHub Account"**
2. Authorize Railway to access your repositories
3. Select the `hackathin-II-phase-2` repository

### Step 3: Create New Project
1. Click **"Create New Project"**
2. Select your repository
3. Choose the `backend` directory
4. Click **"Deploy"**

### Step 4: Configure Environment Variables
1. Go to **Variables** in the Railway dashboard
2. Add the following:

```
DATABASE_URL = sqlite:///./todo.db
SERVER_HOST = 0.0.0.0
SERVER_PORT = $PORT
ENVIRONMENT = production
DEBUG = false
LOG_LEVEL = INFO
```

### Step 5: Set Start Command
1. Go to **Settings**
2. Set **Start Command** to:
   ```
   uvicorn simple_server:app --host 0.0.0.0 --port $PORT
   ```

### Step 6: Get Backend URL
1. After deployment, go to **Settings** → **Domains**
2. Copy the auto-generated URL (e.g., `https://api-todo-production.railway.app`)
3. This is your backend URL!

### Step 7: Update Frontend Environment
1. Go back to Vercel
2. Go to **Settings** → **Environment Variables**
3. Update `NEXT_PUBLIC_API_URL` with your Railway backend URL
4. Redeploy the frontend

---

## 📊 Deployment Checklist

### Frontend (Vercel)
- [ ] Created Vercel account
- [ ] Imported project from GitHub
- [ ] Configured Next.js root directory (`frontend`)
- [ ] Set environment variables
- [ ] Successfully deployed
- [ ] Verified app loads at https://todo-app.vercel.app
- [ ] API calls working properly
- [ ] Added custom domain (optional)

### Backend (Railway)
- [ ] Created Railway account
- [ ] Connected GitHub repository
- [ ] Deployed from backend directory
- [ ] Configured environment variables
- [ ] Set start command
- [ ] Got deployment URL
- [ ] Updated frontend API URL
- [ ] Tested API endpoints

---

## 🧪 Testing Your Deployment

### Test Frontend
1. Open https://todo-app.vercel.app (or your domain)
2. Create a new task
3. Verify task appears in the list
4. Try filtering and sorting
5. Test delete functionality

### Test Backend API
1. Open https://your-backend-url.railway.app/docs
2. Try the interactive API docs
3. Create a task via API
4. Fetch tasks via API
5. Verify response format

---

## 🔄 How Deployments Work

### Automatic Updates
Every time you push to GitHub:

**Frontend (Vercel):**
```
git push → GitHub → Vercel (auto-detects changes) → Build & Deploy → Live!
```

**Backend (Railway):**
```
git push → GitHub → Railway (auto-detects changes) → Build & Deploy → Live!
```

### Manual Redeploy
If needed, you can trigger manual redeployments:
- **Vercel:** Settings → Deployments → Redeploy
- **Railway:** Settings → Redeploy

---

## 🌍 Share Your Application

Once deployed, share these URLs:

**For Users:**
```
https://todo-app.vercel.app
```

**For Developers:**
```
Frontend: https://todo-app.vercel.app
Backend API: https://api-todo.railway.app
API Docs: https://api-todo.railway.app/docs
GitHub: https://github.com/Zainab-M-Hussain/hackathin-II-phase-2
```

---

## 🐛 Troubleshooting

### Frontend shows "Cannot reach backend"
- **Solution:** Check that `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- **Solution:** Verify backend is running in Railway
- **Solution:** Check CORS is enabled in backend

### Backend responds with 502/503 errors
- **Solution:** Check Railway logs for errors
- **Solution:** Verify environment variables are set
- **Solution:** Check Python dependencies installed

### API returns 500 errors
- **Solution:** Check Railway logs for detailed errors
- **Solution:** Verify database URL is correct
- **Solution:** Ensure all dependencies installed

### Slow performance
- **Solution:** Check Vercel analytics for bottlenecks
- **Solution:** Check Railway CPU/memory usage
- **Solution:** Consider upgrading plan if needed

---

## 💰 Cost Analysis

| Service | Plan | Cost | Features |
|---------|------|------|----------|
| **Vercel** | Pro | Free | 100GB bandwidth/month, unlimited deployments |
| **Railway** | Free | Free | 500 compute hours/month, shared resources |
| **Custom Domain** | Optional | ~$10-15/year | Point your own domain |

**Total Monthly Cost:** $0-20 (depending on custom domain)

---

## 🔐 Security Considerations

### Secrets Management
Never commit secrets! Use environment variables:
- ✅ Database URLs
- ✅ API keys
- ✅ Configuration values

Both Vercel and Railway provide secure secret management.

### CORS Configuration
Backend CORS is configured to allow:
- localhost:3000
- localhost:3001
- vercel domains
- Custom domains

Update as needed in `simple_server.py`

---

## 📈 Monitoring & Analytics

### Vercel Dashboard
- View real-time analytics
- Monitor bandwidth usage
- Check build times
- View error logs

### Railway Dashboard
- Monitor CPU & memory usage
- View deployment logs
- Track API response times
- Monitor uptime

---

## 🚀 Advanced: Custom Domain

### Using Vercel's Domain
1. Go to Vercel Settings → Domains
2. Click "Add Domain"
3. Enter your domain (e.g., `todo.yourdomain.com`)
4. Follow DNS setup instructions
5. DNS propagation takes 5-48 hours

### Using Railway's Domain
1. Go to Railway Settings → Domains
2. Add custom domain
3. Configure DNS records
4. Verify ownership

---

## 📚 Useful Links

- **Vercel Docs:** https://vercel.com/docs
- **Railway Docs:** https://docs.railway.app
- **Next.js Deployment:** https://nextjs.org/docs/deployment
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/

---

## ✅ Next Steps

1. **Create accounts** (Vercel & Railway)
2. **Deploy frontend** to Vercel
3. **Deploy backend** to Railway
4. **Update environment variables**
5. **Test thoroughly**
6. **Share with friends!** 🎉

---

## 📞 Support

If you encounter issues:
1. Check Vercel/Railway logs
2. Review deployment guide steps
3. Verify environment variables
4. Test locally first
5. Check GitHub issues

---

**Your application will soon be live for everyone to use!** 🌍✨

Deploy date: [Your deployment date]
Live URL: [Your Vercel URL]
Backend URL: [Your Railway URL]
