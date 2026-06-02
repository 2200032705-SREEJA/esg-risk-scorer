"""
ESG Risk Scoring Dashboard — Streamlit App

Launches automatically by running:
    streamlit run src/dashboard/app.py

On every launch the ingestion pipeline runs to pull fresh news.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# ── Path fix so imports work from any CWD ────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.utils.config import COMPANIES
from src.utils.db import (
    initialize_db,
    get_daily_risk,
    get_latest_events,
    get_company_snapshot,
)
from src.models.risk_scorer import risk_label

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ESG Risk Monitor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        color: white;
        text-align: center;
    }
    .metric-title { font-size: 0.85rem; opacity: 0.7; text-transform: uppercase; }
    .metric-value { font-size: 2.2rem; font-weight: 700; margin: 0.2rem 0; }
    .metric-label { font-size: 0.9rem; }
    .event-row { border-left: 4px solid; padding: 0.4rem 0.8rem; margin: 0.4rem 0; border-radius: 0 8px 8px 0; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

PILLAR_COLORS = {
    "Environmental": "#2ecc71",
    "Social": "#3498db",
    "Governance": "#9b59b6",
}

SENTIMENT_ICONS = {
    "negative": "⚠️",
    "neutral": "➖",
    "positive": "✅",
}


def forecast_risk(df: pd.DataFrame, horizon: int = 7) -> pd.DataFrame:
    """Simple linear regression forecast for next `horizon` days."""
    if len(df) < 3:
        return pd.DataFrame()
    X = np.arange(len(df)).reshape(-1, 1)
    y = df["risk_score"].values
    model = LinearRegression().fit(X, y)
    future_X = np.arange(len(df), len(df) + horizon).reshape(-1, 1)
    preds = np.clip(model.predict(future_X), 0, 1)

    last_date = pd.to_datetime(df["date"].iloc[-1])
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=horizon)
    return pd.DataFrame({"date": future_dates.strftime("%Y-%m-%d"), "risk_score": preds})


def risk_color(score: float) -> str:
    if score >= 0.7:
        return "#e74c3c"
    if score >= 0.4:
        return "#f39c12"
    return "#2ecc71"


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/leaf.png", width=60)
    st.title("🌿 ESG Risk Monitor")
    st.markdown("---")

    selected_company = st.selectbox("Select Company", COMPANIES, index=0)

    st.markdown("---")
    if st.button("🔄 Refresh Data", use_container_width=True):
        with st.spinner("Running ESG pipeline…"):
            try:
                from src.pipeline.ingestion import run_pipeline
                run_pipeline(companies=[selected_company])
                st.success("Data refreshed!")
            except Exception as exc:
                st.error(f"Pipeline error: {exc}")

    st.markdown("---")
    st.caption("Powered by FinBERT-ESG · NewsAPI · Streamlit")


# ── Main Content ──────────────────────────────────────────────────────────────

initialize_db()
df_risk = get_daily_risk(selected_company, days=30)
df_events = get_latest_events(selected_company, limit=10)

st.title(f"ESG Risk Analysis — {selected_company}")

# ── Key Metrics ───────────────────────────────────────────────────────────────

latest = df_risk.iloc[-1] if not df_risk.empty else None
col1, col2, col3, col4 = st.columns(4)

def metric_card(col, title: str, value: str, label: str = "", color: str = "#2ecc71"):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value" style="color:{color}">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

if latest is not None:
    score = latest["risk_score"]
    metric_card(col1, "Composite Risk", f"{score:.2f}", risk_label(score), risk_color(score))
    metric_card(col2, "🌱 Environmental", f"{latest['env_score']:.2f}", "", "#2ecc71")
    metric_card(col3, "🤝 Social", f"{latest['social_score']:.2f}", "", "#3498db")
    metric_card(col4, "⚖️ Governance", f"{latest['gov_score']:.2f}", "", "#9b59b6")
else:
    st.info("No risk data yet. Click **Refresh Data** to fetch the latest ESG news.")

st.markdown("<br>", unsafe_allow_html=True)

# ── Trend Chart ───────────────────────────────────────────────────────────────

if not df_risk.empty:
    st.subheader("30-Day Risk Trend + 7-Day Forecast")
    df_forecast = forecast_risk(df_risk)

    fig = go.Figure()

    # Historical
    fig.add_trace(go.Scatter(
        x=df_risk["date"], y=df_risk["risk_score"],
        name="Historical Risk",
        line=dict(color="#3498db", width=2.5),
        mode="lines+markers",
        marker=dict(size=5),
    ))

    # Pillar breakdown (area)
    for pillar, col_name, color in [
        ("Environmental", "env_score", "#2ecc71"),
        ("Social", "social_score", "#3498db"),
        ("Governance", "gov_score", "#9b59b6"),
    ]:
        fig.add_trace(go.Scatter(
            x=df_risk["date"], y=df_risk[col_name],
            name=pillar, line=dict(color=color, dash="dot"),
            opacity=0.5,
        ))

    # Forecast
    if not df_forecast.empty:
        fig.add_trace(go.Scatter(
            x=df_forecast["date"], y=df_forecast["risk_score"],
            name="7-Day Forecast",
            line=dict(color="#e74c3c", dash="dash", width=2),
            mode="lines",
        ))
        fig.add_vrect(
            x0=df_forecast["date"].iloc[0],
            x1=df_forecast["date"].iloc[-1],
            fillcolor="rgba(231, 76, 60, 0.05)",
            line_width=0,
            annotation_text="Forecast",
        )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Risk Score (0–1)",
        yaxis=dict(range=[0, 1]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Pillar Breakdown Bar ──────────────────────────────────────────────────────

if latest is not None:
    st.subheader("ESG Pillar Breakdown")
    pillars = pd.DataFrame({
        "Pillar": ["Environmental", "Social", "Governance"],
        "Score": [latest["env_score"], latest["social_score"], latest["gov_score"]],
        "Color": ["#2ecc71", "#3498db", "#9b59b6"],
    })
    fig2 = px.bar(
        pillars, x="Score", y="Pillar", orientation="h",
        color="Pillar",
        color_discrete_map={p: c for p, c in zip(pillars["Pillar"], pillars["Color"])},
        range_x=[0, 1],
    )
    fig2.update_layout(
        showlegend=False, height=220,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Recent ESG Events ─────────────────────────────────────────────────────────

st.subheader("Recent ESG Events")
if not df_events.empty:
    for _, row in df_events.iterrows():
        icon = SENTIMENT_ICONS.get(row["sentiment"], "➖")
        color = PILLAR_COLORS.get(row["esg_label"], "#aaa")
        st.markdown(f"""
        <div class="event-row" style="border-color:{color}">
            {icon} <strong>[{row['esg_label']}]</strong> {row['headline'][:120]}…
            &nbsp;&nbsp;<code>{row['date']}</code>
            &nbsp;&nbsp;Risk: <strong>{row['risk_score']:.3f}</strong>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No events found. Refresh to fetch the latest news.")

# ── Company Leaderboard ───────────────────────────────────────────────────────

st.markdown("---")
st.subheader("📊 Company ESG Risk Leaderboard")

df_snap = get_company_snapshot()
if not df_snap.empty:
    df_snap["Risk Level"] = df_snap["risk_score"].apply(risk_label)
    df_snap_display = df_snap[["company", "risk_score", "env_score", "social_score", "gov_score", "Risk Level", "date"]]
    df_snap_display.columns = ["Company", "Risk Score", "Environmental", "Social", "Governance", "Risk Level", "Last Updated"]

    fig3 = px.bar(
        df_snap.head(20), x="company", y="risk_score",
        color="risk_score",
        color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"],
        range_color=[0, 1],
        labels={"risk_score": "Risk Score", "company": "Company"},
    )
    fig3.update_layout(
        height=350,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.dataframe(df_snap_display, use_container_width=True, hide_index=True)
else:
    st.info("Leaderboard will populate after running the pipeline for all companies.")
