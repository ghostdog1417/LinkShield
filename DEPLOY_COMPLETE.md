# 🚀 Complete Guide: Deploying LinkShield to Vercel & Railway

## Overview

This guide walks you through deploying LinkShield with:

- **Frontend**: Vercel (fast, global CDN)
- **Backend**: Railway (simple Python hosting)

**Total time**: ~20-30 minutes  
**Cost**: Free (with optional paid upgrades)

---

## Pre-Deployment Setup

### 1. Ensure Code is on GitHub

```bash
cd c:\Users\srija\Documents\My Projects\LinkShield

# Initialize git
git init
git add .
git commit -m "Initial LinkShield commit"

# Add your GitHub repo (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/LinkShield.git
git branch -M main
git push -u origin main
```

✅ **Result**: Code pushed to GitHub main branch

### 2. Verify Local Setup Works

```bash
# Terminal 1
cd backend && python app.py

# Terminal 2
cd frontend && npm start
```

Visit http://localhost:3000 and test URL analyzer works.

✅ **Result**: App works locally

---

## Phase 1: Deploy Backend to Railway

### Step 1: Create Railway Account

1. Go to https://railway.app
2. Click **Start Now**
3. Sign in with GitHub (fastest)
4. Grant Railway access to GitHub

### Step 2: Create New Project

1. Click **New Project**
2. Select **Deploy from GitHub**
3. Select your **LinkShield** repository
4. Railway auto-detects Python app

### Step 3: Configure Backend Service

Railway should auto-detect these, but verify:

- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

### Step 4: Set Environment Variables

1. In Railway dashboard, click your project
2. Click the **backend** service
3. Go to **Variables** tab
4. Add:
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

