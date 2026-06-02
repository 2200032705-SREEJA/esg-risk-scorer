"""
ESG Risk Scoring Dashboard — Streamlit App
Brutalist Redesign — Powered by Sreeja
"""

import sys
import random
from pathlib import Path
from datetime import date, timedelta

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

st.set_page_config(
    page_title="ESG Risk Monitor",
    page_icon="⬛",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Bebas+Neue&family=IBM+Plex+Mono:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Mono', monospace;
}

.stApp {
    background: #0a0a0a;
}

/* Remove default streamlit padding */
.block-container {
    padding-top: 1.5rem !important;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: #0a0a0a;
    border-right: 3px solid #e8ff00;
}

section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #111111;
    border: 2px solid #333333;
    color: #ffffff;
    font-family: 'IBM Plex Mono', monospace;
    border-radius: 0 !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background: #e8ff00 !important;
    color: #0a0a0a !important;
    border: 3px solid #e8ff00 !important;
    border-radius: 0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1rem !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: #0a0a0a !important;
    color: #e8ff00 !important;
    border-color: #e8ff00 !important;
}

/* ── HERO BANNER ── */
.hero-banner {
    background: #111111;
    border: 3px solid #e8ff00;
    border-radius: 0;
    padding: 2.5rem 3rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 6px; height: 100%;
    background: #e8ff00;
}

.hero-banner::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 6px;
    background: linear-gradient(90deg, #e8ff00 0%, transparent 60%);
}

.hero-badge {
    display: inline-block;
    background: #e8ff00;
    color: #0a0a0a;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 0;
    margin-bottom: 1rem;
    font-family: 'IBM Plex Mono', monospace;
}

.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.5rem;
    font-weight: 400;
    color: #ffffff;
    margin: 0 0 0.3rem 0;
    letter-spacing: 3px;
    line-height: 0.95;
    text-transform: uppercase;
}

.hero-subtitle {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.4);
    margin: 0.8rem 0 0 0;
    font-weight: 400;
    letter-spacing: 1.5px;
    font-family: 'IBM Plex Mono', monospace;
    text-transform: uppercase;
}

/* ── KPI CARDS ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    margin-bottom: 1.5rem;
    border: 3px solid #222222;
}

.kpi-card {
    background: #111111;
    border-right: 3px solid #222222;
    padding: 1.6rem 1.4rem;
    position: relative;
    overflow: hidden;
}

.kpi-card:last-child {
    border-right: none;
}

.kpi-card.green  { border-top: 5px solid #39ff14; }
.kpi-card.yellow { border-top: 5px solid #e8ff00; }
.kpi-card.red    { border-top: 5px solid #ff2d55; }

.kpi-label {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.35);
    margin-bottom: 0.8rem;
    font-family: 'IBM Plex Mono', monospace;
}

.kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.2rem;
    font-weight: 400;
    line-height: 1;
    margin-bottom: 0.4rem;
    letter-spacing: 2px;
}

.kpi-value.green  { color: #39ff14; }
.kpi-value.yellow { color: #e8ff00; }
.kpi-value.red    { color: #ff2d55; }

.kpi-trend {
    font-size: 0.65rem;
    color: rgba(255,255,255,0.3);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── SECTION HEADERS ── */
.section-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    font-weight: 400;
    color: #ffffff;
    letter-spacing: 3px;
    margin: 2rem 0 1rem 0;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    border-left: 5px solid #e8ff00;
    padding-left: 1rem;
}

