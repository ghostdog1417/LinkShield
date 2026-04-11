from __future__ import annotations

import textwrap
import re
from io import StringIO

import pandas as pd
import streamlit as st

from fake_link_detector.detector import analyze_many, analyze_url, train_detector


st.set_page_config(
    page_title="Fake Link Detector",
    page_icon="link",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource(show_spinner="Training the URL detector...")
def load_model():
    return train_detector()


MODEL = load_model()


SAMPLES = [
    "https://github.com/security",
    "https://support.google.com/mail",
    "http://verify-paypa1-login.zip/account/update?token=ab12cd34",
    "https://secure.apple.com-billing.quest/login/confirm",
    "https://docs.python.org/3/library/",
]


def parse_pasted_links(raw_text: str) -> list[str]:
    candidates = [part.strip() for part in re.split(r"[\n,\s]+", raw_text) if part.strip()]
    links: list[str] = []

    for candidate in candidates:
        if candidate.startswith(("http://", "https://")):
            links.append(candidate)
        elif "." in candidate and "@" not in candidate:
            links.append("https://" + candidate)

    return links


def parse_uploaded_links(uploaded_file) -> list[str]:
    if uploaded_file is None:
        return []

    raw_text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
    if not raw_text.strip():
        return []

    if uploaded_file.name.lower().endswith((".csv", ".tsv")):
        try:
            frame = pd.read_csv(StringIO(raw_text), dtype=str, keep_default_na=False)
            cells = frame.astype(str).fillna("").values.flatten().tolist()
            return parse_pasted_links("\n".join(cells))
        except Exception:
            pass

    return parse_pasted_links(raw_text)


def merge_links(*groups: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()

    for group in groups:
        for link in group:
            normalized = link.strip()
            if normalized and normalized not in seen:
                seen.add(normalized)
                merged.append(normalized)

    return merged


st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(35, 82, 124, 0.28), transparent 28%),
            radial-gradient(circle at top right, rgba(192, 93, 54, 0.22), transparent 24%),
            linear-gradient(180deg, #07111f 0%, #0d1726 45%, #111a2a 100%);
        color: #ecf2ff;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .hero {
        padding: 1.4rem 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(14, 29, 48, 0.9), rgba(22, 39, 63, 0.72));
        box-shadow: 0 18px 60px rgba(0, 0, 0, 0.28);
        margin-bottom: 1.4rem;
    }
    .hero h1 {
        margin: 0;
        font-size: 3rem;
        line-height: 1.05;
    }
    .hero p {
        margin-top: 0.6rem;
        color: rgba(236, 242, 255, 0.78);
        max-width: 62ch;
        font-size: 1.02rem;
    }
    .metric-card {
        padding: 1rem 1.1rem;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.08);
        height: 100%;
    }
    .metric-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: rgba(236, 242, 255, 0.58);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }
    .pill {
        display: inline-block;
        padding: 0.28rem 0.62rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 0.2rem 0.28rem 0.2rem 0;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="hero">
        <h1>Fake Link Detector</h1>
        <p>
            Paste a URL or a batch of links to score them with a lightweight machine learning model.
            The dashboard highlights risky patterns like fake subdomains, suspicious TLDs, and phishing-style paths.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.header("Controls")
    selected_sample = st.selectbox("Load a sample URL", ["Custom"] + SAMPLES)
    st.caption("Use the samples to see how the detector behaves on safe and suspicious links.")
    st.markdown("### Sample signals")
    st.markdown("<span class='pill'>brand spoofing</span><span class='pill'>IP hosts</span><span class='pill'>random tokens</span><span class='pill'>odd TLDs</span>", unsafe_allow_html=True)


col_left, col_right = st.columns([1.2, 0.8], gap="large")

with col_left:
    st.subheader("Single link analysis")
    default_url = selected_sample if selected_sample != "Custom" else "https://example.com/security"
    url_input = st.text_area("URL", value=default_url, height=90, placeholder="https://example.com/login")
    analyze_button = st.button("Analyze URL", type="primary")

    if analyze_button:
        result = analyze_url(url_input, MODEL)
        score_pct = round(result.score * 100, 1)
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Verdict</div>
                <div class="metric-value">{result.label}</div>
                <div style="margin-top:0.35rem; color: rgba(236,242,255,0.82);">Risk score: {score_pct}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(result.score)

        if result.reasons:
            st.markdown("**Why it was flagged**")
            for reason in result.reasons:
                st.write(f"- {reason}")

        feature_frame = pd.DataFrame(
            [
                {
                    "host": result.features.get("host", ""),
                    "path": result.features.get("path", ""),
                    "scheme": result.features.get("scheme", ""),
                    "subdomains": result.features.get("subdomain_count", 0),
                    "digits": result.features.get("digit_count", 0),
                    "hyphens": result.features.get("hyphen_count", 0),
                    "url_length": result.features.get("url_length", 0),
                }
            ]
        )
        st.dataframe(feature_frame, use_container_width=True, hide_index=True)

with col_right:
    st.subheader("Batch scan")
    batch_text = st.text_area(
        "Paste links separated by commas, spaces, or new lines",
        value="\n".join(SAMPLES[:3]),
        height=180,
        help="Paste multiple links and detect them together.",
    )
    uploaded_links_file = st.file_uploader(
        "Or upload a .txt, .csv, or .tsv file",
        type=["txt", "csv", "tsv"],
        help="Each row can contain a URL, or a CSV column can hold one or more URLs.",
    )

    if st.button("Detect pasted links"):
        pasted_links = parse_pasted_links(batch_text)
        uploaded_links = parse_uploaded_links(uploaded_links_file)
        batch_results = analyze_many(merge_links(pasted_links, uploaded_links), MODEL)
        if batch_results:
            df = pd.DataFrame(
                [
                    {
                        "url": item.url,
                        "score": round(item.score, 3),
                        "verdict": item.label,
                    }
                    for item in batch_results
                ]
            ).sort_values("score", ascending=False)
            st.caption(f"Scanned {len(batch_results)} unique link(s).")
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.bar_chart(df.set_index("url")[["score"]])
        else:
            st.info("Paste or upload at least one valid link to scan.")

    st.markdown("### What the model looks for")
    insight_text = textwrap.dedent(
        """
        - brand-like words mixed with unrelated domains
        - plain HTTP and IP-based hosts
        - long random paths and tracking parameters
        - suspicious TLDs and stacked subdomains
        """
    ).strip()
    st.markdown(insight_text)
