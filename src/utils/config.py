"""
Central configuration for the ESG Risk Scoring System.
All settings are loaded from environment variables (.env file).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT_DIR / "data" / "raw"
DATA_PROCESSED = ROOT_DIR / "data" / "processed"
DB_PATH = ROOT_DIR / os.getenv("DB_PATH", "data/esg_events.db")

# ── API Keys ─────────────────────────────────────────────────────────────────
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# ── Pipeline Settings ─────────────────────────────────────────────────────────
LOOKBACK_DAYS = int(os.getenv("LOOKBACK_DAYS", 7))
MAX_ARTICLES_PER_COMPANY = 20

# ── NLP Model IDs ─────────────────────────────────────────────────────────────
ESG_MODEL_NAME = "yiyanghkust/finbert-esg"
SENTIMENT_MODEL_NAME = "ProsusAI/finbert"

# ── Risk Scoring ──────────────────────────────────────────────────────────────
# Weights for E, S, G pillars in the composite risk score
ESG_WEIGHTS = {"Environmental": 0.4, "Social": 0.3, "Governance": 0.3}

# Sentiment → risk multiplier  (negative events carry more weight;
# positive news actively reduces risk — clipped to 0 after multiplication)
SENTIMENT_MULTIPLIERS = {"negative": 1.0, "neutral": 0.4, "positive": -0.2}

# ── Companies to Monitor ──────────────────────────────────────────────────────
COMPANIES = [
    "Apple", "Microsoft", "Amazon", "Tesla", "Google",
    "Meta", "Walmart", "ExxonMobil", "Chevron", "JPMorgan",
    "Bank of America", "Goldman Sachs", "Nike", "Coca-Cola", "PepsiCo",
    "McDonald's", "Starbucks", "Ford", "General Motors", "Boeing",
    "3M", "Johnson & Johnson", "Pfizer", "Moderna", "AstraZeneca",
    "Shell", "BP", "TotalEnergies", "Nestlé", "Unilever",
    "Adidas", "H&M", "Zara", "Samsung", "Sony",
    "Netflix", "Spotify", "Uber", "Lyft", "Airbnb",
    "Twitter", "Snap", "Pinterest", "Shopify", "Salesforce",
    "Oracle", "IBM", "Intel", "AMD", "Nvidia",
]