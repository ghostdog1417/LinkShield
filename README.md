# Fake Link Detector

A Streamlit dashboard that uses a lightweight machine learning model to flag suspicious URLs and explain why they look risky.

## Features

- Fast URL risk scoring with an ML classifier
- Simple explanation cues for suspicious patterns
- Sample links for quick testing
- Batch analysis from pasted URLs

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the dashboard:
   ```bash
   streamlit run app.py
   ```

## Notes

The model is trained on synthetic examples built from common phishing and benign URL patterns. It is useful for demos and screening, but it is not a security replacement for a production threat-intelligence pipeline.
