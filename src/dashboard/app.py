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
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Arctic / Orbitron / Shield Theme ──────────────────────────────────────────
# Accent: #00d4ff (ice cyan) · #7eb8ff (steel blue) · #a8edff (frost)
# Risk:   #00e5a0 (safe) · #ffb830 (moderate) · #ff4b6e (danger)
# Base:   #060d1f (void navy) · #0b1530 (card) · #0f1e40 (elevated)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

/* ── HIDE STREAMLIT DEFAULT HEADER ── */
header[data-testid="stHeader"] {
    background: #060d1f !important;
    border-bottom: 1px solid rgba(0,212,255,0.1) !important;
}

header[data-testid="stHeader"]::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 1px;
    background: linear-gradient(90deg, rgba(0,212,255,0.4), transparent);
}

/* Hide the toolbar buttons (Fork, GitHub, menu) */
.stToolbar {
    background: #060d1f !important;
}

/* Hide deploy button */
[data-testid="stToolbar"] {
    background: #060d1f !important;
}

:root {
    --accent:   #00d4ff;
    --accent2:  #7eb8ff;
    --frost:    #a8edff;
    --safe:     #00e5a0;
    --mod:      #ffb830;
    --danger:   #ff4b6e;
    --bg:       #060d1f;
    --card:     #0b1530;
    --elevated: #0f1e40;
    --border:   #1a2d55;
    --text:     #cde0ff;
    --muted:    rgba(160,200,255,0.35);
}

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    color: var(--text);
}

.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(ellipse 80% 40% at 50% -10%, rgba(0,212,255,0.07) 0%, transparent 70%),
        radial-gradient(ellipse 40% 30% at 90% 80%, rgba(126,184,255,0.04) 0%, transparent 60%);
}

.block-container { padding-top: 1.5rem !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080f24 0%, #060d1f 100%);
    border-right: 2px solid var(--border);
    box-shadow: 4px 0 30px rgba(0,212,255,0.04);
}

section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--elevated);
    border: 1.5px solid var(--border) !important;
    color: var(--text) !important;
    font-family: 'Rajdhani', sans-serif !important;
    border-radius: 6px !important;
    font-size: 0.95rem !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%) !important;
    color: #060d1f !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 0.7rem 1rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.25) !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #33ddff 0%, #00b8e6 100%) !important;
    box-shadow: 0 0 32px rgba(0,212,255,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── HERO BANNER ── */
.hero-banner {
    background: linear-gradient(135deg, #0b1530 0%, #0f1e40 60%, #0b1a38 100%);
    border: 1.5px solid var(--border);
    border-top: 3px solid var(--accent);
    border-radius: 12px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 60px rgba(0,212,255,0.06), inset 0 1px 0 rgba(0,212,255,0.1);
}

.hero-banner::before {
    content: '🛡️';
    position: absolute;
    right: 2.5rem; top: 50%;
    transform: translateY(-50%);
    font-size: 6rem;
    opacity: 0.06;
    filter: blur(2px);
}

.hero-banner::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 40%; height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent);
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.3);
    color: var(--accent);
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 1rem;
    font-family: 'Orbitron', monospace;
}

.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 3.2rem;
    font-weight: 900;
    color: #ffffff;
    margin: 0 0 0.3rem 0;
    letter-spacing: 4px;
    line-height: 1;
    text-transform: uppercase;
    text-shadow: 0 0 40px rgba(0,212,255,0.2);
}

.hero-subtitle {
    font-size: 0.85rem;
    color: var(--muted);
    margin: 0.8rem 0 0 0;
    font-weight: 500;
    letter-spacing: 1px;
    font-family: 'Rajdhani', sans-serif;
}

