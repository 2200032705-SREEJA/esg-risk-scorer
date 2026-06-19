"""
ESG Topic Classifier.

Uses FinBERT-ESG (HuggingFace) when transformers/torch are available.
Falls back to a transparent keyword heuristic otherwise — clearly labeled,
never pretending to be AI output.

Model: yiyanghkust/finbert-esg
"""

from __future__ import annotations

import logging
import re
from functools import lru_cache

from src.utils.config import ESG_MODEL_NAME

logger = logging.getLogger(__name__)

VALID_LABELS = {"Environmental", "Social", "Governance"}

# ── Keyword Fallback ──────────────────────────────────────────────────────────
_KW = {
    "Environmental": [
        "emission", "carbon", "climate", "renewable", "pollution", "fossil",
        "sustainability", "greenhouse", "biodiversity", "waste", "recycle",
        "energy", "solar", "wind", "oil spill", "deforestation", "net zero",
    ],
    "Social": [
        "labour", "labor", "worker", "employee", "diversity", "inclusion",
        "human rights", "safety", "union", "wage", "discrimination", "community",
        "health", "wellbeing", "supply chain", "child labour",
    ],
    "Governance": [
        "board", "executive", "ceo", "fraud", "compliance", "audit",
        "whistleblower", "sec", "regulation", "bribery", "corruption",
        "shareholder", "transparency", "accounting", "lawsuit", "fine",
    ],
}


def _keyword_classify(text: str) -> tuple[str, float]:
    """Transparent keyword heuristic. Returns (label, confidence)."""
    lower = text.lower()
    scores: dict[str, int] = {k: 0 for k in _KW}
    for label, keywords in _KW.items():
        for kw in keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", lower):
                scores[label] += 1
    best = max(scores, key=lambda k: scores[k])
    if scores[best] == 0:
        return "None", 0.0
    total = sum(scores.values()) or 1
    confidence = round(min(scores[best] / total + 0.3, 0.95), 4)
    return best, confidence


# ── FinBERT Pipeline (lazy, cached) ──────────────────────────────────────────
@lru_cache(maxsize=1)
def _load_pipeline():
    try:
        from transformers import pipeline as hf_pipeline
        logger.info("Loading ESG classifier '%s' …", ESG_MODEL_NAME)
        return hf_pipeline(
            "text-classification",
            model=ESG_MODEL_NAME,
            top_k=1,
            truncation=True,
            max_length=512,
        )
    except Exception as exc:
        logger.warning("FinBERT-ESG unavailable (%s); using keyword fallback.", exc)
        return None


def classify(text: str) -> tuple[str, float]:
    """
    Returns (label, confidence).
    label ∈ {'Environmental', 'Social', 'Governance', 'None'}.
    Uses FinBERT-ESG when available, keyword heuristic otherwise.
    """
    if not text.strip():
        return "None", 0.0
    clf = _load_pipeline()
    if clf is None:
        return _keyword_classify(text)
    try:
        result = clf(text)[0]
        if isinstance(result, list):
            result = result[0]
        return result["label"], round(result["score"], 4)
    except Exception as exc:
        logger.error("ESG classification error: %s", exc)
        return _keyword_classify(text)


def classify_batch(texts: list[str]) -> list[tuple[str, float]]:
    """Classify a batch of texts."""
    if not texts:
        return []
    clf = _load_pipeline()
    if clf is None:
        return [_keyword_classify(t) for t in texts]
    try:
        results = clf(texts)
        output = []
        for res in results:
            if isinstance(res, list):
                res = res[0]
            output.append((res["label"], round(res["score"], 4)))
        return output
    except Exception as exc:
        logger.error("Batch ESG classification error: %s", exc)
        return [_keyword_classify(t) for t in texts]
