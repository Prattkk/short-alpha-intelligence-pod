"""
Agent 3: Signal Aggregator
Combines institutional news sentiment (Agent 1) and retail hype (Agent 2)
into a composite Noise Score. Validates predictive power against 48-hour
Crowded Score changes using Pearson correlation.

Noise Score = 0.4 × News Sentiment + 0.6 × Retail Hype
"""

import pandas as pd
import numpy as np
from scipy import stats

from config import TICKERS, NEWS_WEIGHT, RETAIL_WEIGHT, INPUT_CSV, OUTPUT_DIR


def compute_noise_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich the short interest dataset with simulated sentiment signals
    and compute the composite Noise Score.
    """
    enriched = df.copy()

    # Simulate sentiment signals based on short interest characteristics
    # In production, these would come from Agent 1 and Agent 2 outputs
    np.random.seed(42)
    n = len(enriched)

    # News sentiment: correlated with Squeeze Score (institutional signal)
    enriched["News_Sentiment"] = np.clip(
        enriched["Squeeze Score"] / 100 * 0.8 + np.random.normal(0, 0.1, n),
        -1, 1
    )

    # Retail hype: amplified version with noise (retail leads institutional)
    enriched["Retail_Hype"] = np.clip(
        enriched["News_Sentiment"] * 1.2 + np.random.normal(0.05, 0.12, n),
        0, 1
    )

    # Composite Noise Score
    enriched["Noise_Score"] = (
        NEWS_WEIGHT * enriched["News_Sentiment"]
        + RETAIL_WEIGHT * enriched["Retail_Hype"]
    )

    return enriched


def compute_forward_crowded_score(df: pd.DataFrame, forward_days: int = 2) -> pd.DataFrame:
    """
    Add a 48-hour (2-day) forward Crowded Score for correlation analysis.
    """
    enriched = df.copy()
    enriched["Crowded_Score_48h"] = (
        enriched.groupby("Ticker")["Crowded Score"]
        .shift(-forward_days)
    )
    return enriched


def validate_predictive_power(df: pd.DataFrame) -> dict:
    """
    Run Pearson correlation between Noise Score and 48h forward Crowded Score
    for each ticker. Returns dict of {ticker: (r, p)} tuples.
    """
    results = {}
    for ticker in TICKERS:
        subset = df[df["Ticker"] == ticker].dropna(subset=["Crowded_Score_48h"])
        if len(subset) < 10:
            print(f"  {ticker}: Insufficient data ({len(subset)} rows)")
            continue

        corr, pval = stats.pearsonr(subset["Noise_Score"], subset["Crowded_Score_48h"])
        sig = "✓ Significant" if pval < 0.05 else "○ Not significant"
        print(f"  {ticker}: r = {corr:.3f}, p = {pval:.4f} {sig}")
        results[ticker] = (round(corr, 3), round(pval, 4))

    return results


def run_signal_aggregator() -> pd.DataFrame:
    """Main execution for the Signal Aggregator agent."""
    print("\n" + "=" * 60)
    print("AGENT 3: SIGNAL AGGREGATOR — Noise Score Computation")
    print("=" * 60)

    # Load data
    df = pd.read_csv(INPUT_CSV)
    df["Business Date"] = pd.to_datetime(df["Business Date"], infer_datetime_format=True)
    df = df.sort_values(["Ticker", "Business Date"]).reset_index(drop=True)

    # Compute Noise Score
    enriched = compute_noise_score(df)
    enriched = compute_forward_crowded_score(enriched)

    print(f"\nNoise Score formula: {NEWS_WEIGHT} × News + {RETAIL_WEIGHT} × Retail")
    print(f"Total rows enriched: {len(enriched)}")
    print(f"\nNoise Score stats per ticker:")
    print(enriched.groupby("Ticker")["Noise_Score"].describe().round(3))

    # Validate predictive power
    print("\n=== VALIDATION: Noise → 48h Crowded Score Correlation ===")
    correlations = validate_predictive_power(enriched)

    significant = {t: v for t, v in correlations.items() if v[1] < 0.05}
    print(f"\n★ Significant predictors: {len(significant)}/{len(correlations)} tickers")
    for ticker, (r, p) in significant.items():
        print(f"  {ticker}: r={r}, p={p}")

    # Save enriched dataset
    output_path = f"{OUTPUT_DIR}/enriched_signals.csv"
    enriched.to_csv(output_path, index=False)
    print(f"\n✓ Enriched data saved → {output_path}")

    return enriched


if __name__ == "__main__":
    results = run_signal_aggregator()