5. **Do NOT set ALLOWED_ORIGINS yet** (you'll need Vercel URL first)

### Step 5: Deploy

1. Click **Deploy** button
2. Wait for build (takes 2-5 minutes)
3. Watch logs for any errors
4. Once deployed, you'll see a public URL like:
   ```
   https://linkshield-backend-production.up.railway.app
   ```

**Copy this URL!** You'll need it for Vercel.

✅ **Result**: Backend running on Railway with a public URL

---

## Phase 2: Deploy Frontend to Vercel

### Step 1: Create Vercel Account

1. Go to https://vercel.com
2. Click **Sign Up**
3. Use GitHub login (fastest)
4. Grant Vercel access to GitHub

### Step 2: Create New Project

1. Click **New Project** or **Add New** → **Project**
2. Click **Import Git Repository**
3. Select **LinkShield**
4. Click **Import**

### Step 3: Configure Frontend

In the configuration screen:

**Framework Preset**: React  
**Root Directory**: `frontend`  
**Build Command**: `npm run build`  
**Output Directory**: `build`

### Step 4: Add Environment Variable

**IMPORTANT**: Before deploying, add your Railway backend URL!

1. Click **Environment Variables**
2. Add:
   ```
   Name: REACT_APP_API_URL
   Value: https://linkshield-backend-production.up.railway.app/api
   ```
   (Use your actual Railway URL from Phase 1)

3. Click **Add**

### Step 5: Deploy

1. Click **Deploy**
2. Wait for build (takes 2-3 minutes)
3. You'll get a Vercel URL like:
   ```
   https://linkshield-xyz123.vercel.app
   ```

**Copy this URL!** You need it to finish Railway setup.

✅ **Result**: Frontend running on Vercel

---

## Phase 3: Fix CORS (Critical!)

Your frontend and backend now have different domains, so you need to allow Vercel's domain on Railway.

### Step 1: Update Railway Variables

1. Go back to Railway dashboard
2. Select your project and **backend** service
3. Go to **Variables** tab
4. Add new variable:
   ```
   Name: ALLOWED_ORIGINS
   Value: https://linkshield-xyz123.vercel.app
   ```
   (Use your actual Vercel URL)

5. If you also want local development to work:
   ```
   ALLOWED_ORIGINS=https://linkshield-xyz123.vercel.app,http://localhost:3000
   ```

### Step 2: Redeploy Railway

1. Go to **Deployments** tab
2. Click the most recent deployment
3. Click **Redeploy** button
4. Wait for redeployment (1-2 minutes)

✅ **Result**: CORS configured correctly

---

## Phase 4: Test Your Deployment

### Test 1: Check Backend Health

```bash
# In any terminal/browser, visit:
https://linkshield-backend-production.up.railway.app/api/health
```

Should return:
```json
{
  "status": "healthy",
  "message": "LinkShield Backend is running"
}
```

### Test 2: Test Frontend

1. Go to your Vercel URL: https://linkshield-xyz123.vercel.app
2. Navigate to **URL Analyzer**
3. Paste a URL and click **Analyze**
4. Should see results!

### Test 3: Check for Errors

1. Open browser **DevTools** (F12)
2. Go to **Console** tab
3. Should be no red errors
4. Go to **Network** tab
5. Should see successful requests to Railway backend

✅ **Result**: App fully deployed and working!

---

## Your Live URLs

Once deployed, share these:

```
🌐 Frontend:  https://linkshield-xyz123.vercel.app
🔧 API Base:  https://linkshield-backend-production.up.railway.app/api
📊 Health:    https://linkshield-backend-production.up.railway.app/api/health
```

---

## How to Update Your App

Whenever you make changes:

```bash
# Make changes to code
# ... edit files ...

# Push to GitHub
git add .
git commit -m "Your changes"
git push origin main

# Both Vercel and Railway will automatically redeploy! ✨
```

---

## Troubleshooting

### Issue: CORS errors in browser console

**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Fix**:
1. Go to Railway dashboard
2. Check ALLOWED_ORIGINS includes your Vercel URL
3. Make sure you set it correctly (no trailing slashes)
4. Click Redeploy on Railway
5. Hard refresh frontend: `Ctrl+Shift+R`

### Issue: Frontend shows "Cannot connect to API"

**Fix**:
1. Verify `REACT_APP_API_URL` in Vercel settings (Settings → Environment Variables)
2. Check Railway backend is actually running (visit health endpoint)
3. Make sure you're using the correct Railway URL
4. Check for typos in the URL

### Issue: 404 errors when navigating

**Fix** (React Router on Vercel):
1. Go to Vercel project settings
2. Go to **Build & Deployment** → **Build Command**
3. Ensure it's: `npm run build`
4. Redeploy

### Issue: Models not loading / scikit-learn errors

**Fix**:
1. Check Railway logs (Deployments → Latest → Logs)
2. Verify `requirements.txt` is in backend folder
3. Check all dependencies listed:
   - flask
   - flask-cors
   - scikit-learn
   - pandas
   - numpy
4. If still failing, manually trigger Railway redeploy

### Issue: Railway backend is very slow

**Reason**: Free tier is shared resources  
**Options**:
1. Upgrade Railway plan ($5/month)
2. Switch to more powerful backend (AWS, Heroku)
3. Add caching to speed up responses

---

## Performance Optimization

### Vercel (Frontend)
- Already optimized with global CDN
- Check Analytics to see performance
- Enable Edge Functions for faster routing (paid feature)

### Railway (Backend)
- Free tier shares resources (slower)
- For serious projects, upgrade to paid plan
- Consider caching responses
- Reduce model training requests

---

## Monitoring

### Check Railway Status
1. Go to Railroad dashboard
2. Select project
3. View **Logs** tab (real-time)
4. Check **Metrics** for CPU/Memory usage

### Check Vercel Status
1. Go to Vercel dashboard
2. Select project
3. Click **Deployments** for deployment history
4. Click **Analytics** for performance metrics

---

## Custom Domain Setup

### Add to Vercel
1. Project Settings → **Domains**
2. Add your domain (e.g., `linkshield.com`)
3. Follow DNS configuration steps

### Add to Railway
1. Project Settings → **Networking**
2. Add custom domain
3. Follow DNS configuration steps

---

## Next Steps

**Congratulations!** Your app is live! 🎉

Now consider:

1. **Share it**: Send your Vercel URL to friends/family
2. **Monitor**: Check logs regularly for issues
3. **Improve**: Add features, fix bugs
4. **Scale**: If popular, upgrade Railway plan
5. **Add DB**: Store user history with PostgreSQL
6. **Add Auth**: User accounts with GitHub login

---

## Need More Help?

- **Quick Reference**: See [DEPLOY_QUICK.md](DEPLOY_QUICK.md)
- **Deployment Tips**: See [DEPLOYMENT_HELP.md](DEPLOYMENT_HELP.md)
- **Other Options**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs

---

**You're done! Your LinkShield app is now live on the internet!** 🚀

If you have questions, check the troubleshooting section or ask for help.
