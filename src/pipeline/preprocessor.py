"""
Text preprocessing for ESG news articles and tweets.

Cleans raw text before it's passed to transformer models:
  - Remove URLs, hashtags, mentions, emojis
  - Decode Twitter Snowflake timestamps
  - Tokenize and normalize
"""

import re
import html
from datetime import datetime, timezone


# ── Twitter Snowflake ─────────────────────────────────────────────────────────
TWITTER_EPOCH_MS = 1288834974657  # Nov 4, 2010


def snowflake_to_datetime(snowflake_id: int) -> datetime:
    """Convert a Twitter Snowflake ID to a UTC datetime."""
    ms = (snowflake_id >> 22) + TWITTER_EPOCH_MS
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)


# ── Text Cleaning ─────────────────────────────────────────────────────────────
_URL_RE = re.compile(r"https?://\S+|www\.\S+")
_HASHTAG_RE = re.compile(r"#\w+")
_MENTION_RE = re.compile(r"@\w+")
_EMOJI_RE = re.compile(
    "[\U00010000-\U0010ffff"
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\u2600-\u26FF\u2700-\u27BF]+",
    flags=re.UNICODE,
)
_WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Return a cleaned, normalized string ready for NLP inference."""
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = _URL_RE.sub(" ", text)
    text = _HASHTAG_RE.sub(" ", text)
    text = _MENTION_RE.sub(" ", text)
    text = _EMOJI_RE.sub(" ", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def truncate(text: str, max_tokens: int = 512) -> str:
    """
    Rough word-level truncation so text fits inside BERT's 512-token window.
    Transformer tokenizers split words further, so 400 words is a safe cap.
    """
    words = text.split()
    return " ".join(words[:400])


def preprocess(text: str) -> str:
    return truncate(clean_text(text))
