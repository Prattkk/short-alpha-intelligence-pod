# Methodology — Scoring Logic & Formulas

## Noise Score

The composite signal that combines institutional and retail sentiment.

```
Noise Score = 0.4 × News Sentiment Index + 0.6 × Retail Hype Index
```

**Rationale for 60/40 weighting:** Retail signals lead institutional coverage by 12–48 hours in squeeze scenarios, making them more predictive of short-term Crowded Score movements. The 60% retail weighting reflects this empirical lead-time advantage.

## Sentiment Scoring

### News Sentiment (Agent 1)
Rule-based keyword classifier on NewsAPI headlines:

- **Bullish words:** surge, rally, squeeze, beat, jump, soar, boom, breakout
- **Bearish words:** fall, drop, short, fraud, lawsuit, miss, crash, plunge
- **Score:** `sum(bullish matches) - sum(bearish matches)`, clamped to [-1, 1]

### Retail Hype Index (Agent 2)
Normalized measure of retail enthusiasm on a [0, 1] scale:

- Post volume on r/wallstreetbets, r/stocks
- Hashtag velocity on Twitter/X
- Comment sentiment polarity

## Validation

Predictive power is validated using **Pearson correlation** between Noise Score (t) and Crowded Score (t + 48h):

| Ticker | r | p-value | Significant? |
|--------|-----|---------|-------------|
| AFRM | 0.192 | 0.002 | ✓ Yes |
| SQ | 0.087 | 0.161 | ✗ No |
| PYPL | 0.345 | <0.001 | ✓ Yes |
| SHOP | 0.064 | 0.308 | ✗ No |
| TSLA | 0.247 | <0.001 | ✓ Yes |

3 of 5 tickers show statistically significant predictive relationships (p < 0.05).

## Fidelity Score (Agent 4)

Measures how closely the synthetic stress-test dataset matches real SQ trading statistics. Scored across 4 dimensions (25 points each):

1. **Mean SI closeness** — distance from real SQ mean SI (8.5%)
2. **Range coverage** — does synthetic data span realistic SI range?
3. **Phase transition smoothness** — are regime changes gradual or jagged?
4. **Volatility clustering** — does high-vol cluster with high-vol (autocorrelation)?

**Result: 77.9/100**

Primary deductions:
- Volatility spread (49.2/100 on subdimension) — GARCH(1,1) would improve
- Sentiment-SI coupling (39.2/100) — Hidden Markov Model recommended for future
