"""
ESG Topic Classifier using FinBERT-ESG.

Classifies text into one of:
  - Environmental
  - Social
  - Governance
  - None (not ESG-related)

Model: yiyanghkust/finbert-esg (HuggingFace)
"""

from __future__ import annotations

import logging
from functools import lru_cache

from transformers import pipeline, Pipeline

from src.utils.config import ESG_MODEL_NAME

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _load_pipeline() -> Pipeline:
    logger.info("Loading ESG classifier '%s' …", ESG_MODEL_NAME)
    return pipeline(
        "text-classification",
        model=ESG_MODEL_NAME,
        top_k=1,
        truncation=True,
        max_length=512,
    )


# Label map — FinBERT-ESG returns labels like 'Environmental', 'Social', 'Governance', 'None'
VALID_LABELS = {"Environmental", "Social", "Governance"}


def classify(text: str) -> tuple[str, float]:
    """
    Returns (label, confidence).
    label is one of 'Environmental', 'Social', 'Governance', or 'None'.
    """
    if not text.strip():
        return "None", 0.0
    try:
        clf = _load_pipeline()
        result = clf(text)[0]  # top_k=1 returns list of list
        if isinstance(result, list):
            result = result[0]
        label = result["label"]
        score = round(result["score"], 4)
        return label, score
    except Exception as exc:
        logger.error("ESG classification error: %s", exc)
        return "None", 0.0


def classify_batch(texts: list[str]) -> list[tuple[str, float]]:
    """Classify a batch of texts. More efficient than calling classify() in a loop."""
    if not texts:
        return []
    try:
        clf = _load_pipeline()
        results = clf(texts)
        output = []
        for res in results:
            if isinstance(res, list):
                res = res[0]
            output.append((res["label"], round(res["score"], 4)))
        return output
    except Exception as exc:
        logger.error("Batch ESG classification error: %s", exc)
        return [("None", 0.0)] * len(texts)
