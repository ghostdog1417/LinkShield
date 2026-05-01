# LinkShield - Fake Link Detection Platform

A modern React-based web application for detecting malicious and fake links using machine learning.

## Project Structure

```
LinkShield/
├── frontend/              # React web application
│   ├── public/
│   ├── src/
│   │   ├── components/    # Reusable React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API client
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
│
├── backend/               # Flask API server
│   ├── app.py            # Main Flask application
│   └── requirements.txt
│
└── fake_link_detector/    # ML detector logic
    ├── detector.py
    └── __init__.py
```

## Features

- **URL Analysis**: Real-time detection of malicious links
- **Dashboard**: Statistics and trends visualization
- **Model Training**: Train and evaluate different ML models
- **Exploratory Data Analysis**: Feature importance and data insights
- **Multiple Models**: Random Forest, Logistic Regression, SVM support

## Tech Stack

### Frontend
- React 18
- Recharts (data visualization)
- Lucide Icons
- Axios (HTTP client)
- CSS with CSS Variables

### Backend
- Flask
- Flask-CORS
- scikit-learn
- pandas

## Installation & Setup

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install Node dependencies
npm install

# Create .env file
echo REACT_APP_API_URL=http://localhost:5000/api > .env
```

## Running the Application

### Start Backend Server

```bash
cd backend
.\.venv\Scripts\Activate.ps1  # On Windows
python app.py
```

The API will be available at `http://localhost:5000`

### Start Frontend Development Server

```bash
cd frontend
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Health Check
- `GET /api/health` - Check server status

### URL Analysis
- `POST /api/analyze` - Analyze a URL
  ```json
  {
    "url": "https://example.com"
  }
  ```

### Dashboard
- `GET /api/dashboard` - Get dashboard statistics

### Analytics
- `GET /api/eda` - Get EDA data

### Model Training
- `POST /api/train` - Train a model
  ```json
  {
    "model": "rf|lr|svm",
    "k_fold": 5,
    "test_size": 0.2,
    "file": <optional CSV file>
  }
  ```

## Building for Production

### Frontend Build

```bash
cd frontend
npm run build
```

Creates optimized build in `frontend/build/`

### Backend Deployment

Update `app.py` for production:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## Demo

The application includes demo data generation:
- Synthetic phishing dataset for demonstration
- Pre-trained model for immediate use
- Sample analytics and statistics

## Usage Examples

### Analyzing a URL

1. Navigate to **URL Analyzer** tab
2. Enter a URL to test
3. View risk score and detection reasons

### Training a Model

1. Go to **Model Training** tab
2. Select model type (RF, LR, SVM)
3. Configure K-Fold validation and test size
4. Optionally upload CSV dataset
5. Click **Train Model** to see results

### Viewing Analytics

1. Check **Dashboard** for overall statistics
2. Explore **Analytics** tab for feature importance
3. Monitor model performance metrics

## Notes

- This is an academic project for learning ML and web development
- Not a production-grade security tool
- Use only with legitimate datasets and URLs for testing

## License

Educational use
