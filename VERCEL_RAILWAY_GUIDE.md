# Deploy LinkShield to Vercel & Railway

## Part 1: Backend Deployment (Railway)

### Prerequisites
- GitHub account with LinkShield repo pushed
- Railway account (https://railway.app) - sign up free

### Step 1: Push Code to GitHub

```bash
cd c:\Users\srija\Documents\My Projects\LinkShield

# Initialize git if not done
git init
git add .
git commit -m "Initial LinkShield commit"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/LinkShield.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Backend to Railway

1. Go to https://railway.app
2. Click **New Project** → **Deploy from GitHub**
3. Select your **LinkShield** repository
4. Railway will auto-detect it's a Python app
5. In the deployment settings:
   - **Root Directory**: `backend`
   - **Start Command**: `python app.py`

### Step 3: Configure Railway Environment

1. In Railway dashboard, go to **Variables**
2. Add these environment variables:
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

3. Click **Deploy** - wait ~5 minutes

### Step 4: Get Backend URL

Once deployed, you'll see a URL like:
```
https://linkshield-backend-production.up.railway.app
```

**Copy this URL - you'll need it for frontend!**

---

## Part 2: Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (https://vercel.com) - free with GitHub login
- Backend URL from Railway (from Part 1)

### Step 1: Deploy to Vercel

1. Go to https://vercel.com/new
2. Click **Import GitHub Repository**
3. Select **LinkShield** repo
4. In project settings:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Next.js (select React if asked)
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Start Command**: `npm start`

### Step 2: Set Environment Variables

Before deploying, add environment variable:

In Vercel dashboard:
1. Go to **Settings** → **Environment Variables**
2. Add:
   ```
   REACT_APP_API_URL=https://linkshield-backend-production.up.railway.app/api
   ```
   (Replace with your actual Railway URL)

3. Click **Deploy**

### Step 3: Verify Frontend

After 2-3 minutes, you'll get a Vercel URL like:
```
https://linkshield.vercel.app
```

---

## Step 3: Fix CORS on Railway Backend

Your frontend and backend now have different origins. Update Flask:

1. In `backend/app.py`, change CORS to allow Vercel:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://linkshield.vercel.app",  # Your Vercel URL
            "http://localhost:3000",           # Local dev
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

2. Push changes:
```bash
git add backend/app.py
git commit -m "Update CORS for Vercel domain"
git push
```

3. Railway will auto-redeploy

---

## Step 4: Test Everything

1. Open your Vercel frontend URL
2. Try analyzing a URL - should work!
3. Check browser console (F12) for any CORS errors

---

## Complete Deployment Checklist

- [ ] GitHub repo created and pushed
- [ ] Railway account created
- [ ] Backend deployed to Railway
- [ ] Backend URL copied
- [ ] Vercel account created
- [ ] Frontend deployed to Vercel
- [ ] Environment variable set in Vercel
- [ ] CORS updated in backend/app.py
- [ ] Backend redeployed after CORS change
- [ ] Frontend URL working and connecting to backend

---

## URLs After Deployment

**Frontend (Vercel):**
```
https://linkshield.vercel.app
```

**Backend API (Railway):**
```
https://linkshield-backend-production.up.railway.app/api
```

---

## Troubleshooting

### Frontend shows "API not connecting"
1. Check `REACT_APP_API_URL` in Vercel settings
2. Verify Railway backend is running
3. Check browser Network tab for 404/CORS errors
4. Verify CORS is updated in backend/app.py

### Railway deployment fails
1. Check **Deployment** logs in Railway dashboard
2. Ensure Python dependencies are in `backend/requirements.txt`
3. Verify `backend/app.py` exists and starts correctly

### Models not loading
1. Railway might need to reinstall: `pip install -r requirements.txt`
2. Check Railway logs for import errors
3. Verify scikit-learn/pandas installed

### Custom domain setup

**For Vercel:**
1. Go to **Settings** → **Domains**
2. Add your domain (e.g., linkshield.com)
3. Update DNS records per Vercel instructions

**For Railway:**
1. Go to **Settings** → **Networking**
2. Add custom domain
3. Update DNS to point to Railway

---

## Redeploy After Changes

**After pushing new code to GitHub:**
```bash
git add .
git commit -m "Your message"
git push origin main
```

- **Railway** redeploys automatically
- **Vercel** redeploys automatically

---

## Monitoring

**Railway:**
- Go to **Monitoring** tab
- View logs, CPU, memory usage

**Vercel:**
- Go to **Analytics** tab
- View request logs, performance

---

## Cost Estimates (May 2026)

- **Vercel**: Free tier (up to 100GB/month bandwidth)
- **Railway**: Free tier ($5/month credits, then pay-per-use)
- **Total**: ~$0-5/month for hobby usage

---

## Next Steps

1. Follow steps above
2. Test your deployed app
3. Share the Vercel URL with others!
4. Monitor logs if issues arise

Questions? Check Railway/Vercel docs or let me know!
