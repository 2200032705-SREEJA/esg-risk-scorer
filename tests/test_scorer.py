"""Tests for the ESG risk scoring engine."""

from src.models.risk_scorer import score_event, aggregate_daily, risk_label


def test_score_event_negative_high():
    score = score_event("Environmental", 0.95, "negative", 0.90)
    assert 0.3 < score <= 1.0


def test_score_event_positive_low():
    score = score_event("Social", 0.90, "positive", 0.85)
    assert score == 0.0


def test_score_event_neutral_mid():
    score = score_event("Governance", 0.80, "neutral", 0.75)
    assert 0.05 < score < 0.5


def test_score_event_clipped():
    score = score_event("Environmental", 1.0, "negative", 1.0)
    assert 0.0 <= score <= 1.0


def test_score_event_none_label():
    score = score_event("None", 0.99, "negative", 0.99)
    assert score == 0.0


def test_aggregate_daily_basic():
    events = [
        {
            "esg_label": "Environmental",
            "sentiment": "negative",
            "risk_score": 0.38,
        },
        {
            "esg_label": "Social",
            "sentiment": "negative",
            "risk_score": 0.28,
        },
        {
            "esg_label": "Governance",
            "sentiment": "neutral",
            "risk_score": 0.09,
        },
    ]

    result = aggregate_daily(events)

    assert "risk_score" in result
    assert "env_score" in result
    assert "social_score" in result
    assert "gov_score" in result
    assert 0.0 <= result["risk_score"] <= 1.0


def test_aggregate_daily_empty():
    result = aggregate_daily([])
    assert result["risk_score"] == 0.0
    assert result["env_score"] == 0.0
    assert result["social_score"] == 0.0
    assert result["gov_score"] == 0.0


def test_risk_label():
    assert "High" in risk_label(0.65)
    assert "High" in risk_label(0.80)

    assert "Moderate" in risk_label(0.50)
    assert "Moderate" in risk_label(0.40)

    assert "Low" in risk_label(0.39)
    assert "Low" in risk_label(0.20)

    assert "Moderate" not in risk_label(0.65)
    assert "Low" not in risk_label(0.40)