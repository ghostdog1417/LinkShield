from __future__ import annotations

from dataclasses import dataclass
import random
import re
import string
from typing import Iterable
from urllib.parse import parse_qs, urlparse

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


_BENIGN_DOMAINS = [
    "example.com",
    "openai.com",
    "github.com",
    "python.org",
    "wikipedia.org",
    "docs.microsoft.com",
    "support.google.com",
    "news.ycombinator.com",
    "stripe.com",
    "cloudflare.com",
]

_BENIGN_PATHS = [
    "/",
    "/about",
    "/pricing",
    "/docs",
    "/blog",
    "/support",
    "/security",
    "/products",
    "/download",
]

_MALICIOUS_WORDS = [
    "verify",
    "login",
    "secure",
    "update",
    "account",
    "reset",
    "wallet",
    "invoice",
    "payment",
    "signin",
]

_SUSPICIOUS_TLDS = ["zip", "top", "xyz", "info", "click", "country", "quest"]

FEATURE_COLUMNS = [
    "subdomain_count",
    "digit_count",
    "hyphen_count",
    "url_length",
    "query_param_count",
    "path_depth",
    "suspicious_word_count",
    "has_http",
    "has_ip_host",
    "tld_is_suspicious",
    "at_symbol_count",
    "special_char_count",
]


@dataclass(frozen=True)
class LinkAnalysis:
    url: str
    score: float
    label: str
    reasons: list[str]
    features: dict[str, object]


@dataclass(frozen=True)
class EvaluationResult:
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float


@dataclass(frozen=True)
class TrainingBundle:
    model_name: str
    model: object
    selected_features: list[str]
    feature_scores: pd.DataFrame
    train_size: int
    test_size: int
    metrics: EvaluationResult
    kfold_scores: dict[str, float]


def _random_token(rng: random.Random, length: int = 8) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(rng.choice(alphabet) for _ in range(length))


def _benign_url(rng: random.Random) -> str:
    domain = rng.choice(_BENIGN_DOMAINS)
    path = rng.choice(_BENIGN_PATHS)
    if rng.random() < 0.3:
        path = f"{path.rstrip('/')}/{rng.choice(['guide', 'api', 'faq', 'terms', 'security'])}"
    if rng.random() < 0.2:
        query = f"?ref={rng.choice(['home', 'email', 'search'])}"
    else:
        query = ""
    scheme = rng.choice(["https", "https", "http"])
    return f"{scheme}://{domain}{path}{query}"


def _malicious_url(rng: random.Random) -> str:
    word = rng.choice(_MALICIOUS_WORDS)
    tld = rng.choice(_SUSPICIOUS_TLDS)
    brand = rng.choice(["paypa1", "micr0soft", "app1e", "g00gle", "amaz0n", "netfIix"]).lower()
    prefix = rng.choice(["secure", "login", "account", "verify", "update", "auth", "billing"])
    suffix = rng.choice(["center", "portal", "service", "support", "confirm", "check", "access"])

    if rng.random() < 0.25:
        host = f"http://{rng.randint(11, 223)}.{rng.randint(0, 255)}.{rng.randint(0, 255)}.{rng.randint(1, 254)}"
    elif rng.random() < 0.35:
        host = f"https://{brand}.{prefix}-{suffix}.{tld}"
    else:
        host = f"https://{prefix}.{brand}-{suffix}.{tld}"

    path_bits = [word, rng.choice(["verify", "security", "session", "update", "unlock"])]
    if rng.random() < 0.4:
        path_bits.append(_random_token(rng, 10))
    path = "/" + "/".join(path_bits)

    if rng.random() < 0.6:
        query = f"?{rng.choice(['token', 'id', 'session', 'redir'])}={_random_token(rng, 14)}"
    else:
        query = ""

    return f"{host}{path}{query}"


