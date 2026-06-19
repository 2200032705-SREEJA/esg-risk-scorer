"""
ESG Risk Scoring Dashboard — Streamlit App
Powered by Sreeja | Real DB backend | FinBERT-ESG + Keyword Fallback
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
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

header[data-testid="stHeader"] { display: none !important; }
.stToolbar, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }

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

html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; color: var(--text); }
.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(ellipse 80% 40% at 50% -10%, rgba(0,212,255,0.07) 0%, transparent 70%),
        radial-gradient(ellipse 40% 30% at 90% 80%, rgba(126,184,255,0.04) 0%, transparent 60%);
}
.block-container { padding-top: 1.5rem !important; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080f24 0%, #060d1f 100%);
    border-right: 2px solid var(--border);
}
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--elevated); border: 1.5px solid var(--border) !important;
    color: var(--text) !important; font-family: 'Rajdhani', sans-serif !important;
    border-radius: 6px !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%) !important;
    color: #060d1f !important; border: none !important; border-radius: 6px !important;
    font-family: 'Orbitron', monospace !important; font-weight: 700 !important;
    font-size: 0.65rem !important; letter-spacing: 2px !important;
    text-transform: uppercase !important; padding: 0.7rem 1rem !important;
    width: 100% !important; box-shadow: 0 0 20px rgba(0,212,255,0.25) !important;
}

.hero-banner {
    background: linear-gradient(135deg, #0b1530 0%, #0f1e40 60%, #0b1a38 100%);
    border: 1.5px solid var(--border); border-top: 3px solid var(--accent);
    border-radius: 12px; padding: 2.5rem 3rem; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
    box-shadow: 0 0 60px rgba(0,212,255,0.06);
}
.hero-banner::before {
    content: '🛡️'; position: absolute; right: 2.5rem; top: 50%;
    transform: translateY(-50%); font-size: 6rem; opacity: 0.06; filter: blur(2px);
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.3);
    color: var(--accent); font-size: 0.6rem; font-weight: 700;
    letter-spacing: 3px; text-transform: uppercase; padding: 5px 14px;
    border-radius: 20px; margin-bottom: 1rem; font-family: 'Orbitron', monospace;
}
.hero-title {
    font-family: 'Orbitron', monospace; font-size: 3.2rem; font-weight: 900;
    color: #ffffff; margin: 0 0 0.3rem 0; letter-spacing: 4px; line-height: 1;
    text-transform: uppercase; text-shadow: 0 0 40px rgba(0,212,255,0.2);
}
.hero-subtitle {
    font-size: 0.85rem; color: var(--muted); margin: 0.8rem 0 0 0;
    font-weight: 500; letter-spacing: 1px;
}

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.kpi-card {
    background: var(--card); border: 1.5px solid var(--border);
    border-radius: 10px; padding: 1.6rem 1.4rem; position: relative; overflow: hidden;
}
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px; border-radius: 10px 10px 0 0;
}
.kpi-card.green::before  { background: linear-gradient(90deg, var(--safe), transparent); }
.kpi-card.yellow::before { background: linear-gradient(90deg, var(--mod), transparent); }
.kpi-card.red::before    { background: linear-gradient(90deg, var(--danger), transparent); }
.kpi-label {
    font-size: 0.65rem; font-weight: 600; letter-spacing: 2.5px;
    text-transform: uppercase; color: var(--muted); margin-bottom: 0.8rem;
}
.kpi-value {
    font-family: 'Orbitron', monospace; font-size: 2.6rem; font-weight: 700;
    line-height: 1; margin-bottom: 0.4rem; letter-spacing: 1px;
}
.kpi-value.green  { color: var(--safe);   text-shadow: 0 0 20px rgba(0,229,160,0.3); }
.kpi-value.yellow { color: var(--mod);    text-shadow: 0 0 20px rgba(255,184,48,0.3); }
.kpi-value.red    { color: var(--danger); text-shadow: 0 0 20px rgba(255,75,110,0.3); }
.kpi-trend { font-size: 0.72rem; color: var(--muted); letter-spacing: 1px; }

.section-header {
    font-family: 'Orbitron', monospace; font-size: 1rem; font-weight: 700;
    color: #ffffff; letter-spacing: 3px; margin: 2rem 0 1rem 0;
    text-transform: uppercase; display: flex; align-items: center;
    gap: 0.8rem; padding-bottom: 0.6rem; border-bottom: 1px solid var(--border);
}
.section-header span { color: var(--accent); }

.event-card {
    background: var(--card); border: 1px solid var(--border); border-left: 4px solid;
    border-radius: 0 8px 8px 0; padding: 1rem 1.4rem; margin-bottom: 0.5rem;
}
.event-card.env { border-left-color: var(--safe); }
.event-card.soc { border-left-color: var(--accent); }
.event-card.gov { border-left-color: var(--accent2); }
.event-title { font-size: 0.9rem; color: var(--text); line-height: 1.5; margin-bottom: 0.5rem; }
.event-meta { font-size: 0.72rem; color: var(--muted); display: flex; gap: 1rem; align-items: center; }
.event-tag {
    display: inline-block; font-size: 0.6rem; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase; padding: 3px 10px;
    border-radius: 20px; border: 1px solid; font-family: 'Orbitron', monospace;
}
.tag-env { border-color: var(--safe);   color: var(--safe);   background: rgba(0,229,160,0.08); }
.tag-soc { border-color: var(--accent); color: var(--accent); background: rgba(0,212,255,0.08); }
.tag-gov { border-color: var(--accent2);color: var(--accent2);background: rgba(126,184,255,0.08); }
.tag-neg { border-color: var(--danger); color: var(--danger); background: rgba(255,75,110,0.08); }
.tag-neu { border-color: var(--muted);  color: var(--muted);  background: rgba(160,200,255,0.05); }
.tag-pos { border-color: var(--safe);   color: var(--safe);   background: rgba(0,229,160,0.08); }

.lb-row {
    display: flex; align-items: center; background: var(--card);
    border: 1px solid var(--border); border-radius: 8px;
    padding: 0.75rem 1.2rem; margin-bottom: 0.4rem; gap: 1rem; transition: all 0.2s ease;
}
.lb-row:hover { background: var(--elevated); border-color: var(--accent); }
.lb-rank { font-family: 'Orbitron', monospace; font-size: 0.75rem; color: var(--muted); width: 28px; }
.lb-name { font-size: 0.9rem; color: var(--text); flex: 1; font-weight: 600; }
.lb-bar-wrap { flex: 2; background: rgba(255,255,255,0.05); border-radius: 4px; height: 6px; overflow: hidden; }
.lb-bar { height: 100%; border-radius: 4px; }
.lb-score { font-family: 'Orbitron', monospace; font-size: 0.85rem; font-weight: 700; width: 52px; text-align: right; }

.sidebar-logo { padding: 1.5rem 0 1rem; border-bottom: 1px solid var(--border); margin-bottom: 1.5rem; text-align: center; }
.sidebar-appname { font-family: 'Orbitron', monospace; font-size: 1rem; color: #ffffff; letter-spacing: 3px; font-weight: 700; }
.sidebar-powered { font-size: 0.6rem; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; margin-top: 0.4rem; }
.sidebar-score-block {
    background: var(--elevated); border: 1px solid var(--border);
    border-top: 2px solid var(--accent); border-radius: 10px;
    padding: 1.5rem; margin: 1.2rem 0; text-align: center;
}
.sidebar-score-label { font-size: 0.58rem; letter-spacing: 2.5px; text-transform: uppercase; color: var(--muted); margin-bottom: 0.6rem; font-family: 'Orbitron', monospace; }
.sidebar-score-value { font-family: 'Orbitron', monospace; font-size: 3.2rem; line-height: 1; letter-spacing: 2px; font-weight: 900; }
.sidebar-score-risk { font-size: 0.65rem; letter-spacing: 2.5px; text-transform: uppercase; margin-top: 0.5rem; font-family: 'Orbitron', monospace; font-weight: 600; }

.data-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(0,229,160,0.08); border: 1px solid rgba(0,229,160,0.25);
    color: var(--safe); font-size: 0.55rem; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase; padding: 3px 10px;
    border-radius: 12px; font-family: 'Orbitron', monospace;
}

.footer {
    margin-top: 3rem; padding: 1.5rem; border-top: 1px solid var(--border);
    text-align: center; font-size: 0.6rem; color: var(--muted);
    letter-spacing: 2.5px; text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def risk_color(score: float) -> str:
    if score >= 0.65: return "#ff4b6e"
    if score >= 0.40: return "#ffb830"
    return "#00e5a0"


def kpi_color_class(v: float) -> str:
    if v >= 0.65: return "red"
    if v >= 0.40: return "yellow"
    return "green"

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
def load_company_list() -> list[str]:
    """Return companies that have data in the DB, in config order."""
    from src.utils.db import get_connection
    from src.utils.config import COMPANIES
    with get_connection() as conn:
        rows = conn.execute("SELECT DISTINCT company FROM daily_risk").fetchall()
    db_companies = {r[0] for r in rows}
    return [c for c in COMPANIES if c in db_companies]

@st.cache_data(ttl=300)
def load_risk_trend(company: str, days: int = 30) -> pd.DataFrame:
    from src.utils.db import get_daily_risk
    return get_daily_risk(company, days)

@st.cache_data(ttl=300)
def load_latest_events(company: str, limit: int = 8) -> pd.DataFrame:
    from src.utils.db import get_latest_events
    return get_latest_events(company, limit)

@st.cache_data(ttl=300)
def load_snapshot() -> pd.DataFrame:
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

# ── Bootstrap DB if empty ─────────────────────────────────────────────────────
from src.utils.db import initialize_db, get_connection
initialize_db()
with get_connection() as _conn:
    _count = _conn.execute("SELECT COUNT(*) FROM daily_risk").fetchone()[0]
if _count == 0:
    with st.spinner("Seeding database with ESG data …"):
        run_pipeline_and_refresh()

COMPANIES = load_company_list()

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

    df_risk = load_risk_trend(selected)

    if df_risk.empty:
        latest_score = 0.0
        env = soc = gov = 0.0
    else:
        latest_score = float(df_risk["risk_score"].iloc[-1])
        env  = float(df_risk["env_score"].iloc[-1])
        soc  = float(df_risk["social_score"].iloc[-1])
        gov  = float(df_risk["gov_score"].iloc[-1])

    color = risk_color(latest_score)

    st.markdown(f"""
    <div class="sidebar-score-block">
        <div class="sidebar-score-label">Current Risk Score</div>
        <div class="sidebar-score-value" style="color:{color};">{latest_score:.2f}</div>
        <div class="sidebar-score-risk" style="color:{color};">{risk_label(latest_score)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="data-badge">✦ REAL DB DATA</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
if "pipeline_running" not in st.session_state:
    st.session_state.pipeline_running = False

if st.button("↺  REFRESH / RE-RUN PIPELINE", use_container_width=True):
    if not st.session_state.pipeline_running:
        st.session_state.pipeline_running = True
        st.session_state.pipeline_future = run_pipeline_background()
        st.success("✓ Pipeline started in background.")
    else:
        st.warning("Pipeline is already running.")

if (
    st.session_state.pipeline_running
    and st.session_state.pipeline_future is not None
    and st.session_state.pipeline_future.done()
):
    st.session_state.pipeline_running = False
    st.session_state.pipeline_future = None
    refresh_cache()
    st.success("✓ Pipeline completed successfully.")

    st.markdown("""
    <div style="margin-top:2rem; font-size:0.6rem; color:rgba(255,255,255,0.15); line-height:2;
                font-family:'IBM Plex Mono',monospace; letter-spacing:1.5px; text-transform:uppercase;">
        FinBERT-ESG · Keyword NLP<br>Streamlit · Scikit-learn<br>SQLite · Plotly
    </div>
    """, unsafe_allow_html=True)

# ── TOP BAR ───────────────────────────────────────────────────────────────────
snapshot = load_snapshot()
n_companies = len(snapshot)
n_events_q = "SELECT COUNT(*) FROM esg_events"
with get_connection() as _conn:
    n_events = _conn.execute(n_events_q).fetchone()[0]

st.markdown(f"""
<div style="background:linear-gradient(90deg,#060d1f 0%,#0b1530 40%,#060d1f 100%);
    border-bottom:2px solid rgba(0,212,255,0.2); padding:0.6rem 2.5rem;
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:0; position:sticky; top:0; z-index:999;">
  <div style="display:flex; align-items:center; gap:0.8rem;">
    <span style="font-size:1.1rem;">🛡️</span>
    <div>
      <span style="font-family:'Orbitron',monospace; font-size:0.58rem; color:#00d4ff; letter-spacing:2px;">ESG Risk Monitor</span>
      <span style="font-family:'Rajdhani',sans-serif; font-size:0.82rem; color:rgba(160,200,255,0.6); margin-left:1rem;">
        NLP-powered · <strong style="color:#00d4ff;">FinBERT-ESG</strong> · Real SQLite data
      </span>
    </div>
  </div>
  <div style="display:flex; align-items:center; gap:1.8rem; flex-shrink:0;">
    <div style="text-align:center;">
      <div style="font-family:'Orbitron',monospace; font-size:0.85rem; font-weight:700; color:#00d4ff;">{n_companies}</div>
      <div style="font-family:'Rajdhani',sans-serif; font-size:0.55rem; color:rgba(160,200,255,0.35); letter-spacing:1.5px; text-transform:uppercase;">Companies</div>
    </div>
    <div style="width:1px; height:28px; background:rgba(0,212,255,0.15);"></div>
    <div style="text-align:center;">
      <div style="font-family:'Orbitron',monospace; font-size:0.85rem; font-weight:700; color:#00e5a0;">{n_events}</div>
      <div style="font-family:'Rajdhani',sans-serif; font-size:0.55rem; color:rgba(160,200,255,0.35); letter-spacing:1.5px; text-transform:uppercase;">Events Scored</div>
    </div>
    <div style="width:1px; height:28px; background:rgba(0,212,255,0.15);"></div>
    <div style="text-align:center;">
      <div style="font-family:'Orbitron',monospace; font-size:0.85rem; font-weight:700; color:#ffb830;">7-Day</div>
      <div style="font-family:'Rajdhani',sans-serif; font-size:0.55rem; color:rgba(160,200,255,0.35); letter-spacing:1.5px; text-transform:uppercase;">Forecast</div>
    </div>
    <div style="width:1px; height:28px; background:rgba(0,212,255,0.15);"></div>
    <div style="text-align:center;">
      <div style="font-family:'Orbitron',monospace; font-size:0.85rem; font-weight:700; color:#7eb8ff;">NLP</div>
      <div style="font-family:'Rajdhani',sans-serif; font-size:0.55rem; color:rgba(160,200,255,0.35); letter-spacing:1.5px; text-transform:uppercase;">Powered</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── HERO BANNER ───────────────────────────────────────────────────────────────
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

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
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
CHART_BG = "rgba(0,0,0,0)"
GRID_CLR  = "rgba(0,212,255,0.06)"
AXIS_CLR  = "rgba(160,200,255,0.4)"

col_chart, col_pillar = st.columns([3, 2])

with col_chart:
    st.markdown('<div class="section-header">📈 <span>Risk Trend</span> + 7-Day Forecast</div>', unsafe_allow_html=True)
    if not df_risk.empty and len(df_risk) >= 2:
        df_fc = forecast(df_risk)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_risk["date"], y=df_risk["risk_score"], name="Composite Risk",
            line=dict(color="#00d4ff", width=2.5), mode="lines+markers",
            fill="tozeroy", fillcolor="rgba(0,212,255,0.04)",
            marker=dict(size=5)))
        for col_name, clr, lbl in [
            ("env_score",    "#00e5a0", "Environmental"),
            ("social_score", "#7eb8ff", "Social"),
            ("gov_score",    "#a8edff", "Governance"),
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
            xaxis=dict(showgrid=False, color=AXIS_CLR),
            yaxis=dict(showgrid=True, gridcolor=GRID_CLR, range=[0, 1], color=AXIS_CLR),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        font=dict(size=9, family="IBM Plex Mono"), bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=0, r=0, t=30, b=0), height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough data points to plot a trend. Run the pipeline to populate more dates.")

with col_pillar:
    st.markdown('<div class="section-header">🎯 <span>Pillar</span> Breakdown</div>', unsafe_allow_html=True)
    fig2 = go.Figure()
    for pillar, score, clr in [
        ("Environmental", env, "#00e5a0"),
        ("Social",        soc, "#00d4ff"),
        ("Governance",    gov, "#7eb8ff"),
    ]:
        fig2.add_trace(go.Bar(
            x=[score], y=[pillar], orientation="h", name=pillar,
            marker=dict(color=clr, opacity=0.9),
            text=f"{score:.3f}", textposition="inside",
            textfont=dict(color="black", size=13, family="Orbitron")))
    fig2.update_layout(
        plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG,
        showlegend=False, barmode="overlay",
        xaxis=dict(range=[0, 1], showgrid=True, gridcolor=GRID_CLR, color=AXIS_CLR),
        yaxis=dict(color=AXIS_CLR, tickfont=dict(family="IBM Plex Mono", size=10)),
        font=dict(color=AXIS_CLR, family="IBM Plex Mono"),
        margin=dict(l=0, r=0, t=10, b=0), height=180)
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=latest_score,
        number=dict(font=dict(color=risk_color(latest_score), family="Orbitron", size=40)),
        gauge=dict(
            axis=dict(range=[0, 1], tickcolor=AXIS_CLR,
                      tickfont=dict(color=AXIS_CLR, size=9, family="IBM Plex Mono")),
            bar=dict(color=risk_color(latest_score), thickness=0.3),
            bgcolor="rgba(255,255,255,0.02)", borderwidth=2, bordercolor="#222222",
            steps=[
                dict(range=[0, 0.40],  color="rgba(0,229,160,0.07)"),
                dict(range=[0.40, 0.65], color="rgba(255,184,48,0.07)"),
                dict(range=[0.65, 1],  color="rgba(255,75,110,0.07)"),
            ])))
    fig3.update_layout(
        paper_bgcolor=CHART_BG, font=dict(color=AXIS_CLR, family="IBM Plex Mono"),
        margin=dict(l=20, r=20, t=20, b=10), height=160)
    st.plotly_chart(fig3, use_container_width=True)

# ── RECENT ESG EVENTS (from DB) ───────────────────────────────────────────────
st.markdown('<div class="section-header">📰 <span>Recent</span> ESG Events</div>', unsafe_allow_html=True)

df_events = load_latest_events(selected, limit=8)

if df_events.empty:
    st.info("No events found for this company.")
else:
    events_html = ""
    for _, row in df_events.iterrows():
        lbl       = row.get("esg_label", "Environmental")
        sentiment = row.get("sentiment", "neutral")
        headline  = row.get("headline", "")
        risk      = float(row.get("risk_score", 0.0))
        edate     = str(row.get("date", ""))[:10]

        css  = {"Environmental": "env", "Social": "soc", "Governance": "gov"}.get(lbl, "env")
        tag  = {"Environmental": "tag-env", "Social": "tag-soc", "Governance": "tag-gov"}.get(lbl, "tag-env")
        stag = {"negative": "tag-neg", "neutral": "tag-neu", "positive": "tag-pos"}.get(sentiment, "tag-neu")
        icon = {"negative": "▼", "neutral": "—", "positive": "▲"}.get(sentiment, "—")
        rc   = "#ff4b6e" if risk > 0.6 else "#ffb830" if risk > 0.3 else "#00e5a0"

        events_html += f"""
        <div class="event-card {css}">
            <div class="event-title">{headline}</div>
            <div class="event-meta">
                <span class="event-tag {tag}">{lbl}</span>
                <span class="event-tag {stag}">{icon} {sentiment.upper()}</span>
                <span>{edate}</span>
                <span>RISK: <strong style="color:{rc}">{risk:.3f}</strong></span>
            </div>
        </div>"""
    st.markdown(events_html, unsafe_allow_html=True)

# ── LEADERBOARD (from DB) ─────────────────────────────────────────────────────
st.markdown('<div class="section-header">🏆 <span>Company</span> Risk Leaderboard</div>', unsafe_allow_html=True)

if not snapshot.empty:
    top = snapshot.head(10)
    col_lb1, col_lb2 = st.columns(2)
    for i, (_, row) in enumerate(top.iterrows()):
        company = row["company"]
        score   = float(row["risk_score"])
        clr     = risk_color(score)
        is_sel  = company == selected
        hb = "border-color:#00d4ff;background:rgba(0,212,255,0.05);" if is_sel else ""
        hn = "color:#00d4ff;font-weight:700;" if is_sel else ""
        tag = ' &nbsp;<span style="font-size:0.5rem;color:#00d4ff;letter-spacing:2px;border:1px solid #00d4ff;padding:1px 6px;border-radius:10px;font-family:Orbitron,monospace;">◀ YOU</span>' if is_sel else ""
        col = col_lb1 if i < 5 else col_lb2
        with col:
            st.markdown(f"""
            <div class="lb-row" style="{hb}">
                <div class="lb-rank">{i+1:02d}</div>
                <div class="lb-name" style="{hn}">{company}{tag}</div>
                <div class="lb-bar-wrap">
                    <div class="lb-bar" style="width:{int(score*100)}%;background:{clr};"></div>
                </div>
                <div class="lb-score" style="color:{clr}">{score:.3f}</div>
            </div>""", unsafe_allow_html=True)
else:
    st.info("No leaderboard data yet. Run the pipeline.")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ESG RISK MONITOR &nbsp;·&nbsp; POWERED BY SREEJA &nbsp;·&nbsp;
    FINBERT-ESG &nbsp;·&nbsp; KEYWORD NLP FALLBACK &nbsp;·&nbsp;
    STREAMLIT &nbsp;·&nbsp; PLOTLY &nbsp;·&nbsp; SQLITE
</div>
""", unsafe_allow_html=True)