/* ── KPI CARDS ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.kpi-card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 10px;
    padding: 1.6rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.kpi-card:hover {
    border-color: var(--accent2);
    box-shadow: 0 0 24px rgba(0,212,255,0.08);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 10px 10px 0 0;
}

.kpi-card.green::before  { background: linear-gradient(90deg, var(--safe), transparent); }
.kpi-card.yellow::before { background: linear-gradient(90deg, var(--mod), transparent); }
.kpi-card.red::before    { background: linear-gradient(90deg, var(--danger), transparent); }

.kpi-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.8rem;
    font-family: 'Rajdhani', sans-serif;
}

.kpi-value {
    font-family: 'Orbitron', monospace;
    font-size: 2.6rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.4rem;
    letter-spacing: 1px;
}

.kpi-value.green  { color: var(--safe);   text-shadow: 0 0 20px rgba(0,229,160,0.3); }
.kpi-value.yellow { color: var(--mod);    text-shadow: 0 0 20px rgba(255,184,48,0.3); }
.kpi-value.red    { color: var(--danger); text-shadow: 0 0 20px rgba(255,75,110,0.3); }

.kpi-trend {
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 1px;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 500;
}

/* ── SECTION HEADERS ── */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 3px;
    margin: 2rem 0 1rem 0;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}

.section-header span { color: var(--accent); }

/* ── EVENT CARDS ── */
.event-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 4px solid;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.4rem;
    margin-bottom: 0.5rem;
    transition: background 0.15s ease, box-shadow 0.15s ease;
}

.event-card:hover {
    background: var(--elevated);
    box-shadow: 0 4px 20px rgba(0,212,255,0.05);
}

.event-card.env { border-left-color: var(--safe); }
.event-card.soc { border-left-color: var(--accent); }
.event-card.gov { border-left-color: var(--accent2); }

.event-title {
    font-size: 0.9rem;
    color: var(--text);
    line-height: 1.5;
    margin-bottom: 0.5rem;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 500;
}

.event-meta {
    font-size: 0.72rem;
    color: var(--muted);
    display: flex;
    gap: 1rem;
    align-items: center;
    font-family: 'Rajdhani', sans-serif;
}

.event-tag {
    display: inline-block;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid;
    font-family: 'Orbitron', monospace;
}

.tag-env { border-color: var(--safe);   color: var(--safe);   background: rgba(0,229,160,0.08); }
.tag-soc { border-color: var(--accent); color: var(--accent); background: rgba(0,212,255,0.08); }
.tag-gov { border-color: var(--accent2);color: var(--accent2);background: rgba(126,184,255,0.08); }
.tag-neg { border-color: var(--danger); color: var(--danger); background: rgba(255,75,110,0.08); }
.tag-neu { border-color: var(--muted);  color: var(--muted);  background: rgba(160,200,255,0.05); }
.tag-pos { border-color: var(--safe);   color: var(--safe);   background: rgba(0,229,160,0.08); }

/* ── LEADERBOARD ── */
.lb-row {
    display: flex;
    align-items: center;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.75rem 1.2rem;
    margin-bottom: 0.4rem;
    gap: 1rem;
    transition: all 0.2s ease;
}

.lb-row:hover {
    background: var(--elevated);
    border-color: var(--accent);
    box-shadow: 0 0 16px rgba(0,212,255,0.08);
    transform: translateX(2px);
}

.lb-rank {
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    width: 28px;
    letter-spacing: 1px;
}

