"""
Financial Sentiment Analyzer.

Uses FinBERT (ProsusAI/finbert) when transformers/torch are available.
Falls back to a transparent keyword heuristic otherwise.

Outputs: positive | neutral | negative
"""

from __future__ import annotations

import logging
import re
from functools import lru_cache

from src.utils.config import SENTIMENT_MODEL_NAME

logger = logging.getLogger(__name__)

# ── Keyword Fallback ──────────────────────────────────────────────────────────
_NEG_KW = [
    "violat", "fine", "penalt", "lawsuit", "fraud", "scandal", "spill",
    "accident", "injur", "death", "recall", "ban", "investigat",
    "exceed", "breach", "fail", "loss", "cut", "layoff", "strike",
]
_POS_KW = [
    "achiev", "milestone", "record", "award", "certif", "clean",
    "renew", "sustain", "commit", "launch", "partner", "improv",
    "expand", "growth", "innovat", "voluntar", "pledge",
]


def _keyword_sentiment(text: str) -> tuple[str, float]:
    lower = text.lower()
    neg = sum(1 for kw in _NEG_KW if re.search(kw, lower))
    pos = sum(1 for kw in _POS_KW if re.search(kw, lower))
    if neg > pos:
        conf = round(min(0.55 + neg * 0.05, 0.92), 4)
        return "negative", conf
    if pos > neg:
        conf = round(min(0.55 + pos * 0.05, 0.92), 4)
        return "positive", conf
    return "neutral", 0.60


@lru_cache(maxsize=1)
def _load_pipeline():
    try:
        from transformers import pipeline as hf_pipeline
        logger.info("Loading sentiment model '%s' …", SENTIMENT_MODEL_NAME)
        return hf_pipeline(
            "text-classification",
            model=SENTIMENT_MODEL_NAME,
            top_k=1,
            truncation=True,
            max_length=512,
        )
    except Exception as exc:
        logger.warning("FinBERT sentiment unavailable (%s); using keyword fallback.", exc)
        return None


def analyze(text: str) -> tuple[str, float]:
    """Returns (label, confidence). label ∈ {'positive', 'neutral', 'negative'}."""
    if not text.strip():
        return "neutral", 0.0
    clf = _load_pipeline()
    if clf is None:
        return _keyword_sentiment(text)
    try:
        result = clf(text)[0]
        if isinstance(result, list):
            result = result[0]
        return result["label"].lower(), round(result["score"], 4)
    except Exception as exc:
        logger.error("Sentiment analysis error: %s", exc)
        return _keyword_sentiment(text)


def analyze_batch(texts: list[str]) -> list[tuple[str, float]]:
    if not texts:
        return []
    clf = _load_pipeline()
    if clf is None:
        return [_keyword_sentiment(t) for t in texts]
    try:
        results = clf(texts)
        output = []
        for res in results:
            if isinstance(res, list):
                res = res[0]
            output.append((res["label"].lower(), round(res["score"], 4)))
        return output
    except Exception as exc:
        logger.error("Batch sentiment error: %s", exc)
        return [_keyword_sentiment(t) for t in texts]
