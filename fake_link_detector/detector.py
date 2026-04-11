from __future__ import annotations

from dataclasses import dataclass
import random
import re
import string
from typing import Iterable
from urllib.parse import parse_qs, urlparse

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


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


@dataclass(frozen=True)
class LinkAnalysis:
    url: str
    score: float
    label: str
    reasons: list[str]
    features: dict[str, object]


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
    }


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
