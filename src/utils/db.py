"""
SQLite database helpers for storing ESG events and daily risk scores.
"""

import sqlite3
from pathlib import Path
from datetime import date
from typing import Optional
import pandas as pd

from src.utils.config import DB_PATH


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_db() -> None:
    """Create tables if they don't exist."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS esg_events (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                company     TEXT    NOT NULL,
                date        TEXT    NOT NULL,
                headline    TEXT,
                esg_label   TEXT,
                sentiment   TEXT,
                risk_score  REAL,
                source      TEXT
            );

            CREATE TABLE IF NOT EXISTS daily_risk (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                company       TEXT NOT NULL,
                date          TEXT NOT NULL,
                risk_score    REAL,
                env_score     REAL,
                social_score  REAL,
                gov_score     REAL,
                UNIQUE(company, date)
            );
        """)


def insert_event(company: str, event_date: str, headline: str,
                 esg_label: str, sentiment: str, risk_score: float,
                 source: str = "newsapi") -> None:
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO esg_events
               (company, date, headline, esg_label, sentiment, risk_score, source)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (company, event_date, headline, esg_label, sentiment, risk_score, source)
        )


def upsert_daily_risk(company: str, risk_date: str,
                      risk: float, env: float, soc: float, gov: float) -> None:
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO daily_risk (company, date, risk_score, env_score, social_score, gov_score)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(company, date) DO UPDATE SET
                   risk_score=excluded.risk_score,
                   env_score=excluded.env_score,
                   social_score=excluded.social_score,
                   gov_score=excluded.gov_score""",
            (company, risk_date, risk, env, soc, gov)
        )


def get_daily_risk(company: str, days: int = 30) -> pd.DataFrame:
    query = """
        SELECT date, risk_score, env_score, social_score, gov_score
        FROM daily_risk
        WHERE company = ?
        ORDER BY date DESC
        LIMIT ?
    """
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn, params=(company, days))
    return df.sort_values("date").reset_index(drop=True)


def get_latest_events(company: str, limit: int = 10) -> pd.DataFrame:
    query = """
        SELECT date, headline, esg_label, sentiment, risk_score
        FROM esg_events
        WHERE company = ?
        ORDER BY date DESC, id DESC
        LIMIT ?
    """
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=(company, limit))


def get_company_snapshot() -> pd.DataFrame:
    """Latest risk score per company — for the leaderboard view."""
    query = """
        SELECT company, risk_score, env_score, social_score, gov_score, date
        FROM daily_risk
        WHERE (company, date) IN (
            SELECT company, MAX(date) FROM daily_risk GROUP BY company
        )
        ORDER BY risk_score DESC
    """
    with get_connection() as conn:
        return pd.read_sql_query(query, conn)
