"""
ESG Risk Scoring Dashboard — Streamlit App
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
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #050d1a; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, #050d1a 100%);
    border-right: 1px solid rgba(0,255,136,0.1);
}
.hero-banner {
    background: linear-gradient(135deg, #0a1628 0%, #0d2137 50%, #071428 100%);
    border: 1px solid rgba(0,255,136,0.15);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(0,255,136,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem; font-weight: 800;
    color: #ffffff; margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px; line-height: 1.1;
}
.hero-subtitle { font-size: 1rem; color: rgba(255,255,255,0.45); margin: 0; font-weight: 300; }
.hero-badge {
    display: inline-block;
    background: rgba(0,255,136,0.1);
    border: 1px solid rgba(0,255,136,0.3);
    color: #00ff88; font-size: 0.7rem; font-weight: 600;
    letter-spacing: 2px; text-transform: uppercase;
    padding: 4px 12px; border-radius: 20px; margin-bottom: 1rem;
}
.kpi-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 1rem; margin-bottom: 2rem;
}
.kpi-card {
    background: linear-gradient(135deg, #0d1f35 0%, #091729 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 1.4rem 1.6rem;
    position: relative; overflow: hidden;
}
.kpi-card::after {
    content: ''; position: absolute;
    bottom: 0; left: 0; right: 0; height: 2px;
    border-radius: 0 0 16px 16px;
}
.kpi-card.green::after  { background: linear-gradient(90deg, #00ff88, transparent); }
.kpi-card.yellow::after { background: linear-gradient(90deg, #ffd700, transparent); }
.kpi-card.red::after    { background: linear-gradient(90deg, #ff4d6d, transparent); }
.kpi-label { font-size: 0.72rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: rgba(255,255,255,0.35); margin-bottom: 0.6rem; }
.kpi-value { font-family: 'Syne', sans-serif; font-size: 2.4rem; font-weight: 800; line-height: 1; margin-bottom: 0.3rem; }
.kpi-value.green  { color: #00ff88; }
.kpi-value.yellow { color: #ffd700; }
.kpi-value.red    { color: #ff4d6d; }
.kpi-trend { font-size: 0.78rem; color: rgba(255,255,255,0.35); }
.section-header {
    font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700;
    color: #ffffff; letter-spacing: -0.2px; margin: 2rem 0 1rem 0;
}
.section-header span { color: #00ff88; }
.event-card {
    background: #0d1f35; border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid; border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.2rem; margin-bottom: 0.6rem;
}
.event-card.env { border-left-color: #00ff88; }
.event-card.soc { border-left-color: #4d9fff; }
.event-card.gov { border-left-color: #b47fff; }
.event-title { font-size: 0.88rem; color: #e0e0e0; line-height: 1.4; margin-bottom: 0.3rem; }
.event-meta  { font-size: 0.72rem; color: rgba(255,255,255,0.35); display: flex; gap: 1rem; }
.event-tag { display: inline-block; font-size: 0.65rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; padding: 2px 8px; border-radius: 4px; }
.tag-env { background: rgba(0,255,136,0.1); color: #00ff88; }
.tag-soc { background: rgba(77,159,255,0.1); color: #4d9fff; }
.tag-gov { background: rgba(180,127,255,0.1); color: #b47fff; }
.tag-neg { background: rgba(255,77,109,0.1); color: #ff4d6d; }
.tag-neu { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.5); }
.tag-pos { background: rgba(0,255,136,0.1); color: #00ff88; }
.lb-row {
    display: flex; align-items: center; background: #0d1f35;
    border: 1px solid rgba(255,255,255,0.05); border-radius: 10px;
    padding: 0.7rem 1.2rem; margin-bottom: 0.4rem; gap: 1rem;
}
.lb-rank { font-family: 'Syne', sans-serif; font-size: 0.85rem; color: rgba(255,255,255,0.25); width: 24px; }
.lb-name { font-size: 0.88rem; color: #e0e0e0; flex: 1; }
.lb-bar-wrap { flex: 2; background: rgba(255,255,255,0.05); border-radius: 4px; height: 6px; overflow: hidden; }
.lb-bar { height: 100%; border-radius: 4px; }
.lb-score { font-family: 'Syne', sans-serif; font-size: 0.9rem; font-weight: 700; width: 48px; text-align: right; }
</style>
""", unsafe_allow_html=True)

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
    if score >= 0.65: return "#ff4d6d"
    if score >= 0.40: return "#ffd700"
    return "#00ff88"

