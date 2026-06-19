"""
End-to-end pipeline ingestion.

Flow:
    1. Fetch news for all companies (NewsAPI) — OR load from seed dataset
    2. Preprocess text
    3. Classify ESG label (FinBERT-ESG or keyword fallback)
    4. Detect sentiment (FinBERT or keyword fallback)
    5. Score each event
    6. Aggregate to daily risk scores per company per date
    7. Persist everything to SQLite
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any

from src.pipeline.fetcher import fetch_all_companies
from src.pipeline.preprocessor import preprocess
from src.models.esg_classifier import classify_batch
from src.models.sentiment import analyze_batch
from src.models.risk_scorer import score_event, aggregate_daily
from src.utils.db import initialize_db, insert_event, upsert_daily_risk
from src.utils.config import COMPANIES, LOOKBACK_DAYS, NEWS_API_KEY

logger = logging.getLogger(__name__)


def _load_seed_articles() -> dict[str, list[dict[str, Any]]]:
    """Return seed articles grouped by company."""
    from src.data.seed_data import SEED_ARTICLES
    grouped: dict[str, list[dict]] = defaultdict(list)
    for art in SEED_ARTICLES:
        company = art["company"]
        grouped[company].append({
            "title": art["title"],
            "description": "",
            "publishedAt": art["publishedAt"],
            "source": {"name": art.get("source", "seed")},
        })
    return dict(grouped)


def run_pipeline(
    companies: list[str] | None = None,
    lookback_days: int = LOOKBACK_DAYS,
    verbose: bool = True,
) -> None:
    """
    Run the full ESG ingestion pipeline.
    Uses NewsAPI when NEWS_API_KEY is set, offline seed data otherwise.
    """
    initialize_db()
    companies = companies or COMPANIES

    if verbose:
        logger.info("Starting ESG pipeline for %d companies …", len(companies))

    # ── Fetch or load ──────────────────────────────────────────────────────────
    if NEWS_API_KEY:
        all_news = fetch_all_companies(companies, lookback_days)
        logger.info("Using live NewsAPI data.")
    else:
        all_news = _load_seed_articles()
        logger.info("No NEWS_API_KEY — using offline seed dataset.")

    for company, articles in all_news.items():
        if not articles:
            continue

        # Group by published date so historical spread is preserved
        date_articles: dict[str, list[dict]] = defaultdict(list)
        for art in articles:
            pub_date = (art.get("publishedAt") or "")[:10]
            date_articles[pub_date].append(art)

        for pub_date, day_articles in date_articles.items():
            headlines = [
                preprocess((a.get("title") or "") + " " + (a.get("description") or ""))
                for a in day_articles
            ]

            esg_results = classify_batch(headlines)
            sentiment_results = analyze_batch(headlines)

            day_events: list[dict] = []

            for i, article in enumerate(day_articles):
                esg_label, esg_conf = esg_results[i]
                sentiment, sent_conf = sentiment_results[i]

                if esg_label == "None":
                    continue

                risk = score_event(esg_label, esg_conf, sentiment, sent_conf)

                day_events.append({"esg_label": esg_label, "sentiment": sentiment, "risk_score": risk})

                insert_event(
                    company=company,
                    event_date=pub_date,
                    headline=article.get("title", ""),
                    esg_label=esg_label,
                    sentiment=sentiment,
                    risk_score=risk,
                    source=article.get("source", {}).get("name", "seed"),
                )

            if day_events:
                scores = aggregate_daily(day_events)
                upsert_daily_risk(
                    company=company,
                    risk_date=pub_date,
                    risk=scores["risk_score"],
                    env=scores["env_score"],
                    soc=scores["social_score"],
                    gov=scores["gov_score"],
                )
                if verbose:
                    logger.info(
                        "%-20s | %s | risk=%.3f  E=%.3f  S=%.3f  G=%.3f",
                        company, pub_date,
                        scores["risk_score"], scores["env_score"],
                        scores["social_score"], scores["gov_score"],
                    )

    if verbose:
        logger.info("Pipeline complete.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    run_pipeline()