def build_training_set(size: int = 1600, seed: int = 42) -> tuple[list[str], list[int]]:
    rng = random.Random(seed)
    urls: list[str] = []
    labels: list[int] = []

    for _ in range(size // 2):
        urls.append(_benign_url(rng))
        labels.append(0)
        urls.append(_malicious_url(rng))
        labels.append(1)

    paired = list(zip(urls, labels, strict=False))
    rng.shuffle(paired)
    shuffled_urls, shuffled_labels = zip(*paired, strict=False)
    return list(shuffled_urls), list(shuffled_labels)


def build_demo_dataframe(size: int = 1600, seed: int = 42) -> pd.DataFrame:
    urls, labels = build_training_set(size=size, seed=seed)
    frame = pd.DataFrame({"url": urls, "label": labels})
    return frame


def _make_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            (
                "vectorizer",
                TfidfVectorizer(
                    analyzer="char",
                    ngram_range=(3, 5),
                    lowercase=True,
                    min_df=1,
                ),
            ),
            (
                "model",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def train_detector(seed: int = 42) -> Pipeline:
    urls, labels = build_training_set(seed=seed)
    pipeline = _make_pipeline()
    pipeline.fit(urls, labels)
    return pipeline


def _extract_features(url: str) -> dict[str, object]:
    parsed = urlparse(url.strip())
    host = parsed.hostname or ""
    path = parsed.path or "/"
    query = parse_qs(parsed.query)

    subdomain_count = host.count(".") - 1 if host.count(".") > 1 else 0
    digit_count = sum(char.isdigit() for char in url)
    hyphen_count = url.count("-")
    suspicious_words = [word for word in _MALICIOUS_WORDS if word in url.lower()]
    ip_address_like = bool(re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host))
    tld = host.rsplit(".", 1)[-1] if "." in host else ""
    query_param_count = len(query)
    path_depth = len([part for part in path.split("/") if part])
    suspicious_word_count = len(suspicious_words)
    has_http = 1 if (parsed.scheme or "").lower() == "http" else 0
    has_ip_host = 1 if ip_address_like else 0
    tld_is_suspicious = 1 if tld in _SUSPICIOUS_TLDS else 0
    at_symbol_count = url.count("@")
    special_char_count = sum(char in "!#$%^*()[]{}<>|\\~`" for char in url)

    return {
        "scheme": parsed.scheme or "",
        "host": host,
        "path": path,
        "query_keys": list(query.keys()),
        "subdomain_count": subdomain_count,
        "digit_count": digit_count,
        "hyphen_count": hyphen_count,
        "url_length": len(url),
        "ip_address_like": ip_address_like,
        "suspicious_words": suspicious_words,
        "tld": tld,
        "query_param_count": query_param_count,
        "path_depth": path_depth,
        "suspicious_word_count": suspicious_word_count,
        "has_http": has_http,
        "has_ip_host": has_ip_host,
        "tld_is_suspicious": tld_is_suspicious,
        "at_symbol_count": at_symbol_count,
        "special_char_count": special_char_count,
    }


def load_project_dataset(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"url", "label"}
    if not required.issubset({col.lower() for col in frame.columns}):
        raise ValueError("Dataset must contain columns: url, label")

    rename_map = {col: col.lower() for col in frame.columns}
    data = frame.rename(columns=rename_map).copy()
    data["url"] = data["url"].astype(str)
    data["label"] = pd.to_numeric(data["label"], errors="coerce")
    data = data.dropna(subset=["url", "label"])
    data["label"] = data["label"].astype(int)
    data = data[data["label"].isin([0, 1])]
    return data[["url", "label"]]


def clean_dataset(data: pd.DataFrame, remove_outliers: bool = True) -> tuple[pd.DataFrame, dict[str, int]]:
    cleaned = data.copy()
    report = {
        "input_rows": len(cleaned),
        "dropped_empty_url": 0,
        "dropped_duplicates": 0,
        "dropped_outliers": 0,
    }

    before_empty = len(cleaned)
    cleaned["url"] = cleaned["url"].astype(str).str.strip()
    cleaned = cleaned[cleaned["url"] != ""]
    report["dropped_empty_url"] = before_empty - len(cleaned)

    before_dupes = len(cleaned)
    cleaned = cleaned.drop_duplicates(subset=["url", "label"])
    report["dropped_duplicates"] = before_dupes - len(cleaned)

    if remove_outliers and not cleaned.empty:
        lengths = cleaned["url"].str.len().astype(float)
        q1 = lengths.quantile(0.25)
        q3 = lengths.quantile(0.75)
        iqr = q3 - q1
        lower = max(1, q1 - 1.5 * iqr)
        upper = q3 + 1.5 * iqr
        before_outliers = len(cleaned)
        cleaned = cleaned[(lengths >= lower) & (lengths <= upper)]
        report["dropped_outliers"] = before_outliers - len(cleaned)

    return cleaned.reset_index(drop=True), report


def build_feature_frame(urls: Iterable[str]) -> pd.DataFrame:
    rows: list[dict[str, float]] = []
    for raw_url in urls:
        url = str(raw_url).strip()
        if not url:
            continue
        normalized = url if "://" in url else f"https://{url}"
        f = _extract_features(normalized)
        rows.append(
            {
                "subdomain_count": float(f["subdomain_count"]),
                "digit_count": float(f["digit_count"]),
                "hyphen_count": float(f["hyphen_count"]),
                "url_length": float(f["url_length"]),
                "query_param_count": float(f["query_param_count"]),
                "path_depth": float(f["path_depth"]),
                "suspicious_word_count": float(f["suspicious_word_count"]),
                "has_http": float(f["has_http"]),
                "has_ip_host": float(f["has_ip_host"]),
                "tld_is_suspicious": float(f["tld_is_suspicious"]),
                "at_symbol_count": float(f["at_symbol_count"]),
                "special_char_count": float(f["special_char_count"]),
            }
        )
    return pd.DataFrame(rows, columns=FEATURE_COLUMNS)


def split_features_labels(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    x = build_feature_frame(data["url"].tolist())
    y = data["label"].astype(int)
    return x, y


def get_model_registry() -> dict[str, object]:
    return {
        "Logistic Regression": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=1200, random_state=42)),
            ]
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=250,
            random_state=42,
            class_weight="balanced",
        ),
        "SVC (RBF)": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", SVC(probability=True, random_state=42)),
            ]
        ),
    }