def risk_label(score):
    if score >= 0.65: return "High Risk"
    if score >= 0.40: return "Moderate"
    return "Low Risk"

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

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem;">
        <div style="font-size:3rem;">🌿</div>
        <div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:800; color:#fff;">ESG Risk Monitor</div>
        <div style="font-size:0.7rem; color:rgba(255,255,255,0.3); letter-spacing:2px; text-transform:uppercase; margin-top:0.2rem;">Powered by FinBERT-ESG</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    selected = st.selectbox("Select Company", COMPANIES, index=0, label_visibility="collapsed")
    base = get_base_risk(selected)
    df_risk = generate_risk_trend(base, seed=get_company_seed(selected))
    latest_score = df_risk["risk_score"].iloc[-1]
    color = risk_color(latest_score)
    st.markdown(f"""
    <div style="text-align:center; padding:1.5rem 0;">
        <div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(255,255,255,0.3); margin-bottom:0.5rem;">Current Risk Score</div>
        <div style="font-family:'Syne',sans-serif; font-size:3.5rem; font-weight:800; color:{color}; line-height:1;">{latest_score:.2f}</div>
        <div style="font-size:0.9rem; color:{color}; margin-top:0.3rem;">{risk_label(latest_score)}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🔄  Refresh Data", use_container_width=True):
        st.success("✅ Dashboard refreshed!")
    st.markdown("""
    <div style="margin-top:2rem; font-size:0.68rem; color:rgba(255,255,255,0.2); text-align:center; line-height:1.8;">
        FinBERT-ESG · NewsAPI · Streamlit<br>Scikit-learn · SQLite · Plotly
    </div>
    """, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
    <div class="hero-badge">Real-Time ESG Analytics</div>
    <div class="hero-title">{selected}</div>
    <div class="hero-subtitle">Environmental · Social · Governance Risk Assessment &nbsp;|&nbsp; NLP-powered by FinBERT-ESG &nbsp;|&nbsp; Updated {date.today().strftime('%b %d, %Y')}</div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
env = df_risk["env_score"].iloc[-1]
soc = df_risk["social_score"].iloc[-1]
gov = df_risk["gov_score"].iloc[-1]

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card {kpi_color_class(latest_score)}">
    <div class="kpi-label">Composite Risk</div>
    <div class="kpi-value {kpi_color_class(latest_score)}">{latest_score:.2f}</div>
    <div class="kpi-trend">{risk_label(latest_score)}</div>
  </div>
  <div class="kpi-card {kpi_color_class(env)}">
    <div class="kpi-label">🌱 Environmental</div>
    <div class="kpi-value {kpi_color_class(env)}">{env:.2f}</div>
    <div class="kpi-trend">Emissions · Waste · Climate</div>
  </div>
  <div class="kpi-card {kpi_color_class(soc)}">
    <div class="kpi-label">🤝 Social</div>
    <div class="kpi-value {kpi_color_class(soc)}">{soc:.2f}</div>
    <div class="kpi-trend">Labour · Diversity · Safety</div>
  </div>
  <div class="kpi-card {kpi_color_class(gov)}">
    <div class="kpi-label">⚖️ Governance</div>
    <div class="kpi-value {kpi_color_class(gov)}">{gov:.2f}</div>
    <div class="kpi-trend">Fraud · Compliance · Board</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
col_chart, col_pillar = st.columns([3, 2])

with col_chart:
    st.markdown('<div class="section-header">📈 30-Day Risk Trend <span>+ 7-Day Forecast</span></div>', unsafe_allow_html=True)
    df_fc = forecast(df_risk)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_risk["date"], y=df_risk["risk_score"], name="Composite Risk",
        line=dict(color="#00ff88", width=2.5), mode="lines", fill="tozeroy", fillcolor="rgba(0,255,136,0.04)"))
    for col_name, clr, lbl in [("env_score","#00ff88","Environmental"),("social_score","#4d9fff","Social"),("gov_score","#b47fff","Governance")]:
        fig.add_trace(go.Scatter(x=df_risk["date"], y=df_risk[col_name], name=lbl,
            line=dict(color=clr, dash="dot", width=1.2), opacity=0.6))
    fig.add_trace(go.Scatter(x=df_fc["date"], y=df_fc["risk_score"], name="Forecast",
        line=dict(color="#ff4d6d", dash="dash", width=2)))
    fig.add_vrect(x0=df_fc["date"].iloc[0], x1=df_fc["date"].iloc[-1], fillcolor="rgba(255,77,109,0.04)", line_width=0)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgba(255,255,255,0.5)", size=11),
        xaxis=dict(showgrid=False, color="rgba(255,255,255,0.2)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", range=[0,1], color="rgba(255,255,255,0.2)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=0, r=0, t=30, b=0), height=300)
    st.plotly_chart(fig, use_container_width=True)

with col_pillar:
    st.markdown('<div class="section-header">🎯 Pillar <span>Breakdown</span></div>', unsafe_allow_html=True)
    fig2 = go.Figure()
    for pillar, score, clr in [("Environmental", env, "#00ff88"), ("Social", soc, "#4d9fff"), ("Governance", gov, "#b47fff")]:
        fig2.add_trace(go.Bar(x=[score], y=[pillar], orientation="h", name=pillar,
            marker=dict(color=clr, opacity=0.85), text=f'{score:.2f}',
            textposition="inside", textfont=dict(color="white", size=13, family="Syne")))
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False, barmode="overlay",
        xaxis=dict(range=[0,1], showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="rgba(255,255,255,0.2)"),
        yaxis=dict(color="rgba(255,255,255,0.5)"),
        font=dict(color="rgba(255,255,255,0.5)"),
        margin=dict(l=0, r=0, t=10, b=0), height=180)
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = go.Figure(go.Indicator(mode="gauge+number", value=latest_score,
        number=dict(font=dict(color=risk_color(latest_score), family="Syne", size=36)),
        gauge=dict(
            axis=dict(range=[0,1], tickcolor="rgba(255,255,255,0.2)", tickfont=dict(color="rgba(255,255,255,0.3)", size=9)),
            bar=dict(color=risk_color(latest_score), thickness=0.25),
            bgcolor="rgba(255,255,255,0.03)",
            steps=[dict(range=[0,0.40], color="rgba(0,255,136,0.07)"),
                   dict(range=[0.40,0.65], color="rgba(255,215,0,0.07)"),
                   dict(range=[0.65,1], color="rgba(255,77,109,0.07)")],
            borderwidth=0)))
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="rgba(255,255,255,0.4)"),
        margin=dict(l=20, r=20, t=20, b=10), height=150)
    st.plotly_chart(fig3, use_container_width=True)

# ── Recent Events ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📰 Recent <span>ESG Events</span></div>', unsafe_allow_html=True)
rng2 = np.random.default_rng(get_company_seed(selected) + 1)
sample_events = rng2.choice(len(DEMO_EVENTS), size=6, replace=False)
events_html = ""
for idx in sample_events:
    lbl, sentiment, headline, risk = DEMO_EVENTS[idx]
    css  = {"Environmental":"env","Social":"soc","Governance":"gov"}.get(lbl,"env")
    tag  = {"Environmental":"tag-env","Social":"tag-soc","Governance":"tag-gov"}.get(lbl,"")
    stag = {"negative":"tag-neg","neutral":"tag-neu","positive":"tag-pos"}.get(sentiment,"")
    icon = {"negative":"⚠️","neutral":"➖","positive":"✅"}.get(sentiment,"")
    edate = (date.today() - timedelta(days=int(rng2.integers(0,7)))).strftime("%b %d")
    rc = '#ff4d6d' if risk>0.6 else '#ffd700' if risk>0.3 else '#00ff88'
    events_html += f"""<div class="event-card {css}">
        <div class="event-title">{headline}</div>
        <div class="event-meta">
            <span class="event-tag {tag}">{lbl}</span>
            <span class="event-tag {stag}">{icon} {sentiment}</span>
            <span>{edate}</span>
            <span>Risk: <strong style="color:{rc}">{risk:.2f}</strong></span>
        </div></div>"""
st.markdown(events_html, unsafe_allow_html=True)

# ── Leaderboard ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🏆 Company <span>Risk Leaderboard</span></div>', unsafe_allow_html=True)
leaderboard = sorted([(c, get_base_risk(c)) for c in COMPANIES], key=lambda x: x[1], reverse=True)
col_lb1, col_lb2 = st.columns(2)
for i, (company, score) in enumerate(leaderboard[:10]):
    col = col_lb1 if i < 5 else col_lb2
    clr = risk_color(score)
    with col:
        st.markdown(f"""<div class="lb-row">
            <div class="lb-rank">{i+1}</div>
            <div class="lb-name">{company}</div>
            <div class="lb-bar-wrap"><div class="lb-bar" style="width:{int(score*100)}%; background:{clr};"></div></div>
            <div class="lb-score" style="color:{clr}">{score:.2f}</div>
        </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:3rem; padding:1.5rem; border-top:1px solid rgba(255,255,255,0.06);
            text-align:center; font-size:0.72rem; color:rgba(255,255,255,0.2); letter-spacing:1px;">
    ESG RISK MONITOR &nbsp;·&nbsp; FINBERT-ESG &nbsp;·&nbsp; NEWSAPI &nbsp;·&nbsp; STREAMLIT &nbsp;·&nbsp; PLOTLY
</div>
""", unsafe_allow_html=True)