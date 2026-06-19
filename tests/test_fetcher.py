"""Tests for the news fetcher module."""
# import pytest  # not available in this env
from unittest.mock import patch, MagicMock
from src.pipeline.fetcher import fetch_company_news, fetch_all_companies


def test_fetch_returns_empty_without_api_key():
    """Without an API key, fetcher should return empty list gracefully."""
    with patch("src.pipeline.fetcher.NEWS_API_KEY", ""):
        result = fetch_company_news("Tesla")
    assert result == []


def test_fetch_all_companies_no_key():
    with patch("src.pipeline.fetcher.NEWS_API_KEY", ""):
        result = fetch_all_companies(["Apple", "Google"])
    assert result == {"Apple": [], "Google": []}


def test_fetch_company_news_api_error():
    """Network errors should return empty list, not raise."""
    import requests
    with patch("src.pipeline.fetcher.NEWS_API_KEY", "fake_key"):
        with patch("requests.get", side_effect=requests.RequestException("timeout")):
            result = fetch_company_news("Microsoft")
    assert result == []


def test_fetch_company_news_parses_articles():
    """Valid API response should return article list."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "articles": [
            {"title": "Tesla cuts emissions", "description": "Big news",
             "publishedAt": "2024-06-01T10:00:00Z",
             "source": {"name": "Reuters"}, "url": "http://example.com"},
        ]
    }
    mock_resp.raise_for_status = MagicMock()
    with patch("src.pipeline.fetcher.NEWS_API_KEY", "fake_key"):
        with patch("requests.get", return_value=mock_resp):
            result = fetch_company_news("Tesla", lookback_days=7)
    assert len(result) == 1
    assert result[0]["title"] == "Tesla cuts emissions"
