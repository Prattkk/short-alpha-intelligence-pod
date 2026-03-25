# short-alpha-intelligence-pod
### 🔍 Multi-Agent Short Squeeze Detection System | NewsAPI · Sentiment NLP · Short Interest Signals

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Academic%20Project-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![UIUC](https://img.shields.io/badge/MSBA-UIUC%20Gies-blue)

> **Disclaimer:** This is an academic project built during my MSBA at UIUC. It is not financial advice and should not be used for real trading decisions.
>
> ---
>
> ## 📌 Overview
>
> `short-alpha-intelligence-pod` is a Python-based multi-agent system designed to detect potential **short squeeze candidates** by fusing three independent signal streams: real-time news sentiment, short interest data, and price momentum. The system monitors five high-volatility fintech and tech tickers — **AFRM, SQ, PYPL, SHOP, and TSLA** — and aggregates signals from four specialized agents into a single actionable squeeze score.
>
> ---
>
> ## 🏗️ Architecture
>
> The system is composed of four autonomous agents that operate in a pipeline:
>
> ```
> ┌─────────────────────────────────────────────────────────────────┐
> │                  short-alpha-intelligence-pod                   │
> └─────────────────────────────────────────────────────────────────┘
>                               │
>           ┌───────────────────┼───────────────────┐
>           ▼                   ▼                   ▼
>  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
>  │  News Scraper   │ │ Short Interest  │ │  Price / Volume │
>  │     Agent       │ │     Agent       │ │   Data Source   │
>  │  (NewsAPI)      │ │ (Short % Float) │ │  (yfinance)     │
>  └────────┬────────┘ └────────┬────────┘ └────────┬────────┘
>           │                   │                   │
>           ▼                   │                   │
>  ┌─────────────────┐          │                   │
>  │   Sentiment     │          │                   │
>  │ Analysis Agent  │          │                   │
>  │ (VADER/TextBlob)│          │                   │
>  └────────┬────────┘          │                   │
>           │                   │                   │
>           └───────────────────┼───────────────────┘
>                               ▼
>                    ┌─────────────────────┐
>                    │  Signal Aggregator  │
>                    │       Agent         │
>                    │  (Squeeze Score +   │
>                    │   Ranked Output)    │
>                    └─────────────────────┘
> ```
>
> ### Agent Responsibilities
>
> | Agent | Role | Key Output |
> |---|---|---|
> | **News Scraper Agent** | Fetches real-time headlines via NewsAPI for each ticker | Raw news articles + timestamps |
> | **Sentiment Analysis Agent** | Scores each article using VADER & TextBlob; aggregates per ticker | Composite sentiment score (−1 to +1) |
> | **Short Interest Agent** | Pulls short % of float and days-to-cover from data source | Short interest score per ticker |
> | **Signal Aggregator Agent** | Combines all signals with configurable weights; ranks tickers | Final squeeze score + alert flag |
>
> ---
>
> ## ✨ Features
>
> - **Real-time news ingestion** via NewsAPI with per-ticker keyword filtering
> - - **Dual-model NLP sentiment pipeline** using both VADER (rule-based) and TextBlob (lexicon-based) for robust scoring
>   - - **Short interest signal layer** incorporating short float % and days-to-cover ratio
>     - - **Configurable signal weights** — adjust the influence of sentiment vs. short interest vs. momentum
>       - - **Squeeze score leaderboard** — tickers ranked by composite short squeeze probability
>         - - **Alert threshold system** — flags tickers that breach a configurable squeeze score cutoff
>           - - **Visualization dashboard** — bar charts and trend plots via Matplotlib and Plotly
>             - - **Modular agent design** — each agent is independently testable and swappable
>              
>               - ---
>
> ## 🛠️ Tech Stack
>
> | Category | Library / Tool |
> |---|---|
> | Language | Python 3.10 |
> | News Ingestion | [NewsAPI](https://newsapi.org/) |
> | Data Processing | Pandas, NumPy |
> | Sentiment NLP | VADER (`vaderSentiment`), TextBlob |
> | Market Data | yfinance |
> | Visualization | Matplotlib, Plotly |
> | Environment | python-dotenv |
> | Dev Tools | Jupyter Notebook, VS Code |
>
> ---
>
> ## 🚀 How to Run
>
> ### 1. Clone the repository
> ```bash
> git clone https://github.com/Prattkk/short-alpha-intelligence-pod.git
> cd short-alpha-intelligence-pod
> ```
>
> ### 2. Create and activate a virtual environment
> ```bash
> python -m venv venv
> source venv/bin/activate        # On Windows: venv\Scripts\activate
> ```
>
> ### 3. Install dependencies
> ```bash
> pip install -r requirements.txt
> ```
>
> ### 4. Set up your API key
> Create a `.env` file in the project root:
> ```
> NEWSAPI_KEY=your_newsapi_key_here
> ```
>
> > Get a free API key at [newsapi.org](https://newsapi.org/)
> >
> > ### 5. Run the system
> > ```bash
> > python main.py
> > ```
> >
> > Or open `analysis.ipynb` in Jupyter for an interactive walkthrough.
> >
> > ---
> >
> > ## 📊 Sample Output
> >
> > ```
> > ============================================================
> >   SHORT-ALPHA INTELLIGENCE POD — SQUEEZE SIGNAL REPORT
> >   Run Time: 2024-11-14  09:32 UTC
> > ============================================================
> >
> > Ticker   Sentiment   Short Interest   Momentum   Squeeze Score   Alert
> > ------   ---------   --------------   --------   -------------   -----
> > AFRM       +0.68          32.4%          +1.2        0.81         🔴 HIGH
> > SQ         +0.45          18.7%          +0.7        0.61         🟡 MED
> > TSLA       +0.31          22.1%          +0.4        0.54         🟡 MED
> > SHOP       +0.22          11.3%          +0.2        0.38         🟢 LOW
> > PYPL       -0.11           9.8%          -0.1        0.21         🟢 LOW
> >
> > Top Squeeze Candidate: AFRM  |  Score: 0.81  |  Confidence: HIGH
> > ============================================================
> > ```
> >
> > The dashboard also renders:
> > - **Sentiment trend chart** — daily rolling sentiment score per ticker over the lookback window
> > - - **Squeeze score bar chart** — ranked visualization of all five tickers
> >   - - **News volume heatmap** — article count per ticker per day to detect narrative velocity
> >    
> >     - ---
> >
> > ## 👤 My Role & What I Learned
> >
> > This was a solo academic project I designed and built end-to-end during my **MS in Business Analytics at the University of Illinois Urbana-Champaign (UIUC Gies)**.
> >
> > **What I built:**
> > - Designed the full 4-agent architecture from scratch, drawing on concepts from multi-agent systems and event-driven pipelines
> > - - Built and integrated the NewsAPI ingestion pipeline with rate-limit handling and deduplication logic
> >   - - Engineered the dual-model sentiment scoring system and calibrated weights via backtesting on historical squeeze events (GME, AMC, BBBY)
> >     - - Developed the signal aggregation layer with configurable weighting and alert thresholds
> >       - - Created the visualization layer to communicate signals clearly
> >        
> >         - **Key learnings:**
> >         - - How to architect modular, agent-based Python systems where components are independently testable
> >           - - The strengths and limitations of lexicon-based NLP (VADER, TextBlob) vs. transformer models for financial text
> >             - - Why signal fusion matters — no single signal (news sentiment alone, short interest alone) is reliably predictive; combining them substantially improves signal quality
> >               - - The importance of data freshness: stale news sentiment can be actively misleading in fast-moving markets
> >                
> >                 - ---
> >
> > ## 🔮 Future Enhancements
> >
> > - [ ] **Transformer-based sentiment** — swap VADER/TextBlob for FinBERT or a fine-tuned RoBERTa model for higher accuracy on financial headlines
> > - [ ] - [ ] **Options flow integration** — incorporate unusual options activity (high call volume, elevated IV) as a fourth independent signal
> > - [ ] - [ ] **Expanded ticker universe** — extend monitoring from 5 to 50+ tickers with dynamic watchlist management
> > - [ ] - [ ] **Async agent execution** — parallelize agent runs with `asyncio` or `concurrent.futures` to reduce end-to-end latency
> > - [ ] - [ ] **Alerting pipeline** — push squeeze alerts to Slack or email via webhook integrations
> > - [ ] - [ ] **Backtesting framework** — formal evaluation of signal accuracy against historical short squeeze events
> > - [ ] - [ ] **Streamlit dashboard** — wrap the output in a live web UI for real-time monitoring
> > - [ ] - [ ] **Docker containerization** — package the system for portable, reproducible deployment
> >
> > - [ ] ---
> >
> > - [ ] ## ⚠️ Disclaimer
> >
> > - [ ] This project was built **purely for academic and educational purposes** as part of the MS in Business Analytics program at UIUC. It is a demonstration of multi-agent system design, NLP pipelines, and financial data engineering concepts.
> >
> > - [ ] **This is NOT financial advice.** The squeeze scores and signals generated by this system are experimental and have not been validated for real-world trading. Do not use this system to make investment decisions. Past signal patterns do not guarantee future market behavior.
> >
> > - [ ] ---
> >
> > - [ ] *Built with curiosity and Python · MSBA @ UIUC Gies College of Business*
