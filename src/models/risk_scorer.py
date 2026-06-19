"""
ESG Risk Scoring Engine.

Combines ESG classification + sentiment into a per-event risk score,
then aggregates to a daily company-level score (0–1 scale).

Risk formula (per event):
    base_risk = sentiment_multiplier (negative=1.0, neutral=0.4, positive=-0.2)
    pillar_weight = ESG_WEIGHTS[esg_label]
    event_risk = clip(base_risk * pillar_weight * esg_confidence * sentiment_confidence, 0, 1)

Daily aggregation:
    Weighted mean of all event risks on that day, clipped to [0, 1].
"""

from __future__ import annotations

import logging
from collections import defaultdict
from datetime import date
from typing import Sequence

import numpy as np

from src.utils.config import ESG_WEIGHTS, SENTIMENT_MULTIPLIERS

logger = logging.getLogger(__name__)


def score_event(
    esg_label: str,
    esg_confidence: float,
    sentiment: str,
    sentiment_confidence: float,
) -> float:
    """
    Compute a single event-level ESG risk score ∈ [0, 1].

    Higher values = higher risk (negative ESG news).
    """
    pillar_weight = ESG_WEIGHTS.get(esg_label, 0.0)
    sentiment_mult = SENTIMENT_MULTIPLIERS.get(sentiment, 0.4)

    raw = sentiment_mult * pillar_weight * esg_confidence * sentiment_confidence
    return float(np.clip(raw, 0.0, 1.0))


def aggregate_daily(
    events: Sequence[dict],
) -> dict[str, float]:
    """
    Given a list of event dicts (keys: esg_label, sentiment, risk_score),
    return a dict with keys:
        risk_score, env_score, social_score, gov_score

    Each pillar score is the mean of event risks for that pillar, or 0 if no events.
    The composite risk_score is the ESG-weight-averaged pillar scores.
    """
    pillar_scores: dict[str, list[float]] = defaultdict(list)

    for ev in events:
        label = ev.get("esg_label", "None")
        risk = float(ev.get("risk_score", 0.0))
        if label in ESG_WEIGHTS:
            pillar_scores[label].append(risk)

    env = float(np.mean(pillar_scores["Environmental"])) if pillar_scores["Environmental"] else 0.0
    soc = float(np.mean(pillar_scores["Social"])) if pillar_scores["Social"] else 0.0
    gov = float(np.mean(pillar_scores["Governance"])) if pillar_scores["Governance"] else 0.0

    composite = (
        ESG_WEIGHTS["Environmental"] * env
        + ESG_WEIGHTS["Social"] * soc
        + ESG_WEIGHTS["Governance"] * gov
    )

    return {
        "risk_score": round(float(np.clip(composite, 0, 1)), 4),
        "env_score": round(env, 4),
        "social_score": round(soc, 4),
        "gov_score": round(gov, 4),
    }


def risk_label(score: float) -> str:
    """Human-readable risk tier for a given score."""
    if score >= 0.65:
        return "🔴 High Risk"
    if score >= 0.4:
        return "🟡 Moderate Risk"
    return "🟢 Low Risk"