def select_top_features(x: pd.DataFrame, y: pd.Series, k: int = 8) -> tuple[list[str], pd.DataFrame]:
    k_value = max(1, min(k, x.shape[1]))
    selector = SelectKBest(score_func=mutual_info_classif, k=k_value)
    selector.fit(x, y)

    scores = pd.DataFrame(
        {
            "feature": x.columns,
            "score": np.asarray(selector.scores_, dtype=float),
            "selected": selector.get_support(),
        }
    ).sort_values("score", ascending=False)

    chosen = scores[scores["selected"]]["feature"].tolist()
    return chosen, scores.reset_index(drop=True)


def evaluate_predictions(y_true: pd.Series, y_pred: np.ndarray, model_name: str) -> EvaluationResult:
    return EvaluationResult(
        model_name=model_name,
        accuracy=float(accuracy_score(y_true, y_pred)),
        precision=float(precision_score(y_true, y_pred, zero_division=0)),
        recall=float(recall_score(y_true, y_pred, zero_division=0)),
        f1_score=float(f1_score(y_true, y_pred, zero_division=0)),
    )


def kfold_validate(model: object, x: pd.DataFrame, y: pd.Series, folds: int = 5) -> dict[str, float]:
    cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=42)
    metrics = {
        "accuracy": [],
        "precision": [],
        "recall": [],
        "f1": [],
    }

    for train_idx, test_idx in cv.split(x, y):
        model_fold = clone(model)
        x_train = x.iloc[train_idx]
        y_train = y.iloc[train_idx]
        x_test = x.iloc[test_idx]
        y_test = y.iloc[test_idx]

        model_fold.fit(x_train, y_train)
        preds = model_fold.predict(x_test)

        metrics["accuracy"].append(float(accuracy_score(y_test, preds)))
        metrics["precision"].append(float(precision_score(y_test, preds, zero_division=0)))
        metrics["recall"].append(float(recall_score(y_test, preds, zero_division=0)))
        metrics["f1"].append(float(f1_score(y_test, preds, zero_division=0)))

    return {name: float(np.mean(values)) for name, values in metrics.items()}


