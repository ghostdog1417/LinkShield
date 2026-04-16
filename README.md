# LinkShield (CA-2 Exhibition Project)

LinkShield is an ANN & ML course project that demonstrates a complete fake-link detection pipeline in a Streamlit dashboard.

## CA-2 pipeline coverage

The dashboard includes dedicated tabs for:

1. Input Data
2. Exploratory Data Analysis (EDA)
3. Data Engineering & Cleaning
4. Feature Selection
5. Data Split
6. Model Selection
7. Model Training
8. K-Fold Validation
9. Performance Metrics
10. Live URL Inference

## Tech stack

- Python
- Streamlit
- scikit-learn
- pandas / numpy
- matplotlib

## Dataset format

Upload a `.csv` or `.tsv` file with:

- `url`: URL string
- `label`: `0` for safe, `1` for fake/suspicious

If no file is uploaded, the app uses a built-in synthetic phishing dataset for demonstration.

## Run locally

1. Create and activate virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start Streamlit:

```bash
streamlit run app.py
```

## Exhibition demo flow (recommended)

1. Open `Input Data` and explain source.
2. Show class distribution and heatmap in `EDA`.
3. Explain cleaning report and engineered features.
4. Show selected features from mutual information.
5. Pick model + split + K value from sidebar.
6. Click **Train and Evaluate Pipeline**.
7. Present K-Fold and final metrics (accuracy, precision, recall, F1).
8. Use `Live URL Inference` for real-time testing.

## Note

This project is designed for academic demonstration and learning. It is not a production-grade security product.
