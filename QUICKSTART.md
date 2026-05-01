# LinkShield - React Website - Quick Start Guide

## Overview

You've successfully converted LinkShield from a Streamlit app to a modern React + Flask full-stack web application! 🚀

## Project Structure

```
LinkShield/
├── frontend/              # React web application (Port 3000)
│   ├── public/
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Dashboard, Analyzer, Training, EDA pages
│   │   ├── services/      # API client
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
│
├── backend/               # Flask REST API (Port 5000)
│   ├── app.py            # Main Flask application
│   └── requirements.txt
│
├── fake_link_detector/    # ML detector logic (unchanged)
│   ├── detector.py
│   └── __init__.py
│
├── setup.bat             # Windows setup script
├── setup.sh              # Mac/Linux setup script
└── README_NEW.md         # Detailed documentation
```

## Feature Parity

The React website maintains all features from the Streamlit app:

✅ **URL Analysis** - Real-time fake link detection
✅ **Dashboard** - Statistics and analytics
✅ **Model Training** - Train RF, LR, SVM models
✅ **Exploratory Data Analysis** - Feature importance & insights
✅ **K-Fold Validation** - Performance evaluation
✅ **Live Inference** - Test URLs with trained model
✅ **Dataset Upload** - CSV/TSV file support

## Quick Start (Windows)

### Automated Setup (Recommended)

```bash
cd c:\Users\srija\Documents\My Projects\LinkShield
setup.bat
```

This will:
1. Create Python virtual environment
2. Install backend dependencies
3. Install frontend Node packages
4. Create .env file

### Manual Setup

**Terminal 1 - Backend:**
```bash
cd backend
.\.venv\Scripts\Activate.ps1
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## Quick Start (Mac/Linux)

```bash
chmod +x setup.sh
./setup.sh
```

Then open two terminals:

**Terminal 1:**
```bash
cd backend
source .venv/bin/activate
python app.py
```

**Terminal 2:**
```bash
cd frontend
npm start
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **Health Check**: http://localhost:5000/api/health

## Pages/Features

### 1. Dashboard
- Total URLs analyzed count
- Safe vs Suspicious breakdown
- Model accuracy metrics
- Weekly analytics chart

### 2. URL Analyzer
- Paste any URL
- Get instant risk score (0-100%)
- See detection reasons
- View extracted URL features

### 3. Model Training
- Select ML model (Random Forest, Logistic Regression, SVM)
- Configure K-Fold validation (2-10 folds)
- Upload custom dataset (CSV/TSV)
- View training results with metrics

### 4. Analytics (EDA)
- Feature importance visualization
- Class distribution chart
- URL length vs malicious probability scatter plot

## API Endpoints

### Health Check
```
GET /api/health
```

### Analyze URL
```
POST /api/analyze
Content-Type: application/json

{
  "url": "https://example.com"
}
```

### Dashboard Stats
```
GET /api/dashboard
```

### EDA Data
```
GET /api/eda
```

### Train Model
```
POST /api/train
Content-Type: multipart/form-data

- model: "rf" | "lr" | "svm"
- k_fold: 5
- test_size: 0.2
- file: (optional CSV/TSV)
```

## Technology Differences

| Feature | Streamlit | React |
|---------|-----------|-------|
| Frontend | Python Streamlit | React 18 |
| Backend | Streamlit cached functions | Flask REST API |
| Styling | Streamlit default | Custom CSS with dark theme |
| Charts | Matplotlib | Recharts (interactive) |
| Deployment | Streamlit Cloud | Docker / Heroku / AWS |
| Performance | Single-threaded | Multi-threaded API |
| Scalability | Limited | Highly scalable |

## Customization

### Change API URL
Edit `frontend/.env`:
```
REACT_APP_API_URL=http://your-backend:5000/api
```

### Change Theme
Edit CSS variables in `frontend/src/index.css`:
```css
:root {
  --bg-primary: #0f172a;
  --accent: #3b82f6;
  /* ... more vars ... */
}
```

### Add More Models
1. Add model to `get_model_registry()` in `detector.py`
2. Update mapping in Flask `train` endpoint
3. Update dropdown in React component

## Troubleshooting

### Port 5000 Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F
```

### CORS Errors
Ensure Flask has CORS enabled:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Model Not Initializing
Check Flask logs for errors. Ensure all detector functions are present.

### Frontend won't connect to API
1. Check backend is running on port 5000
2. Verify `REACT_APP_API_URL` in `.env`
3. Check browser DevTools Network tab for 404/CORS errors

## Production Deployment

See `DEPLOYMENT.md` for:
- Docker containerization
- Docker Compose setup
- AWS/Heroku deployment
- Nginx configuration
- Environment variables

## Next Steps

1. ✅ Run setup script
2. ✅ Start backend server
3. ✅ Start frontend dev server
4. ✅ Visit http://localhost:3000
5. ✅ Test URL analyzer
6. ✅ Train a model
7. 🔜 Deploy to production

## Key Improvements Over Streamlit

- **Responsive Design** - Works on mobile, tablet, desktop
- **Better UX** - No page refreshes, faster interactions
- **Scalability** - Handle multiple concurrent users
- **API-driven** - Easy to integrate with other apps
- **Version Control** - Separate frontend & backend repos
- **Performance** - Client-side rendering, fast API responses
- **Customization** - Complete control over UI/UX

## Support

For issues or questions:
1. Check browser console for errors
2. Check Flask server logs
3. Verify all files are in correct locations
4. Ensure Python & Node versions are compatible

---

**Happy analyzing! 🛡️**
