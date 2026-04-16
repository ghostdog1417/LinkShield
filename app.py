from __future__ import annotations

from io import StringIO

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from fake_link_detector.detector import (
    FEATURE_COLUMNS,
    analyze_url,
    build_demo_dataframe,
    build_feature_frame,
    clean_dataset,
    get_model_registry,
    load_project_dataset,
    train_detector,
    train_pipeline,
)


st.set_page_config(
    page_title="LinkShield CA-2 Dashboard",
    page_icon="shield",
    layout="centered",
)


@st.cache_data(show_spinner=False)
def load_default_dataset() -> pd.DataFrame:
    return build_demo_dataframe(size=2000, seed=42)


@st.cache_resource(show_spinner=False)
def load_live_url_model():
    return train_detector(seed=42)


def load_uploaded_dataset(uploaded_file) -> pd.DataFrame:
    raw = uploaded_file.getvalue().decode("utf-8", errors="ignore")
    if uploaded_file.name.lower().endswith(".tsv"):
        frame = pd.read_csv(StringIO(raw), sep="\t")
    else:
        frame = pd.read_csv(StringIO(raw))
    return load_project_dataset(frame)


def render_heatmap(frame: pd.DataFrame):
    corr = frame.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    im = ax.imshow(corr, cmap="YlOrRd", interpolation="nearest")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.index)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(corr.index, fontsize=8)
    ax.set_title("Correlation Heatmap")
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.03)
    st.pyplot(fig)


st.title("LinkShield: ANN & ML CA-2 Exhibition")
st.caption("Simple and stable pipeline demo: input, EDA, cleaning, feature selection, split, training, K-fold, metrics, and live URL prediction.")

with st.sidebar:
    st.header("Run Configuration")
    test_size = st.slider("Test set ratio", min_value=0.1, max_value=0.4, value=0.2, step=0.05)
    feature_k = st.slider("Number of selected features", min_value=4, max_value=len(FEATURE_COLUMNS), value=8, step=1)
    folds = st.slider("K-Fold splits", min_value=3, max_value=10, value=5, step=1)
    selected_model = st.selectbox("Model Selection", options=list(get_model_registry().keys()))
    remove_outliers = st.checkbox("Apply IQR outlier removal", value=True)


uploaded = st.file_uploader("Upload dataset (.csv/.tsv) with columns: url, label (0=safe, 1=fake)", type=["csv", "tsv"])

if uploaded is not None:
    try:
        raw_data = load_uploaded_dataset(uploaded)
        data_source = f"Uploaded file: {uploaded.name}"
    except Exception as err:
        st.error(f"Unable to parse uploaded data: {err}")
        raw_data = load_default_dataset()
        data_source = "Fallback synthetic dataset"
else:
    raw_data = load_default_dataset()
    data_source = "Built-in synthetic phishing dataset"


cleaned_data, cleaning_report = clean_dataset(raw_data, remove_outliers=remove_outliers)
features_df = build_feature_frame(cleaned_data["url"]) if not cleaned_data.empty else pd.DataFrame(columns=FEATURE_COLUMNS)

if "trained_bundle" not in st.session_state:
    st.session_state.trained_bundle = None

st.subheader("1) Input Data")
st.write(f"Data source: **{data_source}**")
st.write(f"Rows: **{len(raw_data)}**")
st.dataframe(raw_data.head(15), width="stretch")

st.subheader("2) EDA")
if cleaned_data.empty:
    st.warning("No rows available after cleaning.")
else:
    class_counts = cleaned_data["label"].value_counts().rename(index={0: "Safe", 1: "Fake"})
    st.bar_chart(class_counts)
    st.dataframe(features_df.describe().T, width="stretch")
    render_heatmap(features_df)

st.subheader("3) Data Engineering & Cleaning")
st.dataframe(pd.DataFrame([cleaning_report]), width="stretch", hide_index=True)
st.write(f"Rows after cleaning: **{len(cleaned_data)}**")

st.subheader("4) Feature Selection, Split, Model Selection, Training")
st.write(f"Model: **{selected_model}** | Test size: **{test_size}** | Top-K features: **{feature_k}** | K-Fold: **{folds}**")

if st.button("Train and Evaluate Pipeline", type="primary"):
    if cleaned_data.empty or len(cleaned_data["label"].unique()) < 2:
        st.error("Training requires non-empty data with both classes (0 and 1).")
    else:
        st.session_state.trained_bundle = train_pipeline(
            cleaned_data,
            model_name=selected_model,
            test_size=test_size,
            feature_k=feature_k,
            folds=folds,
        )

bundle = st.session_state.trained_bundle

if bundle is None:
    st.info("Click 'Train and Evaluate Pipeline' to run model training.")
else:
    st.success(f"Training complete using {bundle.model_name}")
    st.write(f"Train rows: **{bundle.train_size}** | Test rows: **{bundle.test_size}**")

    st.subheader("5) Feature Selection")
    st.dataframe(bundle.feature_scores, width="stretch")
    st.write("Selected features: " + ", ".join(bundle.selected_features))

    st.subheader("6) K-Fold Validation")
    kfold_df = pd.DataFrame([bundle.kfold_scores]).rename(
        columns={
            "accuracy": "cv_accuracy",
            "precision": "cv_precision",
            "recall": "cv_recall",
            "f1": "cv_f1",
        }
    )
    st.dataframe(kfold_df, width="stretch", hide_index=True)

    st.subheader("7) Performance Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Accuracy", f"{bundle.metrics.accuracy:.3f}")
        st.metric("Precision", f"{bundle.metrics.precision:.3f}")
    with col2:
        st.metric("Recall", f"{bundle.metrics.recall:.3f}")
        st.metric("F1 Score", f"{bundle.metrics.f1_score:.3f}")

st.subheader("8) Live URL Inference")
st.caption("Simple real-time demo for your exhibition.")
live_model = load_live_url_model()
sample_url = st.text_input("Enter URL", value="https://secure-paypa1-login.zip/account/verify")
if st.button("Analyze URL"):
    result = analyze_url(sample_url, live_model)
    st.write(f"Verdict: **{result.label}**")
    st.write(f"Risk score: **{result.score:.3f}**")
    st.progress(float(result.score))
    for reason in result.reasons:
        st.write(f"- {reason}")

    preview = build_feature_frame([sample_url])
    st.dataframe(preview, width="stretch")
