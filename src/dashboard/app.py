"""
ESG Risk Monitor — Bloomberg-grade Dashboard
Powered by Sreeja | FinBERT-ESG + Keyword Fallback | Real SQLite data
"""

import sys
from pathlib import Path
from datetime import date, timedelta

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.models.risk_scorer import risk_label

st.set_page_config(
    page_title="ESG Risk Monitor",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design System ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

/* Reset Streamlit chrome */
header[data-testid="stHeader"],
.stToolbar,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stMain"] > div { padding: 0 !important; }

/* ── Tokens ── */
:root {
  --bg:          #0a0c10;
  --surface:     #111318;
  --surface-2:   #181b22;
  --border:      #23272f;
  --border-soft: rgba(255,255,255,0.06);

  --text:        #e8eaf0;
  --text-2:      #9299a8;
  --text-3:      #585f6d;

  --accent:      #2563eb;
  --accent-soft: rgba(37,99,235,0.12);
  --accent-glow: rgba(37,99,235,0.25);

  --green:       #10b981;
  --green-soft:  rgba(16,185,129,0.10);
  --yellow:      #f59e0b;
  --yellow-soft: rgba(245,158,11,0.10);
  --red:         #ef4444;
  --red-soft:    rgba(239,68,68,0.10);

  --env:         #10b981;
  --soc:         #818cf8;
  --gov:         #38bdf8;

  --mono: 'IBM Plex Mono', monospace;
  --sans: 'Inter', system-ui, sans-serif;

  --r-sm: 4px;
  --r-md: 8px;
  --r-lg: 12px;
}

html, body, [class*="css"] {
  font-family: var(--sans);
  color: var(--text);
  background: var(--bg);
}

.stApp {
  background: var(--bg);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
  width: 240px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }
section[data-testid="stSidebar"] .stSelectbox > div > div {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-sm) !important;
  color: var(--text) !important;
  font-family: var(--sans) !important;
  font-size: 0.875rem !important;
}
section[data-testid="stSidebar"] .stButton > button {
  background: var(--accent) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--r-sm) !important;
  font-family: var(--mono) !important;
  font-size: 0.7rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.08em !important;
  padding: 0.6rem 1rem !important;
  width: 100% !important;
  transition: opacity 0.15s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  opacity: 0.85 !important;
}

/* ── Topbar ── */
.topbar {
  height: 48px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}
.topbar-brand {
  display: flex; align-items: center; gap: 10px;
}
.topbar-logo {
  width: 28px; height: 28px;
  background: var(--accent);
  border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 700; color: #fff;
}
.topbar-name {
  font-family: var(--mono);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text);
  letter-spacing: 0.04em;
}
.topbar-sub {
  font-size: 0.72rem;
  color: var(--text-3);
  margin-left: 2px;
}
.topbar-stats {
  display: flex; align-items: center; gap: 24px;
}
.topbar-stat {
  display: flex; align-items: center; gap: 8px;
}
.topbar-stat-val {
  font-family: var(--mono);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text);
}
.topbar-stat-lbl {
  font-size: 0.68rem;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.topbar-divider {
  width: 1px; height: 20px;
  background: var(--border);
}
.status-dot {
  width: 6px; height: 6px;
  background: var(--green);
  border-radius: 50%;
  box-shadow: 0 0 6px var(--green);
}

/* ── Sidebar internals ── */
.sb-header {
  padding: 20px 20px 16px;
  border-bottom: 1px solid var(--border);
}
.sb-logo-row {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 4px;
}
.sb-icon {
  width: 32px; height: 32px;
  background: var(--accent);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; color: #fff;
}
.sb-title {
  font-family: var(--mono);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
  line-height: 1.3;
}
.sb-subtitle {
  font-size: 0.65rem;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-top: 2px;
}
.sb-section {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}
.sb-label {
  font-size: 0.65rem;
  font-weight: 600;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 8px;
}
.sb-score-card {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 16px;
  text-align: center;
}
.sb-score-num {
  font-family: var(--mono);
  font-size: 2.5rem;
  font-weight: 600;
  line-height: 1;
}
.sb-score-label {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-top: 4px;
}
.sb-pillar-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid var(--border-soft);
}
.sb-pillar-row:last-child { border-bottom: none; }
.sb-pillar-name {
  font-size: 0.75rem;
  color: var(--text-2);
  display: flex; align-items: center; gap: 6px;
}
.sb-pillar-dot {
  width: 6px; height: 6px; border-radius: 50%;
  flex-shrink: 0;
}
.sb-pillar-val {
  font-family: var(--mono);
  font-size: 0.75rem;
  font-weight: 500;
}
.sb-meta {
  font-size: 0.65rem;
  color: var(--text-3);
}

