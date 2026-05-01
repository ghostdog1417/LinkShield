# Deployment Resources

## Video Tutorials

- **Railway Docs**: https://docs.railway.app/getting-started
- **Vercel Docs**: https://vercel.com/docs/getting-started
- **Railway GitHub Integration**: https://docs.railway.app/deploy/github

## Step-by-Step Screenshots

### Railway Backend Deployment

1. **New Project**
   - Go to railway.app
   - Click "New Project"
   - Select "Deploy from GitHub"

2. **Select Repository**
   - Connect GitHub
   - Select LinkShield repo
   - Authorize access

3. **Configure Service**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

4. **Set Variables**
   - FLASK_ENV: `production`
   - ALLOWED_ORIGINS: `https://yourfrontend.vercel.app`

5. **Deploy**
   - Click "Deploy"
   - Wait 3-5 minutes
   - Copy the public URL

### Vercel Frontend Deployment

1. **New Project**
   - Go to vercel.com
   - Click "New Project"
   - Select "Import Git Repository"

2. **Select Repository**
   - Sign in with GitHub
   - Select LinkShield repo

3. **Configure Project**
   - Root Directory: `frontend`
   - Framework: React
   - Build: `npm run build`

4. **Set Environment Variables**
   - REACT_APP_API_URL: `https://your-railway-backend.up.railway.app/api`

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Get Vercel URL

## Environment Variables Reference

### Railway Backend (.env or Variables tab)
```
FLASK_ENV=production
FLASK_DEBUG=False
ALLOWED_ORIGINS=https://linkshield.vercel.app,http://localhost:3000
```

### Vercel Frontend (Settings → Environment Variables)
```
REACT_APP_API_URL=https://linkshield-backend-production.up.railway.app/api
```

## Monitoring & Logs

### View Railway Logs
1. Go to Railway Dashboard
2. Select LinkShield project
3. Click project service
4. View **Logs** tab (live streaming)
5. Check for errors or deployment issues

### View Vercel Logs
1. Go to Vercel Dashboard
2. Select LinkShield project
3. Click **Deployments**
4. Click the deployment you want to check
5. Click **Logs** to view build/runtime logs

## Troubleshooting

### Backend won't start on Railway
- Check logs for Python errors
- Verify requirements.txt has all dependencies
- Ensure app.py has correct Flask syntax

### Frontend can't connect to API
- Double-check REACT_APP_API_URL in Vercel
- Make sure Railway backend is actually running
- Check ALLOWED_ORIGINS includes Vercel URL
- View browser console (F12) for exact error

### CORS Error (most common)
```
Access to XMLHttpRequest blocked by CORS policy
```
**Solution:**
1. Go to Railway dashboard
2. Add ALLOWED_ORIGINS variable with your Vercel URL
3. Redeploy Railway
4. Hard refresh frontend (Ctrl+Shift+R)

### scikit-learn import error on Railway
- Railway auto-installs from requirements.txt
- If error persists, manually restart deployment
- Check requirements.txt has scikit-learn listed

## Custom Domain Setup

### Add domain to Vercel
1. Go to Project Settings
2. Click "Domains"
3. Add your domain
4. Update DNS per Vercel instructions

### Add domain to Railway
1. Go to Project Settings
2. Click "Networking"
3. Add custom domain
4. Update DNS per Railway instructions

## Automatic Redeploys

Both platforms redeploy automatically when you push to `main` branch:

```bash
git add .
git commit -m "Your changes"
git push origin main

# Railway and Vercel will automatically redeploy!
```

Set up GitHub webhook in deployment settings if not automatic.

## Performance Tips

1. **Enable Vercel Edge Functions** for faster frontend
2. **Upgrade Railway plan** if backend is slow
3. **Add caching** to API responses
4. **Monitor bandwidth** usage

## Cost Monitoring

- **Vercel**: Check Analytics dashboard for bandwidth
- **Railway**: Check Billing for usage

Both offer generous free tiers for hobby projects.

## Next: Add Database

Once your site is live, consider adding:
- PostgreSQL (Railway offers this)
- User history tracking
- Saved analyses
- User authentication

## Useful Commands

```bash
# Check Railway status
railway status

# View Railway logs locally
railway logs

# Redeploy manually
railway up

# Check environment on Railway
railway env

# Login to Railway CLI
railway login

# Deploy specific service
railway deploy --service=backend
```

Install Railway CLI:
```bash
npm install -g @railway/cli
```

---

**Need more help? Check the full guides:**
- [VERCEL_RAILWAY_GUIDE.md](VERCEL_RAILWAY_GUIDE.md)
- [DEPLOY_QUICK.md](DEPLOY_QUICK.md)
