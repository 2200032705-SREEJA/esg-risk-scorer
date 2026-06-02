# 🌿 Real-Time ESG Risk Scoring System

> **An AI-powered investment analytics platform** that monitors Environmental, Social, and Governance (ESG) risks across publicly listed companies using live news streams and transformer-based NLP — updated dynamically every time you launch.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)](https://streamlit.io)
[!](https://img.shields.io/badge/HuggingFace-FinBERT--ESG-yellow?logo=huggingface)](https://huggingface.co)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 What This Project Does

Traditional ESG assessments rely on quarterly reports — slow, backward-looking, and blind to emerging risks. This system changes that by:

1. **Fetching live ESG news** for 50+ companies via NewsAPI
2. **Classifying** each article into Environmental, Social, or Governance using FinBERT-ESG
3. **Scoring sentiment** (positive / neutral / negative) with FinBERT Sentiment
4. **Computing daily risk scores** (0–1 scale) using weighted ESG × Sentiment aggregation
5. **Forecasting 7-day risk trends** with linear regression
6. **Visualizing everything** in a Streamlit dashboard — real-time, interactive, and beautiful

---

## 🖥️ Dashboard Preview

```
┌──────────────────────────────────────────────────────────────┐
│  🌿 ESG Risk Monitor          [Company: Apple ▾]  [Refresh]  │
├──────────────────────────────────────────────────────────────┤
│  ESG Risk Score: 0.62 ▲   E: 0.71  S: 0.55  G: 0.48        │
│  ┌────────────────────────────────────┐                       │
│  │ 30-Day Risk Trend + 7-Day Forecast │                       │
│  └────────────────────────────────────┘                       │
│  Recent ESG Events:                                           │
│   ⚠️  [Environmental] Apple fined for e-waste ... (0.84)     │
│   ✅  [Governance]   Diversity hiring milestone ... (0.12)    │
└──────────────────────────────────────────────────────────────┘
```

---

## 🏗️ System Architecture

```
NewsAPI / Historical Tweets
         │
         ▼
  ┌─────────────┐
  │ Preprocessor│  (clean text, decode timestamps, tokenize)
  └──────┬──────┘
         │
         ▼
  ┌──────────────────┐
  │ FinBERT-ESG      │  → classify: Environmental / Social / Governance
  │ FinBERT Sentiment│  → detect: positive / neutral / negative
  └──────┬───────────┘
         │
         ▼
  ┌─────────────────────────┐
  │ Risk Score Engine       │  → weighted aggregation → 0–1 normalized score
  │ SQLite DB               │  → persist daily scores per company
  └──────────┬──────────────┘
             │
             ▼
  ┌──────────────────────────────┐
  │  Streamlit Dashboard         │
  │  • Real-time scores          │
  │  • ESG pillar breakdown      │
  │  • 30-day trend + forecast   │
  │  • 50-company comparison     │
  └──────────────────────────────┘
```

---

## 📁 Project Structure

```
esg-risk-scorer/
├── src/
│   ├── pipeline/
│   │   ├── fetcher.py         # NewsAPI + tweet collection
│   │   ├── preprocessor.py    # Text cleaning & normalization
│   │   └── ingestion.py       # Orchestrates the full pipeline
│   ├── models/
│   │   ├── esg_classifier.py  # FinBERT-ESG wrapper
│   │   ├── sentiment.py       # FinBERT Sentiment wrapper
│   │   └── risk_scorer.py     # ESG × Sentiment scoring engine
│   ├── dashboard/
│   │   └── app.py             # Streamlit app (main entry point)
│   └── utils/
│       ├── db.py              # SQLite helpers
│       └── config.py          # App-wide settings
├── data/
│   ├── raw/                   # Raw fetched articles
│   └── processed/             # Cleaned + scored data
├── notebooks/
│   └── EDA.ipynb              # Exploratory analysis & charts
├── tests/
│   ├── test_classifier.py
│   ├── test_scorer.py
│   └── test_fetcher.py
├── docs/
│   └── architecture.md
├── scripts/
│   └── seed_companies.py      # One-time company list seeding
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Quickstart

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/esg-risk-scorer.git
cd esg-risk-scorer
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
# Edit .env and add your NewsAPI key
```

### 3. Run the Dashboard

```bash
streamlit run src/dashboard/app.py
```

The pipeline auto-fetches the latest ESG news on every launch and updates all scores.

---

## 🔬 Models Used

| Model | Purpose | Source |
|-------|---------|--------|
| `yiyanghkust/finbert-esg` | ESG topic classification (E/S/G) | HuggingFace |
| `ProsusAI/finbert` | Financial sentiment analysis | HuggingFace |
| `sklearn LinearRegression` | 7-day risk forecasting | Scikit-learn |

**Classification accuracy:** 84–89% agreement with human labels on 200+ manually reviewed news samples.

---

## 📊 Key Results

| Metric | Value |
|--------|-------|
| Companies monitored | 50 |
| News articles processed | 43,000+ |
| ESG classification accuracy | 84–89% |
| Average update time (50 companies) | ~9 seconds |
| Forecast horizon | 7 days |
| Risk score range | 0 (safe) → 1 (high risk) |

---

## 💡 Business Use Cases

- **Portfolio managers** — rebalance based on ESG health across 50 companies
- **Retail investors** — "Should I invest now?" — answered by real-time scores
- **Compliance teams** — early warnings for regulatory and reputational risks
- **Sustainability analysts** — identify which ESG pillar (E/S/G) is most vulnerable

---

## 🚀 Future Roadmap

- [ ] Multi-source data ingestion (Bloomberg, Reuters, Reddit)
- [ ] Advanced forecasting (LSTM / Transformer-based time series)
- [ ] Portfolio-level ESG aggregation
- [ ] Cloud deployment (AWS / GCP) with scheduled auto-refresh
- [ ] REST API for third-party integration
- [ ] Peer benchmarking and sector comparisons

---

## 🛠️ Tech Stack

`Python 3.10` · `HuggingFace Transformers` · `FinBERT-ESG` · `Streamlit` · `SQLite` · `Pandas` · `Plotly` · `Scikit-learn` · `NewsAPI` · `NLTK`

---
