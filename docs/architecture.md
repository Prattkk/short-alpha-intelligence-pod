# System Architecture

## Multi-Agent Design Philosophy

The Short-Alpha Intelligence Pod uses a **4-agent pipeline architecture** where each agent specializes in a distinct analytical function. Agents operate sequentially, with each one enriching the data before passing it downstream.

This design mirrors how institutional trading desks decompose complex signals — no single analyst covers everything; instead, specialists collaborate to build a composite view.

## Agent Responsibilities

### Agent 1: Discovery Agent (API Oracle)
**Input:** Raw short interest CSV
**Output:** Peak squeeze dates + scored NewsAPI headlines
**Logic:** Identifies top-3 Squeeze Score dates per ticker, then queries NewsAPI for institutional headlines within a ±3 day window. Headlines are scored using a rule-based sentiment classifier (bullish/bearish keyword matching).

### Agent 2: Browser Scout (Retail Sentiment)
**Input:** Peak dates from Agent 1
**Output:** Retail Hype Index + Black Swan event log
**Logic:** Captures retail sentiment signals from Reddit (r/wallstreetbets, r/stocks) and Twitter/X around peak squeeze dates. Compares retail hype against institutional news sentiment to identify alpha gaps — moments where retail leads institutional coverage by 12–48 hours.

### Agent 3: Signal Aggregator
**Input:** Outputs from Agent 1 + Agent 2
**Output:** Composite Noise Score + correlation validation
**Logic:** Combines signals using a weighted formula: `Noise Score = 0.4 × News + 0.6 × Retail`. Validates predictive power by computing Pearson correlation between Noise Score and 48-hour forward Crowded Score.

### Agent 4: Synthesis Agent
**Input:** Most crowded ticker from Agent 1
**Output:** 1,095-day synthetic stress-test dataset
**Logic:** Generates a realistic multi-year dataset with three phases (Buildup → Squeeze → Recovery). Simulates correlated short interest, sentiment, volatility, and returns. Validated against real SQ statistics using a Fidelity Score metric.

## Data Flow

```
Short Interest CSV
       │
       ▼
  ┌─────────┐     NewsAPI
  │ Agent 1  │────────────► Headlines + Sentiment
  │ Discovery│
  └────┬─────┘
       │ peak dates
       ▼
  ┌─────────┐
  │ Agent 2  │────────────► Retail Hype + Black Swans
  │ Browser  │
  └────┬─────┘
       │ sentiment signals
       ▼
  ┌─────────┐
  │ Agent 3  │────────────► Noise Score + Validation
  │ Aggregat.│
  └────┬─────┘
       │ most crowded ticker
       ▼
  ┌─────────┐
  │ Agent 4  │────────────► 1,095-day Stress-Test
  │ Synthesis│
  └──────────┘
```

## Why This Architecture

Traditional approaches use a single data source (Bloomberg OR Reddit scraper). The multi-agent design captures signals that neither source alone can provide:

| Signal Type | API Oracle Only | Browser Scout Only | Combined |
|---|---|---|---|
| Earnings surprises | ✓ | ✗ | ✓ |
| Retail coordination | ✗ | ✓ | ✓ |
| Black Swan detection | Delayed | Early (12-48h lead) | Early |
| Regulatory filings | ✓ | ✗ | ✓ |
| Meme stock momentum | ✗ | ✓ | ✓ |