def train_pipeline(
    data: pd.DataFrame,
    model_name: str,
    test_size: float = 0.2,
    feature_k: int = 8,
    folds: int = 5,
) -> TrainingBundle:
    x, y = split_features_labels(data)
    chosen_features, score_frame = select_top_features(x, y, k=feature_k)

    x_selected = x[chosen_features]
    x_train, x_test, y_train, y_test = train_test_split(
        x_selected,
        y,
        test_size=test_size,
        stratify=y,
        random_state=42,
    )

    models = get_model_registry()
    if model_name not in models:
        raise ValueError(f"Unknown model '{model_name}'.")

    model = clone(models[model_name])
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    metrics = evaluate_predictions(y_test, predictions, model_name=model_name)
    kfold_scores = kfold_validate(clone(model), x_selected, y, folds=folds)

    return TrainingBundle(
        model_name=model_name,
        model=model,
        selected_features=chosen_features,
        feature_scores=score_frame,
        train_size=len(x_train),
        test_size=len(x_test),
        metrics=metrics,
        kfold_scores=kfold_scores,
    )


def _rule_reasons(features: dict[str, object]) -> list[str]:
    reasons: list[str] = []
    host = str(features["host"])
    path = str(features["path"])
    tld = str(features["tld"])

    if features["scheme"] == "http":
        reasons.append("Uses plain HTTP instead of HTTPS.")
    if features["ip_address_like"]:
        reasons.append("Domain is an IP address, which is common in fake links.")
    if int(features["subdomain_count"]) >= 2:
        reasons.append("Has multiple subdomains that can hide the real domain.")
    if int(features["hyphen_count"]) >= 2:
        reasons.append("Contains many hyphens, a common phishing pattern.")
    if int(features["digit_count"]) >= 6:
        reasons.append("Contains many digits and random-looking tokens.")
    if any(word in path.lower() or word in host.lower() for word in _MALICIOUS_WORDS):
        reasons.append("Contains words commonly used in credential theft or fake alerts.")
    if tld in _SUSPICIOUS_TLDS:
        reasons.append("Uses a TLD that is often abused by low-quality scam sites.")
    if features["query_keys"]:
        reasons.append("Includes tracking-style query parameters.")

    return reasons[:5]


def analyze_url(url: str, model: Pipeline) -> LinkAnalysis:
    cleaned = url.strip()
    if not cleaned:
        return LinkAnalysis(
            url=url,
            score=0.0,
            label="No URL provided",
            reasons=["Paste a URL to analyze it."],
            features={"host": "", "path": "", "scheme": ""},
        )

    if "://" not in cleaned:
        cleaned = "https://" + cleaned

    probability = float(model.predict_proba([cleaned])[0][1])
    features = _extract_features(cleaned)
    reasons = _rule_reasons(features)

    if probability >= 0.75:
        label = "High risk"
    elif probability >= 0.5:
        label = "Suspicious"
    else:
        label = "Likely safe"

    return LinkAnalysis(
        url=cleaned,
        score=probability,
        label=label,
        reasons=reasons or ["The URL does not show strong phishing signals."],
        features=features,
    )


def analyze_many(urls: Iterable[str], model: Pipeline) -> list[LinkAnalysis]:
    return [analyze_url(url, model) for url in urls if url.strip()]