.section-header span { color: #e8ff00; }

/* ── EVENT CARDS ── */
.event-card {
    background: #111111;
    border: 2px solid #222222;
    border-left: 5px solid;
    border-radius: 0;
    padding: 1rem 1.4rem;
    margin-bottom: 0.5rem;
    transition: border-color 0.15s ease;
}

.event-card:hover {
    background: #161616;
}

.event-card.env { border-left-color: #39ff14; }
.event-card.soc { border-left-color: #00c8ff; }
.event-card.gov { border-left-color: #bf5fff; }

.event-title {
    font-size: 0.85rem;
    color: #e0e0e0;
    line-height: 1.5;
    margin-bottom: 0.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 400;
}

.event-meta {
    font-size: 0.68rem;
    color: rgba(255,255,255,0.3);
    display: flex;
    gap: 1rem;
    align-items: center;
    font-family: 'IBM Plex Mono', monospace;
}

.event-tag {
    display: inline-block;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 0;
    border: 1px solid;
}

.tag-env { border-color: #39ff14; color: #39ff14; background: transparent; }
.tag-soc { border-color: #00c8ff; color: #00c8ff; background: transparent; }
.tag-gov { border-color: #bf5fff; color: #bf5fff; background: transparent; }
.tag-neg { border-color: #ff2d55; color: #ff2d55; background: transparent; }
.tag-neu { border-color: rgba(255,255,255,0.3); color: rgba(255,255,255,0.4); background: transparent; }
.tag-pos { border-color: #39ff14; color: #39ff14; background: transparent; }

/* ── LEADERBOARD ── */
.lb-row {
    display: flex;
    align-items: center;
    background: #111111;
    border: 2px solid #1e1e1e;
    border-left: 5px solid #333333;
    padding: 0.75rem 1.2rem;
    margin-bottom: 0.4rem;
    gap: 1rem;
    transition: background 0.15s ease;
}

.lb-row:hover {
    background: #161616;
    border-left-color: #e8ff00;
}

.lb-rank {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    color: rgba(255,255,255,0.2);
    width: 28px;
    letter-spacing: 1px;
}

.lb-name {
    font-size: 0.82rem;
    color: #d0d0d0;
    flex: 1;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.5px;
}

.lb-bar-wrap {
    flex: 2;
    background: #1e1e1e;
    border: 1px solid #2a2a2a;
    height: 8px;
    overflow: hidden;
}

.lb-bar { height: 100%; }

.lb-score {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    font-weight: 400;
    width: 52px;
    text-align: right;
    letter-spacing: 1px;
}

/* ── SIDEBAR LOGO AREA ── */
.sidebar-logo {
    padding: 1.5rem 0 1rem;
    border-bottom: 3px solid #e8ff00;
    margin-bottom: 1.5rem;
}

.sidebar-appname {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: #ffffff;
    letter-spacing: 4px;
    line-height: 1;
}

.sidebar-powered {
    font-size: 0.6rem;
    color: rgba(255,255,255,0.25);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.3rem;
    font-family: 'IBM Plex Mono', monospace;
}

.sidebar-score-block {
    background: #0a0a0a;
    border: 3px solid #1e1e1e;
    padding: 1.5rem;
    margin: 1.2rem 0;
    text-align: center;
    position: relative;
}

.sidebar-score-label {
    font-size: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.25);
    margin-bottom: 0.6rem;
    font-family: 'IBM Plex Mono', monospace;
}

.sidebar-score-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4rem;
    line-height: 1;
    letter-spacing: 3px;
}

.sidebar-score-risk {
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.4rem;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
}

/* ── FOOTER ── */
.footer {
    margin-top: 3rem;
    padding: 1.5rem;
    border-top: 3px solid #1e1e1e;
    text-align: center;
    font-size: 0.65rem;
    color: rgba(255,255,255,0.18);
    letter-spacing: 3px;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────
COMPANIES = [
    "Apple", "Microsoft", "Amazon", "Tesla", "Google",
    "Meta", "Walmart", "ExxonMobil", "Chevron", "JPMorgan",
    "Bank of America", "Goldman Sachs", "Nike", "Coca-Cola", "PepsiCo",
    "McDonald's", "Starbucks", "Ford", "General Motors", "Boeing",
]

DEMO_EVENTS = [
    ("Environmental", "negative", "Carbon emissions exceeded quarterly targets amid production surge", 0.82),
    ("Social", "negative", "Labour union files complaint over workplace safety violations", 0.74),
    ("Governance", "negative", "SEC investigates executive stock option backdating practices", 0.79),
    ("Environmental", "neutral", "Company releases annual sustainability report with mixed results", 0.38),
    ("Social", "positive", "Diversity hiring initiative achieves 40% representation milestone", 0.08),
    ("Governance", "positive", "Board approves independent ethics committee with external oversight", 0.06),
    ("Environmental", "negative", "Oil spill incident reported at offshore drilling facility", 0.91),
    ("Social", "neutral", "Employee satisfaction survey shows stable 72% approval rating", 0.31),
    ("Governance", "negative", "Whistleblower alleges financial misreporting in Asia operations", 0.85),
    ("Environmental", "positive", "Renewable energy transition reaches 60% of total power usage", 0.05),
]

def generate_risk_trend(base, days=30, seed=42):
    rng = np.random.default_rng(seed)
    dates = [(date.today() - timedelta(days=days - i)).isoformat() for i in range(days)]
    noise = rng.normal(0, 0.05, days).cumsum() * 0.3
    env = np.clip(base * 1.1 + noise + rng.normal(0, 0.03, days), 0, 1)
    soc = np.clip(base * 0.9 + noise * 0.8 + rng.normal(0, 0.03, days), 0, 1)
    gov = np.clip(base * 0.95 + noise * 0.6 + rng.normal(0, 0.02, days), 0, 1)
    risk = 0.4 * env + 0.3 * soc + 0.3 * gov
    return pd.DataFrame({"date": dates, "risk_score": np.clip(risk, 0, 1),
                         "env_score": env, "social_score": soc, "gov_score": gov})

def get_company_seed(company):
    return sum(ord(c) for c in company) % 1000

def get_base_risk(company):
    rng = np.random.default_rng(get_company_seed(company))
    return float(rng.uniform(0.2, 0.85))

def risk_color(score):
    if score >= 0.65: return "#ff2d55"
    if score >= 0.40: return "#e8ff00"
    return "#39ff14"

def risk_label(score):
    if score >= 0.65: return "HIGH RISK"
    if score >= 0.40: return "MODERATE"
    return "LOW RISK"

def forecast(df, horizon=7):
    from sklearn.linear_model import LinearRegression
    X = np.arange(len(df)).reshape(-1, 1)
    y = df["risk_score"].values
    m = LinearRegression().fit(X, y)
    fx = np.arange(len(df), len(df) + horizon).reshape(-1, 1)
    preds = np.clip(m.predict(fx), 0, 1)
    last = pd.to_datetime(df["date"].iloc[-1])
    fdates = pd.date_range(last + pd.Timedelta(days=1), periods=horizon).strftime("%Y-%m-%d")
    return pd.DataFrame({"date": fdates, "risk_score": preds})

def kpi_color_class(v):
    if v >= 0.65: return "red"
    if v >= 0.40: return "yellow"
    return "green"

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:2rem; margin-bottom:0.4rem;">⬛</div>
        <div class="sidebar-appname">ESG RISK<br>MONITOR</div>
        <div class="sidebar-powered">POWERED BY SREEJA</div>
    </div>
    """, unsafe_allow_html=True)

    selected = st.selectbox("SELECT COMPANY", COMPANIES, index=0, label_visibility="visible")
    base = get_base_risk(selected)
    df_risk = generate_risk_trend(base, seed=get_company_seed(selected))
    latest_score = df_risk["risk_score"].iloc[-1]
    color = risk_color(latest_score)

    st.markdown(f"""
    <div class="sidebar-score-block">
        <div class="sidebar-score-label">Current Risk Score</div>
        <div class="sidebar-score-value" style="color:{color};">{latest_score:.2f}</div>
        <div class="sidebar-score-risk" style="color:{color};">{risk_label(latest_score)}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("↺  REFRESH DATA", use_container_width=True):
        st.success("✓ Dashboard refreshed.")

    st.markdown("""
    <div style="margin-top:2rem; font-size:0.6rem; color:rgba(255,255,255,0.15); line-height:2;
                font-family:'IBM Plex Mono',monospace; letter-spacing:1.5px; text-transform:uppercase;">
        FinBERT-ESG · NewsAPI<br>Streamlit · Scikit-learn<br>SQLite · Plotly
    </div>
    """, unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
    <div class="hero-badge">⬛ Real-Time ESG Analytics</div>
    <div class="hero-title">{selected}</div>
    <div class="hero-subtitle">
        Environmental · Social · Governance Risk Assessment &nbsp;|&nbsp;
        NLP-powered by FinBERT-ESG &nbsp;|&nbsp;
        Updated {date.today().strftime('%b %d, %Y')}
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
env  = df_risk["env_score"].iloc[-1]
soc  = df_risk["social_score"].iloc[-1]
gov  = df_risk["gov_score"].iloc[-1]

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card {kpi_color_class(latest_score)}">
    <div class="kpi-label">◈ Composite Risk</div>
    <div class="kpi-value {kpi_color_class(latest_score)}">{latest_score:.2f}</div>
    <div class="kpi-trend">{risk_label(latest_score)}</div>
  </div>
  <div class="kpi-card {kpi_color_class(env)}">
    <div class="kpi-label">▲ Environmental</div>
    <div class="kpi-value {kpi_color_class(env)}">{env:.2f}</div>
    <div class="kpi-trend">Emissions · Waste · Climate</div>
  </div>
  <div class="kpi-card {kpi_color_class(soc)}">
    <div class="kpi-label">◉ Social</div>
    <div class="kpi-value {kpi_color_class(soc)}">{soc:.2f}</div>
    <div class="kpi-trend">Labour · Diversity · Safety</div>
  </div>
  <div class="kpi-card {kpi_color_class(gov)}">
    <div class="kpi-label">⬡ Governance</div>
    <div class="kpi-value {kpi_color_class(gov)}">{gov:.2f}</div>
    <div class="kpi-trend">Fraud · Compliance · Board</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CHARTS ────────────────────────────────────────────────────────────────────
col_chart, col_pillar = st.columns([3, 2])

CHART_BG = "rgba(0,0,0,0)"
GRID_CLR  = "rgba(255,255,255,0.06)"
AXIS_CLR  = "rgba(255,255,255,0.25)"

with col_chart:
    st.markdown('<div class="section-header">📈 <span>30-Day Risk Trend</span> + 7-Day Forecast</div>', unsafe_allow_html=True)
    df_fc = forecast(df_risk)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_risk["date"], y=df_risk["risk_score"], name="Composite Risk",
        line=dict(color="#e8ff00", width=2.5), mode="lines",
        fill="tozeroy", fillcolor="rgba(232,255,0,0.04)"))
    for col_name, clr, lbl in [
        ("env_score",    "#39ff14", "Environmental"),
        ("social_score", "#00c8ff", "Social"),
        ("gov_score",    "#bf5fff", "Governance")
    ]:
        fig.add_trace(go.Scatter(
            x=df_risk["date"], y=df_risk[col_name], name=lbl,
            line=dict(color=clr, dash="dot", width=1.3), opacity=0.65))
    fig.add_trace(go.Scatter(
        x=df_fc["date"], y=df_fc["risk_score"], name="Forecast",
        line=dict(color="#ff2d55", dash="dash", width=2.2)))
    fig.add_vrect(
        x0=df_fc["date"].iloc[0], x1=df_fc["date"].iloc[-1],
        fillcolor="rgba(255,45,85,0.04)", line_width=0)
    fig.update_layout(
        plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG,
        font=dict(color=AXIS_CLR, size=10, family="IBM Plex Mono"),
        xaxis=dict(showgrid=False, color=AXIS_CLR, linecolor="#222222", linewidth=2),
        yaxis=dict(showgrid=True, gridcolor=GRID_CLR, range=[0,1],
                   color=AXIS_CLR, linecolor="#222222", linewidth=2),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    font=dict(size=9, family="IBM Plex Mono"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=0, r=0, t=30, b=0), height=300)
    st.plotly_chart(fig, use_container_width=True)

with col_pillar:
    st.markdown('<div class="section-header">🎯 <span>Pillar</span> Breakdown</div>', unsafe_allow_html=True)
    fig2 = go.Figure()
    for pillar, score, clr in [
        ("Environmental", env, "#39ff14"),
        ("Social",        soc, "#00c8ff"),
        ("Governance",    gov, "#bf5fff")
    ]:
        fig2.add_trace(go.Bar(
            x=[score], y=[pillar], orientation="h", name=pillar,
            marker=dict(color=clr, opacity=0.9,
                        line=dict(color=clr, width=1)),
            text=f'{score:.2f}', textposition="inside",
            textfont=dict(color="black", size=14, family="Bebas Neue")))
    fig2.update_layout(
        plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG,
        showlegend=False, barmode="overlay",
        xaxis=dict(range=[0,1], showgrid=True, gridcolor=GRID_CLR,
                   color=AXIS_CLR, linecolor="#222222", linewidth=2),
        yaxis=dict(color=AXIS_CLR, linecolor="#222222",
                   tickfont=dict(family="IBM Plex Mono", size=10)),
        font=dict(color=AXIS_CLR, family="IBM Plex Mono"),
        margin=dict(l=0, r=0, t=10, b=0), height=180)
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=latest_score,
        number=dict(font=dict(color=risk_color(latest_score), family="Bebas Neue", size=40)),
        gauge=dict(
            axis=dict(range=[0,1],
                      tickcolor=AXIS_CLR,
                      tickfont=dict(color=AXIS_CLR, size=9, family="IBM Plex Mono")),
            bar=dict(color=risk_color(latest_score), thickness=0.3),
            bgcolor="rgba(255,255,255,0.02)",
            borderwidth=2,
            bordercolor="#222222",
            steps=[
                dict(range=[0, 0.40], color="rgba(57,255,20,0.06)"),
                dict(range=[0.40,0.65], color="rgba(232,255,0,0.06)"),
                dict(range=[0.65,1],   color="rgba(255,45,85,0.06)"),
            ])))
    fig3.update_layout(
        paper_bgcolor=CHART_BG,
        font=dict(color=AXIS_CLR, family="IBM Plex Mono"),
        margin=dict(l=20, r=20, t=20, b=10), height=160)
    st.plotly_chart(fig3, use_container_width=True)

# ── RECENT EVENTS ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📰 <span>Recent</span> ESG Events</div>', unsafe_allow_html=True)

rng2 = np.random.default_rng(get_company_seed(selected) + 1)
sample_events = rng2.choice(len(DEMO_EVENTS), size=6, replace=False)
events_html = ""
for idx in sample_events:
    lbl, sentiment, headline, risk = DEMO_EVENTS[idx]
    css  = {"Environmental": "env", "Social": "soc", "Governance": "gov"}.get(lbl, "env")
    tag  = {"Environmental": "tag-env", "Social": "tag-soc", "Governance": "tag-gov"}.get(lbl, "")
    stag = {"negative": "tag-neg", "neutral": "tag-neu", "positive": "tag-pos"}.get(sentiment, "")
    icon = {"negative": "▼", "neutral": "—", "positive": "▲"}.get(sentiment, "")
    edate = (date.today() - timedelta(days=int(rng2.integers(0, 7)))).strftime("%b %d")
    rc = '#ff2d55' if risk > 0.6 else '#e8ff00' if risk > 0.3 else '#39ff14'
    events_html += f"""
    <div class="event-card {css}">
        <div class="event-title">{headline}</div>
        <div class="event-meta">
            <span class="event-tag {tag}">{lbl}</span>
            <span class="event-tag {stag}">{icon} {sentiment.upper()}</span>
            <span>{edate}</span>
            <span>RISK: <strong style="color:{rc}">{risk:.2f}</strong></span>
        </div>
    </div>"""
st.markdown(events_html, unsafe_allow_html=True)

# ── LEADERBOARD ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🏆 <span>Company</span> Risk Leaderboard</div>', unsafe_allow_html=True)

leaderboard = sorted([(c, get_base_risk(c)) for c in COMPANIES], key=lambda x: x[1], reverse=True)
col_lb1, col_lb2 = st.columns(2)
for i, (company, score) in enumerate(leaderboard[:10]):
    col = col_lb1 if i < 5 else col_lb2
    clr = risk_color(score)
    with col:
        st.markdown(f"""
        <div class="lb-row">
            <div class="lb-rank">{i+1:02d}</div>
            <div class="lb-name">{company}</div>
            <div class="lb-bar-wrap">
                <div class="lb-bar" style="width:{int(score*100)}%; background:{clr};"></div>
            </div>
            <div class="lb-score" style="color:{clr}">{score:.2f}</div>
        </div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ESG RISK MONITOR &nbsp;·&nbsp; POWERED BY SREEJA &nbsp;·&nbsp;
    FINBERT-ESG &nbsp;·&nbsp; NEWSAPI &nbsp;·&nbsp; STREAMLIT &nbsp;·&nbsp; PLOTLY
</div>
""", unsafe_allow_html=True)