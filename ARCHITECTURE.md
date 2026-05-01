# LinkShield Website Architecture

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT SIDE                         │
│  React 18 + React Router + Recharts + Lucide Icons         │
│  └─ Modern, responsive UI with dark theme                  │
└─────────────────────────────────┬───────────────────────────┘
                                  │ HTTP/REST
                                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      FLASK REST API                          │
│  Flask + Flask-CORS                                          │
│  └─ 5 Main Endpoints (health, analyze, dashboard, eda,     │
│     train)                                                   │
└─────────────────────────────────┬───────────────────────────┘
                                  │ Python Functions
                                  ▼
┌─────────────────────────────────────────────────────────────┐
│               ML/DETECTOR LOGIC (Unchanged)                  │
│  scikit-learn Pipeline                                       │
│  └─ URL Feature Extraction                                  │
│  └─ Model Training & Evaluation                             │
│  └─ Prediction & Risk Scoring                               │
└─────────────────────────────────────────────────────────────┘
```

## File Tree

```
LinkShield/
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navigation.js      [Sidebar navigation]
│   │   │   └── Navigation.css
│   │   ├── pages/
│   │   │   ├── Dashboard.js       [Stats & charts]
│   │   │   ├── Dashboard.css
│   │   │   ├── UrlAnalyzer.js     [URL detection form]
│   │   │   ├── UrlAnalyzer.css
│   │   │   ├── ModelTraining.js   [ML model training UI]
│   │   │   ├── ModelTraining.css
│   │   │   ├── EDA.js             [Data visualization]
│   │   │   └── EDA.css
│   │   ├── services/
│   │   │   └── apiClient.js       [Axios HTTP client]
│   │   ├── App.js                 [Main router]
│   │   ├── App.css
│   │   ├── index.js               [Entry point]
│   │   └── index.css              [Global styles]
│   └── package.json
│
├── backend/
│   ├── app.py                     [Flask REST API]
│   └── requirements.txt
│
├── fake_link_detector/
│   ├── detector.py                [ML logic - UNCHANGED]
│   └── __init__.py
│
├── .env.example                   [Environment template]
├── .gitignore                     [Git ignore rules]
├── setup.bat                      [Windows setup]
├── setup.sh                       [Unix setup]
├── QUICKSTART.md                  [Quick start guide]
├── README_NEW.md                  [Full documentation]
├── DEPLOYMENT.md                  [Production guide]
└── package.json                   [Root scripts]
```

## Component Hierarchy

```
App (React Router)
├── Navigation (Sidebar)
│   ├── Logo & Brand
│   ├── Nav Links (4 pages)
│   └── Footer Info
│
└── Routes (Main Content)
    ├── Dashboard
    │   ├── Stats Cards (4)
    │   ├── Charts Grid
    │   └── Responsive Layout
    │
    ├── UrlAnalyzer
    │   ├── Search Form
    │   ├── Result Display
    │   ├── Features Grid
    │   └── Risk Indicator
    │
    ├── ModelTraining
    │   ├── Configuration Panel
    │   │   ├── Model Selector
    │   │   ├── K-Fold Input
    │   │   ├── Test Size Input
    │   │   └── File Upload
    │   ├── Results Panel
    │   └── Metrics Grid
    │
    └── EDA
        ├── Feature Importance Chart
        ├── Class Distribution
        └── Scatter Plot
```

## API Flows

### URL Analysis Flow
```
Frontend Form
    ↓ (POST /api/analyze)
Flask Route
    ↓ analyze_url()
Detector
    ↓ Extract Features + Predict
Result (JSON)
    ↓
Frontend Display
```

### Model Training Flow
```
Frontend Upload Form
    ↓ (POST /api/train, multipart)
Flask Route
    ↓ Load Dataset / Use Demo
    ↓ train_pipeline()
Detector
    ↓ Feature Selection
    ↓ Model Training
    ↓ K-Fold Validation
Training Results
    ↓
Frontend Metrics Display
```

## Styling System

**CSS Variables (Dark Theme)**
```css
--bg-primary: #0f172a        /* Deep blue-black */
--bg-secondary: #1e293b      /* Dark slate */
--bg-tertiary: #334155       /* Medium slate */
--text-primary: #e2e8f0      /* Light text */
--text-secondary: #cbd5e1    /* Muted text */
--border: #475569            /* Border color */
--success: #10b981           /* Green */
--danger: #ef4444            /* Red */
--accent: #3b82f6            /* Blue */
```

## Features Implemented

### Frontend Features
- ✅ Responsive sidebar navigation
- ✅ Real-time URL analysis
- ✅ Interactive data visualizations (Recharts)
- ✅ Model training interface
- ✅ File upload support
- ✅ EDA charts & insights
- ✅ Dark theme throughout
- ✅ Mobile-responsive design

### Backend Features
- ✅ RESTful API with CORS
- ✅ URL analysis endpoint
- ✅ Dashboard statistics
- ✅ Model training endpoint
- ✅ EDA data endpoint
- ✅ Health check endpoint
- ✅ CSV/TSV file handling
- ✅ Error handling & validation

### ML Features (Preserved)
- ✅ 12 URL features extracted
- ✅ 3 ML models available (RF, LR, SVM)
- ✅ K-Fold cross-validation
- ✅ Feature selection
- ✅ Performance metrics
- ✅ Demo dataset generation
- ✅ Real-time predictions

## Performance Considerations

| Aspect | Optimization |
|--------|--------------|
| API Response | < 500ms for URL analysis |
| Bundle Size | ~150KB gzipped (React + deps) |
| Database | None (stateless API) |
| Caching | Browser cache + API headers |
| Scalability | Horizontal (stateless backend) |

## Key Differences from Streamlit

| Aspect | Streamlit | React |
|--------|-----------|-------|
| **Architecture** | All-in-one Python app | Frontend + Backend separation |
| **UI Updates** | Full page reload | Partial DOM updates |
| **Hosting** | Streamlit Cloud / Custom | Anywhere (Docker, AWS, etc.) |
| **Customization** | Limited CSS | Full control |
| **Performance** | Slower on interactions | Faster, more responsive |
| **Team Structure** | Single developer | Frontend + Backend devs |
| **Deployment** | Push to Streamlit Cloud | CI/CD pipeline |
| **Monitoring** | Limited | Full observability |

## Development Workflow

```
1. Start Backend:
   cd backend
   .venv\Scripts\Activate.ps1
   python app.py

2. Start Frontend:
   cd frontend
   npm start

3. Develop:
   - Edit React components in real-time (HMR)
   - Edit Flask routes and restart
   - Use React DevTools & Network tab

4. Test:
   - Test endpoints in Postman/Thunder Client
   - Check browser console for errors
   - Use Flask debug mode

5. Deploy:
   - Build React: npm run build
   - Docker both services
   - Push to registry
```

## Future Enhancements

- Database integration (user history, saved analyses)
- Authentication & user accounts
- Advanced analytics dashboard
- API key management
- Webhook notifications
- Batch URL analysis
- Custom model uploads
- Real-time model retraining
- Mobile app (React Native)
- GraphQL API option

---

**This architecture provides a scalable, modern web application while maintaining all the ML functionality from the original Streamlit app.**
