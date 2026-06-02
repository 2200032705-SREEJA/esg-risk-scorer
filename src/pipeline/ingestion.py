"""
End-to-end pipeline ingestion.

Called automatically when the Streamlit dashboard launches.
Flow:
    1. Fetch news for all companies (NewsAPI)
    2. Preprocess text
    3. Classify ESG label (FinBERT-ESG)
    4. Detect sentiment (FinBERT Sentiment)
    5. Score each event
    6. Aggregate to daily risk scores
    7. Persist everything to SQLite
"""

from __future__ import annotations

import logging
from datetime import date

from src.pipeline.fetcher import fetch_all_companies
from src.pipeline.preprocessor import preprocess
from src.models.esg_classifier import classify_batch
from src.models.sentiment import analyze_batch
from src.models.risk_scorer import score_event, aggregate_daily
from src.utils.db import initialize_db, insert_event, upsert_daily_risk
from src.utils.config import COMPANIES, LOOKBACK_DAYS

logger = logging.getLogger(__name__)


def run_pipeline(
    companies: list[str] | None = None,
    lookback_days: int = LOOKBACK_DAYS,
    verbose: bool = True,
) -> None:
    """
    Run the full ESG ingestion pipeline.

    Args:
        companies: Override the default company list.
        lookback_days: How many days back to fetch news.
        verbose: Log progress to stdout.
    """
    initialize_db()
    companies = companies or COMPANIES
    today = date.today().isoformat()

    if verbose:
        logger.info("Starting ESG pipeline for %d companies …", len(companies))

    all_news = fetch_all_companies(companies, lookback_days)

    for company, articles in all_news.items():
        if not articles:
            continue

        # ── Preprocess ────────────────────────────────────────────────────────
        headlines = [
            preprocess((a.get("title") or "") + " " + (a.get("description") or ""))
            for a in articles
        ]
        published_dates = [
            (a.get("publishedAt") or today)[:10]  # ISO date slice
            for a in articles
        ]

        # ── Classify & Score ──────────────────────────────────────────────────
        esg_results = classify_batch(headlines)
        sentiment_results = analyze_batch(headlines)

        day_events: list[dict] = []

        for i, article in enumerate(articles):
            esg_label, esg_conf = esg_results[i]
            sentiment, sent_conf = sentiment_results[i]

            if esg_label == "None":
                continue  # Skip non-ESG content

            risk = score_event(esg_label, esg_conf, sentiment, sent_conf)

            event = {
                "esg_label": esg_label,
                "sentiment": sentiment,
                "risk_score": risk,
            }
            day_events.append(event)

            insert_event(
                company=company,
                event_date=published_dates[i],
                headline=article.get("title", ""),
                esg_label=esg_label,
                sentiment=sentiment,
                risk_score=risk,
                source=article.get("source", {}).get("name", "newsapi"),
            )

        # ── Aggregate Daily Score ─────────────────────────────────────────────
        if day_events:
            scores = aggregate_daily(day_events)
            upsert_daily_risk(
                company=company,
                risk_date=today,
                risk=scores["risk_score"],
                env=scores["env_score"],
                soc=scores["social_score"],
                gov=scores["gov_score"],
            )
            if verbose:
                logger.info(
                    "%-20s | risk=%.3f  E=%.3f  S=%.3f  G=%.3f",
                    company, scores["risk_score"],
                    scores["env_score"], scores["social_score"], scores["gov_score"],
                )

    if verbose:
        logger.info("Pipeline complete.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    run_pipeline()