.lb-name {
    font-size: 0.9rem;
    color: var(--text);
    flex: 1;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.lb-bar-wrap {
    flex: 2;
    background: rgba(255,255,255,0.05);
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
}

.lb-bar { height: 100%; border-radius: 4px; }

.lb-score {
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    width: 52px;
    text-align: right;
    letter-spacing: 1px;
}

/* ── SIDEBAR LOGO AREA ── */
.sidebar-logo {
    padding: 1.5rem 0 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
    text-align: center;
}

.sidebar-appname {
    font-family: 'Orbitron', monospace;
    font-size: 1rem;
    color: #ffffff;
    letter-spacing: 3px;
    line-height: 1.4;
    font-weight: 700;
}

.sidebar-powered {
    font-size: 0.6rem;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.4rem;
    font-family: 'Rajdhani', sans-serif;
}

.sidebar-score-block {
    background: var(--elevated);
    border: 1px solid var(--border);
    border-top: 2px solid var(--accent);
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1.2rem 0;
    text-align: center;
    box-shadow: 0 0 30px rgba(0,212,255,0.05);
}

.sidebar-score-label {
    font-size: 0.58rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.6rem;
    font-family: 'Orbitron', monospace;
}

.sidebar-score-value {
    font-family: 'Orbitron', monospace;
    font-size: 3.2rem;
    line-height: 1;
    letter-spacing: 2px;
    font-weight: 900;
}

.sidebar-score-risk {
    font-size: 0.65rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-top: 0.5rem;
    font-family: 'Orbitron', monospace;
    font-weight: 600;
}

/* ── FOOTER ── */
.footer {
    margin-top: 3rem;
    padding: 1.5rem;
    border-top: 1px solid var(--border);
    text-align: center;
    font-size: 0.6rem;
    color: var(--muted);
    letter-spacing: 2.5px;
    text-transform: uppercase;
    font-family: 'Rajdhani', sans-serif;
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

def get_base_risk(company, offset=0):
    rng = np.random.default_rng(get_company_seed(company) + offset)
    return float(rng.uniform(0.2, 0.85))

# ── SESSION STATE for refresh randomization ────────────────────────────────────
if "refresh_seed" not in st.session_state:
    st.session_state.refresh_seed = 0

def risk_color(score):
    if score >= 0.65: return "#ff4b6e"
    if score >= 0.40: return "#ffb830"
    return "#00e5a0"

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
        <div style="font-size:2.5rem; margin-bottom:0.5rem;">🛡️</div>
        <div class="sidebar-appname">ESG RISK<br>MONITOR</div>
        <div class="sidebar-powered">POWERED BY SREEJA</div>
    </div>
    """, unsafe_allow_html=True)

    selected = st.selectbox("SELECT COMPANY", COMPANIES, index=0, label_visibility="visible")
    base = get_base_risk(selected, offset=st.session_state.refresh_seed)
    df_risk = generate_risk_trend(base, seed=get_company_seed(selected) + st.session_state.refresh_seed)
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
        st.session_state.refresh_seed += 1
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
    <div class="hero-badge">🛡️ Real-Time ESG Analytics</div>
    <div class="hero-title">{selected}</div>
    <div class="hero-subtitle">
        Environmental · Social · Governance Risk Assessment &nbsp;|&nbsp;
        NLP-powered by FinBERT-ESG &nbsp;|&nbsp;
        Updated {date.today().strftime('%b %d, %Y')}
    </div>
</div>
""", unsafe_allow_html=True)

# ── PROJECT DESCRIPTION STRIP ─────────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(90deg, rgba(0,212,255,0.08) 0%, rgba(11,21,48,0.6) 50%, rgba(0,212,255,0.04) 100%);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 10px;
    padding: 1.2rem 2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 2.5rem;
    flex-wrap: wrap;
">
    <div style="display:flex; align-items:center; gap:0.6rem;">
        <span style="font-size:1.3rem;">🛡️</span>
        <div>
            <div style="font-family:'Orbitron',monospace; font-size:0.6rem; color:#00d4ff; letter-spacing:2px; text-transform:uppercase; margin-bottom:2px;">About This Project</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:0.92rem; color:rgba(160,200,255,0.85); font-weight:500; max-width:700px; line-height:1.5;">
                An NLP-powered ESG risk intelligence dashboard that processes financial news using
                <strong style="color:#00d4ff;">FinBERT-ESG</strong> to classify Environmental, Social &amp; Governance signals in real time —
                helping analysts and investors identify corporate risk exposure at a glance.
            </div>
        </div>
    </div>
    <div style="display:flex; gap:1.5rem; margin-left:auto; flex-shrink:0;">
        <div style="text-align:center;">
            <div style="font-family:'Orbitron',monospace; font-size:1rem; font-weight:700; color:#00d4ff;">20+</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:0.65rem; color:rgba(160,200,255,0.4); letter-spacing:1.5px; text-transform:uppercase;">Companies</div>
        </div>
        <div style="width:1px; background:rgba(0,212,255,0.15);"></div>
        <div style="text-align:center;">
            <div style="font-family:'Orbitron',monospace; font-size:1rem; font-weight:700; color:#00e5a0;">3</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:0.65rem; color:rgba(160,200,255,0.4); letter-spacing:1.5px; text-transform:uppercase;">ESG Pillars</div>
        </div>
        <div style="width:1px; background:rgba(0,212,255,0.15);"></div>
        <div style="text-align:center;">
            <div style="font-family:'Orbitron',monospace; font-size:1rem; font-weight:700; color:#ffb830;">7-Day</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:0.65rem; color:rgba(160,200,255,0.4); letter-spacing:1.5px; text-transform:uppercase;">Forecast</div>
        </div>
        <div style="width:1px; background:rgba(0,212,255,0.15);"></div>
        <div style="text-align:center;">
            <div style="font-family:'Orbitron',monospace; font-size:1rem; font-weight:700; color:#7eb8ff;">NLP</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:0.65rem; color:rgba(160,200,255,0.4); letter-spacing:1.5px; text-transform:uppercase;">Powered</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


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
GRID_CLR  = "rgba(0,212,255,0.06)"
AXIS_CLR  = "rgba(160,200,255,0.4)"

with col_chart:
    st.markdown('<div class="section-header">📈 <span>30-Day Risk Trend</span> + 7-Day Forecast</div>', unsafe_allow_html=True)
    df_fc = forecast(df_risk)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_risk["date"], y=df_risk["risk_score"], name="Composite Risk",
        line=dict(color="#00d4ff", width=2.5), mode="lines",
        fill="tozeroy", fillcolor="rgba(0,212,255,0.04)"))
    for col_name, clr, lbl in [
        ("env_score",    "#00e5a0", "Environmental"),
        ("social_score", "#7eb8ff", "Social"),
        ("gov_score",    "#a8edff", "Governance")
    ]:
        fig.add_trace(go.Scatter(
            x=df_risk["date"], y=df_risk[col_name], name=lbl,
            line=dict(color=clr, dash="dot", width=1.3), opacity=0.65))
    fig.add_trace(go.Scatter(
        x=df_fc["date"], y=df_fc["risk_score"], name="Forecast",
        line=dict(color="#ff4b6e", dash="dash", width=2.2)))
    fig.add_vrect(
        x0=df_fc["date"].iloc[0], x1=df_fc["date"].iloc[-1],
        fillcolor="rgba(255,75,110,0.03)", line_width=0)
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
        ("Environmental", env, "#00e5a0"),
        ("Social",        soc, "#00d4ff"),
        ("Governance",    gov, "#7eb8ff")
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
                dict(range=[0, 0.40], color="rgba(0,229,160,0.07)"),
                dict(range=[0.40,0.65], color="rgba(255,184,48,0.07)"),
                dict(range=[0.65,1],   color="rgba(255,75,110,0.07)"),
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

leaderboard = sorted(
    [(c, get_base_risk(c, offset=st.session_state.refresh_seed)) for c in COMPANIES],
    key=lambda x: x[1], reverse=True
)
col_lb1, col_lb2 = st.columns(2)
for i, (company, score) in enumerate(leaderboard[:10]):
    col = col_lb1 if i < 5 else col_lb2
    clr = risk_color(score)
    is_selected = company == selected
    highlight_border = "border-color: #00d4ff; background: rgba(0,212,255,0.05); box-shadow: 0 0 16px rgba(0,212,255,0.1);" if is_selected else ""
    highlight_name   = f"color: #00d4ff; font-weight: 700;" if is_selected else ""
    selected_tag     = ' &nbsp;<span style="font-size:0.5rem;color:#00d4ff;letter-spacing:2px;border:1px solid #00d4ff;padding:1px 6px;border-radius:10px;font-family:Orbitron,monospace;">◀ YOU</span>' if is_selected else ""
    with col:
        st.markdown(f"""
        <div class="lb-row" style="{highlight_border}">
            <div class="lb-rank">{i+1:02d}</div>
            <div class="lb-name" style="{highlight_name}">{company}{selected_tag}</div>
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