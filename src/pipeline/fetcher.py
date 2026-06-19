"""
News fetcher — retrieves ESG-relevant articles for each company via NewsAPI.

Usage:
    from src.pipeline.fetcher import fetch_company_news
    articles = fetch_company_news("Tesla", lookback_days=7)
"""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any

import requests

from src.utils.config import NEWS_API_KEY, LOOKBACK_DAYS, MAX_ARTICLES_PER_COMPANY

logger = logging.getLogger(__name__)

_ESG_KEYWORDS = "ESG OR sustainability OR environment OR emissions OR governance OR labour OR compliance"
_BASE_URL = "https://newsapi.org/v2/everything"


def _build_query(company: str) -> str:
    return f'"{company}" AND ({_ESG_KEYWORDS})'


def fetch_company_news(
    company: str,
    lookback_days: int = LOOKBACK_DAYS,
    page_size: int = MAX_ARTICLES_PER_COMPANY,
) -> list[dict[str, Any]]:
    """
    Fetch recent ESG-related news articles for a company.

    Returns a list of dicts with keys: title, description, publishedAt, source, url.
    Returns an empty list if the API key is missing or the request fails.
    """
    if not NEWS_API_KEY:
        logger.warning("NEWS_API_KEY not set — returning empty article list.")
        return []

    from_date = (date.today() - timedelta(days=lookback_days)).isoformat()

    params = {
        "q": _build_query(company),
        "from": from_date,
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "language": "en",
        "apiKey": NEWS_API_KEY,
    }

    try:
        resp = requests.get(_BASE_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("articles", [])
        logger.info("Fetched %d articles for '%s'", len(articles), company)
        return articles
    except requests.RequestException as exc:
        logger.error("NewsAPI error for '%s': %s", company, exc)
        return []


def fetch_all_companies(
    companies: list[str],
    lookback_days: int = LOOKBACK_DAYS,
) -> dict[str, list[dict[str, Any]]]:
    """Fetch news for every company. Returns {company: [articles]}."""
    results: dict[str, list[dict[str, Any]]] = {}
    for company in companies:
        results[company] = fetch_company_news(company, lookback_days)
    return results
