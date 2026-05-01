# Quick Deployment Checklist - Vercel & Railway

## 🎯 TL;DR - 5 Steps to Deploy

### Step 1: Push to GitHub
```bash
cd c:\Users\srija\Documents\My Projects\LinkShield
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/LinkShield.git
git push -u origin main
```

### Step 2: Deploy Backend (Railway)
- Go to https://railway.app → Sign in with GitHub
- Click **New Project** → **Deploy from GitHub** → Select LinkShield
- In settings: Root Directory = `backend`
- Railway auto-deploys, then copy the URL (e.g., `https://linkshield-backend-production.up.railway.app`)

### Step 3: Set Railway Environment
In Railway dashboard → **Variables**:
```
FLASK_ENV=production
ALLOWED_ORIGINS=https://linkshield.vercel.app,http://localhost:3000
```

### Step 4: Deploy Frontend (Vercel)
- Go to https://vercel.com → Click **Import Project**
- Select LinkShield repo → Root: `frontend`
- Environment Variables:
  ```
  REACT_APP_API_URL=https://linkshield-backend-production.up.railway.app/api
  ```
- Deploy!

### Step 5: Test
- Open your Vercel URL
- Try analyzing a URL
- Check F12 console for errors

---

## 📍 Your Deployed URLs

```
🌐 Frontend: https://linkshield.vercel.app
🔧 Backend: https://linkshield-backend-production.up.railway.app
📡 API: https://linkshield-backend-production.up.railway.app/api
```

---

## ✅ Deployment Checklist

- [ ] GitHub repo created
- [ ] Code pushed to main branch
- [ ] Railway backend deployed
- [ ] Backend URL copied
- [ ] Railway environment variables set
- [ ] Vercel frontend deployed
- [ ] Frontend environment variables set
- [ ] Frontend loads successfully
- [ ] URL Analyzer works
- [ ] Model Training works
- [ ] No CORS errors in console

---

## 🔄 How to Redeploy After Changes

```bash
# Make changes to code
# ...

# Push to GitHub
git add .
git commit -m "Your changes"
git push origin main

# Both Railway and Vercel redeploy automatically! ✨
```

---

## 🆘 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| CORS errors in console | Check `ALLOWED_ORIGINS` in Railway Variables |
| Frontend shows "Cannot connect" | Verify `REACT_APP_API_URL` in Vercel |
| Models not loading | Check Railway logs for scikit-learn import errors |
| URL Analyzer 404 | Restart Railway deployment manually |
| Long load times | Railway free tier is slower; upgrade if needed |

---

## 📊 Monitoring

**Railway Logs:**
- Dashboard → Select project → **Logs** tab

**Vercel Logs:**
- Dashboard → Select project → **Deployments** → Click deployment → **Logs**

**Test API Health:**
```
curl https://linkshield-backend-production.up.railway.app/api/health
```

---

## 💰 Cost

- **Vercel**: Free (up to 100GB/month)
- **Railway**: Free tier ($5/month credit)
- **Total**: ~$0 for hobby usage

Upgrade only if you need more power!

---

## 📚 More Help

- [VERCEL_RAILWAY_GUIDE.md](VERCEL_RAILWAY_GUIDE.md) - Detailed guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Other deployment options
- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs

---

**You're all set! Deploy now and share your app! 🚀**