/* ── Main content ── */
.main-wrap {
  padding: 12px 24px 24px;
}

/* ── Page header ── */
.page-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--text);
  letter-spacing: -0.03em;
  margin-bottom: 4px;
  line-height: 1.1;
}
.page-header {
  display: flex; align-items: flex-start; justify-content: space-between;
  margin-bottom: 16px;
}
.page-meta {
  font-size: 0.78rem;
  color: var(--text-3);
  display: flex; align-items: center; gap: 12px;
}
.page-meta-sep { color: var(--border); }
.page-badge {
  display: inline-flex; align-items: center; gap: 5px;
  background: var(--accent-soft);
  border: 1px solid var(--accent-glow);
  border-radius: 20px;
  padding: 3px 10px;
  font-size: 0.65rem;
  font-weight: 600;
  color: #60a5fa;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-family: var(--mono);
  margin-top: 8px;
  display: inline-flex;
}

/* ── KPI Row ── */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}
.kpi-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 12px 14px;
  position: relative;
  overflow: hidden;
}
.kpi-card::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  border-radius: var(--r-lg) var(--r-lg) 0 0;
}
.kpi-card.green::after  { background: var(--green); }
.kpi-card.yellow::after { background: var(--yellow); }
.kpi-card.red::after    { background: var(--red); }
.kpi-card.env::after    { background: var(--env); }
.kpi-card.soc::after    { background: var(--soc); }
.kpi-card.gov::after    { background: var(--gov); }

.kpi-label {
  font-size: 0.68rem;
  font-weight: 600;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 8px;
  display: flex; align-items: center; gap: 6px;
}
.kpi-dot {
  width: 5px; height: 5px; border-radius: 50%;
}
.kpi-value {
  font-family: var(--mono);
  font-size: 1.7rem;
  font-weight: 600;
  line-height: 1;
  margin-bottom: 5px;
  letter-spacing: -0.02em;
}
.kpi-value.green  { color: var(--green); }
.kpi-value.yellow { color: var(--yellow); }
.kpi-value.red    { color: var(--red); }
.kpi-sub {
  font-size: 0.7rem;
  color: var(--text-3);
}
.kpi-risk-chip {
  display: inline-flex; align-items: center; gap: 4px;
  border-radius: 20px;
  padding: 2px 8px;
  font-size: 0.62rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-family: var(--mono);
}
.kpi-risk-chip.green  { background: var(--green-soft);  color: var(--green); }
.kpi-risk-chip.yellow { background: var(--yellow-soft); color: var(--yellow); }
.kpi-risk-chip.red    { background: var(--red-soft);    color: var(--red); }

/* ── Section headers ── */
.sec-header {
  display: flex; align-items: center; justify-content: space-between;
  margin: 0 0 12px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
}
.sec-title {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  display: flex; align-items: center; gap: 8px;
}
.sec-title-icon {
  font-size: 0.75rem;
  color: var(--text-3);
}
.sec-badge {
  font-family: var(--mono);
  font-size: 0.62rem;
  color: var(--text-3);
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 2px 6px;
}

/* ── Event cards ── */
.event-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 12px 14px;
  margin-bottom: 6px;
  display: flex; align-items: flex-start; gap: 12px;
  transition: border-color 0.15s;
}
.event-card:hover { border-color: rgba(255,255,255,0.15); }
.event-pillar-bar {
  width: 3px; border-radius: 4px; align-self: stretch; flex-shrink: 0;
  min-height: 36px;
}
.event-body { flex: 1; min-width: 0; }
.event-headline {
  font-size: 0.82rem;
  color: var(--text);
  line-height: 1.5;
  margin-bottom: 6px;
}
.event-meta-row {
  display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
}
.event-chip {
  display: inline-flex; align-items: center; gap: 3px;
  border-radius: 3px;
  padding: 1px 7px;
  font-size: 0.62rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-family: var(--mono);
  border: 1px solid;
}
.chip-env { border-color: rgba(16,185,129,0.3); color: var(--env); background: rgba(16,185,129,0.08); }
.chip-soc { border-color: rgba(129,140,248,0.3); color: var(--soc); background: rgba(129,140,248,0.08); }
.chip-gov { border-color: rgba(56,189,248,0.3);  color: var(--gov); background: rgba(56,189,248,0.08); }
.chip-neg { border-color: rgba(239,68,68,0.3);   color: var(--red);    background: rgba(239,68,68,0.08); }
.chip-neu { border-color: var(--border);           color: var(--text-3); background: transparent; }
.chip-pos { border-color: rgba(16,185,129,0.3);  color: var(--green);  background: rgba(16,185,129,0.08); }
.event-date { font-size: 0.68rem; color: var(--text-3); font-family: var(--mono); }
.event-risk-val { font-family: var(--mono); font-size: 0.72rem; font-weight: 600; }

