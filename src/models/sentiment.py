"""
Financial Sentiment Analyzer using FinBERT (ProsusAI/finbert).

Detects polarity of financial/ESG text:
  - positive
  - neutral
  - negative

Model: ProsusAI/finbert (HuggingFace)
"""

from __future__ import annotations

import logging
from functools import lru_cache

from transformers import pipeline, Pipeline

from src.utils.config import SENTIMENT_MODEL_NAME

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _load_pipeline() -> Pipeline:
    logger.info("Loading sentiment model '%s' …", SENTIMENT_MODEL_NAME)
    return pipeline(
        "text-classification",
        model=SENTIMENT_MODEL_NAME,
        top_k=1,
        truncation=True,
        max_length=512,
    )


def analyze(text: str) -> tuple[str, float]:
    """
    Returns (label, confidence).
    label is one of 'positive', 'neutral', 'negative'.
    """
    if not text.strip():
        return "neutral", 0.0
    try:
        clf = _load_pipeline()
        result = clf(text)[0]
        if isinstance(result, list):
            result = result[0]
        label = result["label"].lower()
        score = round(result["score"], 4)
        return label, score
    except Exception as exc:
        logger.error("Sentiment analysis error: %s", exc)
        return "neutral", 0.0


def analyze_batch(texts: list[str]) -> list[tuple[str, float]]:
    """Batch sentiment analysis."""
    if not texts:
        return []
    try:
        clf = _load_pipeline()
        results = clf(texts)
        output = []
        for res in results:
            if isinstance(res, list):
                res = res[0]
            output.append((res["label"].lower(), round(res["score"], 4)))
        return output
    except Exception as exc:
        logger.error("Batch sentiment error: %s", exc)
        return [("neutral", 0.0)] * len(texts)
