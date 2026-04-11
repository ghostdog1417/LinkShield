# Fake Link Detector

A Streamlit-based phishing-link screening dashboard that scores URLs with a lightweight machine learning classifier and rule-based explanations.

It is designed for learning, demos, and quick triage of suspicious links.

## What this app does

The app provides two analysis modes:

1. Single URL analysis for deep inspection of one link.
2. Batch link scanning for many links at once (pasted or uploaded).

Each analyzed URL receives:

- A risk score (0.0 to 1.0)
- A verdict label
- Human-readable explanation reasons
- Extracted URL features (host, path, scheme, counts, etc.)

## Complete feature list

### 1. Streamlit dashboard UI

- Full-page dashboard layout with custom styling and themed gradients.
- Sidebar controls for quick sample selection.
- Split view:
   - Left column for single-link analysis
   - Right column for batch scanning
- Built-in data tables and score charts for results.

### 2. Single link analyzer

- Input via text area (`URL`).
- Auto-normalization behavior:
   - If scheme is missing, `https://` is automatically prepended.
- One-click analysis with `Analyze URL` button.
- Displays:
   - Verdict card (`Likely safe`, `Suspicious`, `High risk`)
   - Risk score percentage
   - Progress bar for score
   - Up to 5 explanation bullets
   - Feature table (`host`, `path`, `scheme`, `subdomains`, `digits`, `hyphens`, `url_length`)

### 3. Batch scanning

- Paste multiple links separated by:
   - new lines
   - commas
   - whitespace
- Upload input files:
   - `.txt`
   - `.csv`
   - `.tsv`
- CSV/TSV behavior:
   - Reads all cells as text
   - Flattens the entire table
   - Extracts URL-like tokens from every cell
- URL extraction behavior:
   - Keeps values starting with `http://` or `https://`
   - Converts bare domains (for example `example.com`) to `https://example.com`
   - Ignores obvious non-URL tokens and email-like values
- Merges pasted + uploaded URLs
- De-duplicates links while preserving first-seen order
- Displays:
   - Number of unique scanned links
   - Results table sorted by highest score first
   - Bar chart of risk scores

### 4. Built-in sample dataset

- Preloaded safe and suspicious example URLs in the sidebar.
- `Custom` mode lets users provide their own URL without sample override.

### 5. On-start model training and caching

- The detector model is trained automatically at app startup.
- Uses Streamlit `@st.cache_resource` so training runs once per session/process and is reused.
- Startup spinner message indicates training state.

### 6. Synthetic training data generation

- Balanced synthetic dataset (default size: 1600 URLs, half benign and half malicious).
- Deterministic random seed support for reproducibility (`seed=42` by default).
- Benign URL generator includes:
   - realistic domains
   - common navigation paths
   - occasional query parameters
   - mixed HTTP/HTTPS (HTTPS-biased)
- Malicious URL generator includes patterns such as:
   - brand spoofing strings (`paypa1`, `g00gle`, etc.)
   - suspicious TLDs (`zip`, `top`, `xyz`, `info`, `click`, `country`, `quest`)
   - credential-theft words (`verify`, `login`, `reset`, etc.)
   - random token segments and query values
   - occasional IP-based hosts

### 7. ML pipeline architecture

The model is a scikit-learn pipeline:

1. `TfidfVectorizer`
    - Character-level analysis
    - n-grams from 3 to 5
    - lowercase normalization
2. `LogisticRegression`
    - `max_iter=1000`
    - `class_weight='balanced'`
    - `random_state=42`

### 8. Feature extraction engine

For each URL, the detector extracts structured features:

- `scheme`
- `host`
- `path`
- `query_keys`
- `subdomain_count`
- `digit_count`
- `hyphen_count`
- `url_length`
- `ip_address_like`
- `suspicious_words`
- `tld`

### 9. Rule-based explanation layer

In addition to ML score, the app derives explanation reasons from URL features.

Possible reasons include:

- Uses plain HTTP instead of HTTPS
- Host looks like an IP address
- Too many stacked subdomains
- Many hyphens
- Many digits/random-like tokens
- Credential-theft keywords in host/path
- Suspicious TLD
- Query parameters present

Up to 5 reasons are returned for readability.

Fallback message:

- If no suspicious reason is triggered, the app returns: `The URL does not show strong phishing signals.`

### 10. Verdict mapping

Risk probability is mapped to labels using fixed thresholds:

- `>= 0.75` -> `High risk`
- `>= 0.50 and < 0.75` -> `Suspicious`
- `< 0.50` -> `Likely safe`

### 11. Edge-case handling

- Empty single URL input returns:
   - label: `No URL provided`
   - score: `0.0`
   - guidance reason prompting user to paste a URL
- Empty/invalid upload content is safely ignored.
- Batch action with no valid URLs shows a helpful info prompt.

## Project structure

```
fake-link-detector/
|-- app.py
|-- README.md
|-- requirements.txt
`-- fake_link_detector/
      |-- __init__.py
      `-- detector.py
```

- `app.py`: Streamlit UI, input parsing, model loading, and visualization.
- `fake_link_detector/detector.py`: Synthetic data generation, model training, URL analysis logic.
- `requirements.txt`: runtime dependencies.

## Requirements

Dependencies listed in `requirements.txt`:

- `streamlit>=1.33`
- `scikit-learn>=1.4`
- `pandas>=2.2`
- `numpy>=1.26`
- `joblib>=1.3`

## Setup and run

### 1. Create a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install packages

```bash
pip install -r requirements.txt
```

### 3. Start the app

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit (usually `http://localhost:8501`).

## How to use

### Single URL mode

1. Enter a URL in the left panel.
2. Click `Analyze URL`.
3. Review verdict, score, reasons, and extracted feature table.

### Batch mode

1. Paste many links in the right panel and/or upload `.txt`, `.csv`, `.tsv`.
2. Click `Detect pasted links`.
3. Review sorted table and bar chart.

## Notes and limitations

- The model is trained on synthetic data, not a live threat-intel feed.
- Scores are useful for screening and demos, not final security decisions.
- The detector can produce false positives and false negatives.
- Use this tool as an assistant layer alongside other security controls.

## Future enhancement ideas

- Persist and load a pre-trained model instead of training on startup.
- Add domain reputation and WHOIS-based signals.
- Export batch results to CSV.
- Add confidence calibration and threshold controls in UI.
- Add unit tests for parser, feature extraction, and threshold logic.