/* ── Leaderboard ── */
.lb-row {
  display: flex; align-items: center;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 10px 14px;
  margin-bottom: 4px;
  gap: 12px;
  transition: border-color 0.15s;
  cursor: default;
}
.lb-row:hover { border-color: rgba(255,255,255,0.12); }
.lb-row.active { border-color: var(--accent); background: var(--accent-soft); }
.lb-rank {
  font-family: var(--mono);
  font-size: 0.68rem;
  color: var(--text-3);
  width: 22px;
  text-align: center;
}
.lb-rank.top { color: var(--yellow); font-weight: 600; }
.lb-name {
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--text);
  flex: 1;
}
.lb-name.active { color: #60a5fa; font-weight: 600; }
.lb-bar-wrap {
  flex: 2;
  height: 4px;
  background: var(--surface-2);
  border-radius: 2px;
  overflow: hidden;
}
.lb-bar { height: 100%; border-radius: 2px; }
.lb-score {
  font-family: var(--mono);
  font-size: 0.75rem;
  font-weight: 600;
  width: 42px;
  text-align: right;
}
.you-tag {
  font-family: var(--mono);
  font-size: 0.55rem;
  font-weight: 600;
  color: #60a5fa;
  border: 1px solid rgba(37,99,235,0.4);
  border-radius: 3px;
  padding: 1px 5px;
  letter-spacing: 0.06em;
}

/* ── Footer ── */
.footer {
  margin-top: 32px;
  padding: 16px 0;
  border-top: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
}
.footer-text {
  font-size: 0.65rem;
  color: var(--text-3);
  font-family: var(--mono);
  letter-spacing: 0.06em;
}
.footer-stack {
  display: flex; align-items: center; gap: 6px;
}
.footer-tag {
  font-size: 0.6rem;
  color: var(--text-3);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 2px 6px;
  font-family: var(--mono);
}

/* ── "What this means" explainer boxes ── */
.explain {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-top: 10px;
  margin-bottom: 4px;
  padding: 10px 12px;
  background: var(--surface-2);
  border: 1px solid var(--border-soft);
  border-left: 2px solid var(--accent);
  border-radius: var(--r-sm);
}
.explain-icon {
  color: var(--accent);
  font-size: 0.8rem;
  line-height: 1.4;
  flex-shrink: 0;
}
.explain-text {
  font-size: 0.72rem;
  line-height: 1.55;
  color: var(--text-2);
}
.explain-text b { color: var(--text); font-weight: 600; }
.sb-explain {
  margin-top: 8px;
  padding: 8px 10px;
  background: var(--bg);
  border: 1px solid var(--border-soft);
  border-radius: var(--r-sm);
  font-size: 0.66rem;
  line-height: 1.5;
  color: var(--text-3);
}
.sb-explain b { color: var(--text-2); font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
def risk_color(score: float) -> str:
    if score >= 0.65: return "#ef4444"
    if score >= 0.40: return "#f59e0b"
    return "#10b981"

def kpi_cls(v: float) -> str:
    if v >= 0.65: return "red"
    if v >= 0.40: return "yellow"
    return "green"

def risk_label_short(score: float) -> str:
    if score >= 0.65: return "High Risk"
    if score >= 0.40: return "Moderate"
    return "Low Risk"

def forecast(df: pd.DataFrame, horizon: int = 7) -> pd.DataFrame:
    from sklearn.linear_model import LinearRegression
    X = np.arange(len(df)).reshape(-1, 1)
    y = df["risk_score"].values
    m = LinearRegression().fit(X, y)
    fx = np.arange(len(df), len(df) + horizon).reshape(-1, 1)
    preds = np.clip(m.predict(fx), 0, 1)
    last = pd.to_datetime(df["date"].iloc[-1])
    fdates = pd.date_range(last + pd.Timedelta(days=1), periods=horizon).strftime("%Y-%m-%d")
    return pd.DataFrame({"date": fdates, "risk_score": preds})

# ── Data Layer ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_company_list():
    from src.utils.db import get_connection
    from src.utils.config import COMPANIES
    with get_connection() as conn:
        rows = conn.execute("SELECT DISTINCT company FROM daily_risk").fetchall()
    db_companies = {r[0] for r in rows}
    return [c for c in COMPANIES if c in db_companies]

@st.cache_data(ttl=300)
def load_risk_trend(company: str, days: int = 30):
    from src.utils.db import get_daily_risk
    return get_daily_risk(company, days)

@st.cache_data(ttl=300)
def load_latest_events(company: str, limit: int = 8):
    from src.utils.db import get_latest_events
    return get_latest_events(company, limit)

@st.cache_data(ttl=300)
def load_snapshot():
    from src.utils.db import get_company_snapshot
    return get_company_snapshot()

def refresh_cache():
    load_company_list.clear()
    load_risk_trend.clear()
    load_latest_events.clear()
    load_snapshot.clear()

from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=1)
if "pipeline_future" not in st.session_state:
    st.session_state.pipeline_future = None

def run_pipeline_and_refresh():
    from src.pipeline.ingestion import run_pipeline
    run_pipeline(verbose=False)
    refresh_cache()

def run_pipeline_background():
    return executor.submit(run_pipeline_and_refresh)

# Bootstrap
from src.utils.db import initialize_db, get_connection
initialize_db()
with get_connection() as _conn:
    _count = _conn.execute("SELECT COUNT(*) FROM daily_risk").fetchone()[0]
if _count == 0:
    with st.spinner("Seeding database…"):
        run_pipeline_and_refresh()

COMPANIES = load_company_list()

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-header">
      <div class="sb-logo-row">
        <div class="sb-icon">◈</div>
        <div>
          <div class="sb-title">ESG Monitor</div>
          <div class="sb-subtitle">Risk Intelligence</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section"><div class="sb-label">Company</div>', unsafe_allow_html=True)
    selected = st.selectbox("Company", COMPANIES, index=0, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    OUTPUT_OPTIONS = [
        "All Sections",
        "Composite Risk Score",
        "Pillar Breakdown",
        "Risk Trend & Forecast",
        "Risk Gauge",
        "Pillar Scores",
        "Recent ESG Events",
        "Risk Leaderboard",
    ]
    st.markdown('<div class="sb-section"><div class="sb-label">Show Output</div>', unsafe_allow_html=True)
    output_view = st.selectbox("Show Output", OUTPUT_OPTIONS, index=0, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    show_all        = output_view == "All Sections"
    show_composite  = show_all or output_view == "Composite Risk Score"
    show_pillars    = show_all or output_view == "Pillar Breakdown"
    show_trend      = show_all or output_view == "Risk Trend & Forecast"
    show_gauge      = show_all or output_view == "Risk Gauge"
    show_pillarbars = show_all or output_view == "Pillar Scores"
    show_events     = show_all or output_view == "Recent ESG Events"
    show_leaderboard = show_all or output_view == "Risk Leaderboard"

    df_risk = load_risk_trend(selected)

    if df_risk.empty:
        latest_score = env = soc = gov = 0.0
    else:
        latest_score = float(df_risk["risk_score"].iloc[-1])
        env  = float(df_risk["env_score"].iloc[-1])
        soc  = float(df_risk["social_score"].iloc[-1])
        gov  = float(df_risk["gov_score"].iloc[-1])

    color = risk_color(latest_score)
    cls   = kpi_cls(latest_score)

    sb_html = ""
    if show_composite:
        sb_html += f"""
        <div class="sb-section">
          <div class="sb-label">Composite Risk Score</div>
          <div class="sb-score-card">
            <div class="sb-score-num" style="color:{color}">{latest_score:.3f}</div>
            <div class="sb-score-label" style="color:{color}">{risk_label_short(latest_score)}</div>
          </div>
          <div class="sb-explain">A single 0–1 score for <b>{selected}</b> combining all ESG news. Closer to 0 = low risk, closer to 1 = high risk.</div>
        </div>"""
    if show_pillars:
        sb_html += f"""
        <div class="sb-section">
          <div class="sb-label">Pillar Breakdown</div>
          <div class="sb-pillar-row">
            <div class="sb-pillar-name"><div class="sb-pillar-dot" style="background:#10b981"></div>Environmental</div>
            <div class="sb-pillar-val" style="color:#10b981">{env:.3f}</div>
          </div>
          <div class="sb-pillar-row">
            <div class="sb-pillar-name"><div class="sb-pillar-dot" style="background:#818cf8"></div>Social</div>
            <div class="sb-pillar-val" style="color:#818cf8">{soc:.3f}</div>
          </div>
          <div class="sb-pillar-row">
            <div class="sb-pillar-name"><div class="sb-pillar-dot" style="background:#38bdf8"></div>Governance</div>
            <div class="sb-pillar-val" style="color:#38bdf8">{gov:.3f}</div>
          </div>
          <div class="sb-explain">The composite score is a weighted average of these three: <b>Environmental</b> 40%, <b>Social</b> 30%, <b>Governance</b> 30%.</div>
        </div>"""
    if sb_html:
        st.markdown(sb_html, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">', unsafe_allow_html=True)

    if "pipeline_running" not in st.session_state:
        st.session_state.pipeline_running = False

    if st.button("↺  Refresh Pipeline", use_container_width=True):
        if not st.session_state.pipeline_running:
            st.session_state.pipeline_running = True
            st.session_state.pipeline_future = run_pipeline_background()
            st.success("Pipeline running…")
        else:
            st.warning("Already running.")

    if (
        st.session_state.pipeline_running
        and st.session_state.pipeline_future is not None
        and st.session_state.pipeline_future.done()
    ):
        st.session_state.pipeline_running = False
        st.session_state.pipeline_future = None
        refresh_cache()
        st.success("Pipeline complete.")

    st.markdown(f"""
    <div style="margin-top:12px;">
      <div class="sb-meta">Updated {date.today().strftime('%d %b %Y')}</div>
      <div class="sb-meta">FinBERT-ESG · SQLite</div>
    </div>
    </div>
    """, unsafe_allow_html=True)

# ── TOPBAR ────────────────────────────────────────────────────────────────────
snapshot = load_snapshot()
n_companies = len(snapshot)
with get_connection() as _conn:
    n_events = _conn.execute("SELECT COUNT(*) FROM esg_events").fetchone()[0]

st.markdown(f"""
<div class="topbar">
  <div class="topbar-brand">
    <div class="topbar-logo">◈</div>
    <div>
      <div class="topbar-name">ESG RISK MONITOR</div>
      <div class="topbar-sub">NLP-powered · FinBERT-ESG · Real-time data</div>
    </div>
  </div>
  <div class="topbar-stats">
    <div class="topbar-stat">
      <div class="status-dot"></div>
      <div class="topbar-stat-lbl">Live</div>
    </div>
    <div class="topbar-divider"></div>
    <div class="topbar-stat">
      <div class="topbar-stat-val">{n_companies}</div>
      <div class="topbar-stat-lbl">Companies</div>
    </div>
    <div class="topbar-divider"></div>
    <div class="topbar-stat">
      <div class="topbar-stat-val">{n_events:,}</div>
      <div class="topbar-stat-lbl">Events Scored</div>
    </div>
    <div class="topbar-divider"></div>
    <div class="topbar-stat">
      <div class="topbar-stat-val">7-Day</div>
      <div class="topbar-stat-lbl">Forecast</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── MAIN CONTENT ──────────────────────────────────────────────────────────────
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# Page header
color = risk_color(latest_score)
cls   = kpi_cls(latest_score)
st.markdown(f"""
<div class="page-header">
  <div>
    <div class="page-title">{selected}</div>
    <div class="page-meta">
      <span>Environmental · Social · Governance</span>
      <span class="page-meta-sep">·</span>
      <span>{date.today().strftime('%d %b %Y')}</span>
    </div>
    <div style="margin-top:8px;">
      <span class="page-badge">◈ Real-Time Analytics</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# KPI Row
kpi_cards = ""
n_cards = 0
if show_composite:
    kpi_cards += f"""
  <div class="kpi-card {cls}">
    <div class="kpi-label"><div class="kpi-dot" style="background:{color}"></div>Composite Risk</div>
    <div class="kpi-value {cls}">{latest_score:.3f}</div>
    <div class="kpi-risk-chip {cls}">{risk_label_short(latest_score)}</div>
  </div>"""
    n_cards += 1
if show_pillars:
    kpi_cards += f"""
  <div class="kpi-card env">
    <div class="kpi-label"><div class="kpi-dot" style="background:var(--env)"></div>Environmental</div>
    <div class="kpi-value" style="color:var(--env)">{env:.3f}</div>
    <div class="kpi-sub">Emissions · Waste · Climate</div>
  </div>
  <div class="kpi-card soc">
    <div class="kpi-label"><div class="kpi-dot" style="background:var(--soc)"></div>Social</div>
    <div class="kpi-value" style="color:var(--soc)">{soc:.3f}</div>
    <div class="kpi-sub">Labour · Diversity · Safety</div>
  </div>
  <div class="kpi-card gov">
    <div class="kpi-label"><div class="kpi-dot" style="background:var(--gov)"></div>Governance</div>
    <div class="kpi-value" style="color:var(--gov)">{gov:.3f}</div>
    <div class="kpi-sub">Fraud · Compliance · Board</div>
  </div>"""
    n_cards += 3

if kpi_cards:
    explain_bits = []
    if show_composite:
        explain_bits.append("<b>Composite Risk</b> blends all three pillars (40% / 30% / 30%) into one overall figure.")
    if show_pillars:
        explain_bits.append("<b>Environmental</b>, <b>Social</b>, and <b>Governance</b> are each the average risk of that pillar's recent headlines.")
    explain_text = " ".join(explain_bits) + " Negative news raises the score, neutral news has a small effect, and positive news lowers it."

    st.markdown(f"""
    <div class="kpi-row" style="grid-template-columns: repeat({n_cards}, 1fr);">
      {kpi_cards}
    </div>
    <div class="explain">
      <div class="explain-icon">ⓘ</div>
      <div class="explain-text">
        <b>What this means:</b> these numbers (0–1, higher = riskier) come from scoring every recent news headline about
        <b>{selected}</b>. {explain_text}
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
CHART_BG  = "rgba(0,0,0,0)"
GRID_CLR  = "rgba(255,255,255,0.05)"
AXIS_CLR  = "#585f6d"
FONT_MONO = "IBM Plex Mono"

col_chart, col_right = (None, None)
if show_trend and (show_gauge or show_pillarbars):
    col_chart, col_right = st.columns([5, 2])
elif show_trend:
    col_chart = st.container()
elif show_gauge or show_pillarbars:
    col_right = st.container()

if show_trend and col_chart is not None:
    with col_chart:
        st.markdown("""
        <div class="sec-header">
          <div class="sec-title"><span class="sec-title-icon">↗</span>Risk Trend &amp; 7-Day Forecast</div>
          <div class="sec-badge">30-day window</div>
        </div>
        """, unsafe_allow_html=True)

        if not df_risk.empty and len(df_risk) >= 2:
            df_fc = forecast(df_risk)
            fig = go.Figure()

            # Shaded forecast zone
            fig.add_vrect(
                x0=df_fc["date"].iloc[0], x1=df_fc["date"].iloc[-1],
                fillcolor="rgba(37,99,235,0.04)", line_width=0)

            # Pillar lines (faint)
            for col_name, clr, lbl in [
                ("env_score",    "#10b981", "Environmental"),
                ("social_score", "#818cf8", "Social"),
                ("gov_score",    "#38bdf8", "Governance"),
            ]:
                fig.add_trace(go.Scatter(
                    x=df_risk["date"], y=df_risk[col_name], name=lbl,
                    line=dict(color=clr, dash="dot", width=1.2), opacity=0.5,
                    showlegend=True))

            # Composite area
            fig.add_trace(go.Scatter(
                x=df_risk["date"], y=df_risk["risk_score"], name="Composite",
                line=dict(color="#2563eb", width=2.5), mode="lines",
                fill="tozeroy", fillcolor="rgba(37,99,235,0.06)"))

            # Forecast
            fig.add_trace(go.Scatter(
                x=df_fc["date"], y=df_fc["risk_score"], name="Forecast",
                line=dict(color="#ef4444", dash="dash", width=1.8),
                marker=dict(size=0)))

            fig.update_layout(
                plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG,
                font=dict(color=AXIS_CLR, size=10, family=FONT_MONO),
                xaxis=dict(showgrid=False, color=AXIS_CLR, linecolor=GRID_CLR,
                           tickfont=dict(size=10)),
                yaxis=dict(showgrid=True, gridcolor=GRID_CLR, range=[0, 1],
                           color=AXIS_CLR, tickfont=dict(size=10),
                           tickformat=".2f"),
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                    font=dict(size=10, family=FONT_MONO), bgcolor="rgba(0,0,0,0)",
                    itemsizing="constant"),
                margin=dict(l=0, r=0, t=30, b=0),
                height=280,
                hovermode="x unified",
                hoverlabel=dict(bgcolor="#181b22", font=dict(family=FONT_MONO, size=11)))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""
            <div class="explain">
              <div class="explain-icon">ⓘ</div>
              <div class="explain-text">
                <b>What this means:</b> the solid blue line is {selected}'s actual composite risk score over the last 30 days;
                the dotted lines show the same trend for each pillar. The red dashed line is a simple <b>7-day forecast</b>
                fitted to the recent trend &mdash; it's a projection, not a prediction of real future events.
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Insufficient data. Run the pipeline to populate trend data.")

if (show_gauge or show_pillarbars) and col_right is not None:
    with col_right:
        if show_gauge:
            # Gauge
            st.markdown("""
            <div class="sec-header">
              <div class="sec-title">Risk Gauge</div>
            </div>
            """, unsafe_allow_html=True)

            fig3 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=latest_score,
                number=dict(font=dict(color=risk_color(latest_score), family=FONT_MONO, size=32),
                            valueformat=".3f"),
                gauge=dict(
                    axis=dict(range=[0, 1], tickcolor=AXIS_CLR,
                              tickfont=dict(color=AXIS_CLR, size=9, family=FONT_MONO),
                              nticks=5),
                    bar=dict(color=risk_color(latest_score), thickness=0.25),
                    bgcolor="rgba(0,0,0,0)", borderwidth=0,
                    steps=[
                        dict(range=[0, 0.40],  color="rgba(16,185,129,0.08)"),
                        dict(range=[0.40, 0.65], color="rgba(245,158,11,0.08)"),
                        dict(range=[0.65, 1],  color="rgba(239,68,68,0.08)"),
                    ],
                    threshold=dict(
                        line=dict(color=risk_color(latest_score), width=2),
                        thickness=0.75, value=latest_score))))
            fig3.update_layout(
                paper_bgcolor=CHART_BG,
                font=dict(color=AXIS_CLR, family=FONT_MONO),
                margin=dict(l=10, r=10, t=10, b=0),
                height=180)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown("""
            <div class="explain">
              <div class="explain-icon">ⓘ</div>
              <div class="explain-text">
                <b>What this means:</b> the needle is today's composite score. <b style="color:#10b981">Green</b> (0&ndash;0.40) is
                low risk, <b style="color:#f59e0b">yellow</b> (0.40&ndash;0.65) is moderate, <b style="color:#ef4444">red</b>
                (0.65&ndash;1.0) is high risk.
              </div>
            </div>
            """, unsafe_allow_html=True)

        if show_pillarbars:
            # Pillar bars
            st.markdown("""
            <div class="sec-header" style="margin-top:8px;">
              <div class="sec-title">Pillar Scores</div>
            </div>
            """, unsafe_allow_html=True)

            fig2 = go.Figure()
            for pillar, score, clr in [
                ("Environmental", env, "#10b981"),
                ("Social",        soc, "#818cf8"),
                ("Governance",    gov, "#38bdf8"),
            ]:
                fig2.add_trace(go.Bar(
                    x=[score], y=[pillar], orientation="h", name=pillar,
                    marker=dict(color=clr, opacity=0.85),
                    text=f"{score:.3f}", textposition="inside",
                    textfont=dict(color="#ffffff", size=11, family=FONT_MONO)))
            fig2.update_layout(
                plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG,
                showlegend=False, barmode="overlay",
                xaxis=dict(range=[0, 1], showgrid=True, gridcolor=GRID_CLR,
                           color=AXIS_CLR, tickformat=".1f",
                           tickfont=dict(size=9)),
                yaxis=dict(color=AXIS_CLR,
                           tickfont=dict(family=FONT_MONO, size=10)),
                font=dict(color=AXIS_CLR, family=FONT_MONO),
                margin=dict(l=0, r=0, t=0, b=0),
                height=120)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("""
            <div class="explain">
              <div class="explain-icon">ⓘ</div>
              <div class="explain-text">
                <b>What this means:</b> a side-by-side comparison of the three pillar scores, so you can see at a glance which
                area &mdash; environmental, social, or governance &mdash; is driving the company's overall risk.
              </div>
            </div>
            """, unsafe_allow_html=True)

# ── Events + Leaderboard ──────────────────────────────────────────────────────
col_ev, col_lb = (None, None)
if show_events and show_leaderboard:
    col_ev, col_lb = st.columns([3, 2])
elif show_events:
    col_ev = st.container()
elif show_leaderboard:
    col_lb = st.container()

if show_events and col_ev is not None:
    with col_ev:
        df_events = load_latest_events(selected, limit=8)
        st.markdown(f"""
        <div class="sec-header" style="margin-top:8px;">
          <div class="sec-title">Recent ESG Events</div>
          <div class="sec-badge">{selected}</div>
        </div>
        """, unsafe_allow_html=True)

        if df_events.empty:
            st.info("No events found. Run the pipeline.")
        else:
            events_html = ""
            for _, row in df_events.iterrows():
                lbl       = row.get("esg_label", "Environmental")
                sentiment = row.get("sentiment", "neutral")
                headline  = row.get("headline", "")
                risk      = float(row.get("risk_score", 0.0))
                edate     = str(row.get("date", ""))[:10]

                pillar_color = {"Environmental": "#10b981", "Social": "#818cf8", "Governance": "#38bdf8"}.get(lbl, "#10b981")
                chip_css     = {"Environmental": "chip-env", "Social": "chip-soc", "Governance": "chip-gov"}.get(lbl, "chip-env")
                sent_css     = {"negative": "chip-neg", "neutral": "chip-neu", "positive": "chip-pos"}.get(sentiment, "chip-neu")
                sent_icon    = {"negative": "▼", "neutral": "—", "positive": "▲"}.get(sentiment, "—")
                rc           = "#ef4444" if risk > 0.6 else "#f59e0b" if risk > 0.3 else "#10b981"

                events_html += f"""
                <div class="event-card">
                  <div class="event-pillar-bar" style="background:{pillar_color}"></div>
                  <div class="event-body">
                    <div class="event-headline">{headline}</div>
                    <div class="event-meta-row">
                      <span class="event-chip {chip_css}">{lbl}</span>
                      <span class="event-chip {sent_css}">{sent_icon} {sentiment.upper()}</span>
                      <span class="event-date">{edate}</span>
                      <span class="event-risk-val" style="color:{rc}">{risk:.3f}</span>
                    </div>
                  </div>
                </div>"""
            st.markdown(events_html, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="explain">
          <div class="explain-icon">ⓘ</div>
          <div class="explain-text">
            <b>What this means:</b> the most recent distinct ESG news headlines found for <b>{selected}</b>, newest first.
            Each card shows which pillar it relates to (Environmental / Social / Governance), whether the news was
            positive, neutral, or negative, and the individual risk score that headline contributed.
          </div>
        </div>
        """, unsafe_allow_html=True)

if show_leaderboard and col_lb is not None:
    with col_lb:
        st.markdown("""
        <div class="sec-header" style="margin-top:8px;">
          <div class="sec-title">Risk Leaderboard</div>
          <div class="sec-badge">Top 10</div>
        </div>
        """, unsafe_allow_html=True)

        if not snapshot.empty:
            top = snapshot.head(10)
            for i, (_, row) in enumerate(top.iterrows()):
                company = row["company"]
                score   = float(row["risk_score"])
                clr     = risk_color(score)
                is_sel  = company == selected
                rank_cls  = "top" if i < 3 else ""
                name_cls  = "active" if is_sel else ""
                row_cls   = "active" if is_sel else ""
                you_tag   = '<span class="you-tag">YOU</span>' if is_sel else ""

                st.markdown(f"""
                <div class="lb-row {row_cls}">
                  <div class="lb-rank {rank_cls}">{i+1:02d}</div>
                  <div class="lb-name {name_cls}">{company} {you_tag}</div>
                  <div class="lb-bar-wrap">
                    <div class="lb-bar" style="width:{int(score*100)}%;background:{clr}"></div>
                  </div>
                  <div class="lb-score" style="color:{clr}">{score:.3f}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No leaderboard data yet.")

        st.markdown("""
        <div class="explain">
          <div class="explain-icon">ⓘ</div>
          <div class="explain-text">
            <b>What this means:</b> all monitored companies ranked by their latest composite risk score, highest risk first.
            The <b>YOU</b> tag marks the company currently selected in the sidebar.
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div class="footer-text">ESG RISK MONITOR · POWERED BY SREEJA</div>
  <div class="footer-stack">
    <span class="footer-tag">FinBERT-ESG</span>
    <span class="footer-tag">Streamlit</span>
    <span class="footer-tag">Plotly</span>
    <span class="footer-tag">SQLite</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)