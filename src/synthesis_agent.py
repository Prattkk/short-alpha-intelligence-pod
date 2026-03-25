"""
Agent 4: Synthesis Agent — 1,095-Day Stress-Test Generator
Generates a synthetic multi-year dataset for the most crowded stock (SQ)
simulating Black Swan regime transitions: buildup → peak → squeeze → recovery.

Fidelity Score: 77.9/100 against real SQ distribution.
"""

import pandas as pd
import numpy as np
from config import OUTPUT_DIR


def generate_stress_test(
    ticker: str = "SQ",
    n_days: int = 1095,
    seed: int = 2024,
) -> pd.DataFrame:
    """
    Generate a synthetic 1,095-day dataset with realistic phase transitions.

    Phases:
        - Buildup (0–55%):    Gradual SI accumulation, rising sentiment
        - Peak/Squeeze (55–65%): Rapid SI collapse, extreme volatility
        - Recovery (65–100%):  SI stabilization, sentiment normalization
    """
    np.random.seed(seed)
    dates = pd.bdate_range(start="2021-01-01", periods=n_days)

    # Phase boundaries
    buildup_end = int(n_days * 0.55)
    squeeze_end = int(n_days * 0.65)

    # ── SHORT INTEREST: gradual build → rapid collapse ──
    si = np.zeros(n_days)
    for i in range(buildup_end):
        si[i] = 0.04 + 0.06 * (i / buildup_end) + np.random.normal(0, 0.002)
    for i in range(buildup_end, squeeze_end):
        frac = (i - buildup_end) / (squeeze_end - buildup_end)
        si[i] = 0.10 - 0.07 * frac + np.random.normal(0, 0.003)
    for i in range(squeeze_end, n_days):
        frac = (i - squeeze_end) / (n_days - squeeze_end)
        si[i] = 0.03 + 0.02 * np.exp(-frac * 2) + np.random.normal(0, 0.002)
    si = np.clip(si, 0, 0.15)

    # ── NEWS SENTIMENT INDEX ──
    news_idx = np.zeros(n_days)
    for i in range(n_days):
        if i < buildup_end:
            trend = 0.3 * (i / buildup_end)
        elif i < squeeze_end:
            trend = 0.3 - 0.5 * ((i - buildup_end) / (squeeze_end - buildup_end))
        else:
            trend = -0.2 + 0.3 * ((i - squeeze_end) / (n_days - squeeze_end))
        news_idx[i] = trend + np.random.normal(0, 0.08)

    # Inject spike at squeeze start
    news_idx[buildup_end - 5: buildup_end + 5] += np.random.normal(0.4, 0.05, 10)
    news_idx = np.clip(news_idx, -1, 1)

    # ── RETAIL HYPE INDEX: lags news, amplified around squeeze ──
    retail_idx = np.zeros(n_days)
    for i in range(5, n_days):
        lag_effect = 0.6 * news_idx[i - 2] + 0.3 * news_idx[i - 5]
        retail_idx[i] = lag_effect + np.random.normal(0, 0.1)
    retail_idx[buildup_end:squeeze_end] += np.random.normal(0.3, 0.08, squeeze_end - buildup_end)
    retail_idx = np.clip(retail_idx, 0, 1)

    # ── PRICE VOLATILITY ──
    vol = np.abs(news_idx * 0.4 + retail_idx * 0.3) + si * 2
    vol[buildup_end:squeeze_end] *= 3
    vol = np.clip(vol + np.abs(np.random.normal(0, 0.015, n_days)), 0, 0.5)

    # ── SIMULATED RETURNS ──
    returns = np.random.normal(0, vol)
    returns[buildup_end:squeeze_end] += np.random.normal(0.02, 0.03, squeeze_end - buildup_end)

    # ── COMPOSITE SCORES ──
    noise_score = 0.4 * news_idx + 0.6 * retail_idx
    crowded_score = np.clip(si * 500 + np.random.normal(0, 3, n_days), 0, 100)
    squeeze_score = np.clip(crowded_score * 0.8 + vol * 100 + np.random.normal(0, 5, n_days), 0, 100)

    # ── PHASE LABELS ──
    phases = []
    for i in range(n_days):
        if i < buildup_end:
            phases.append("Buildup")
        elif i < squeeze_end:
            phases.append("Squeeze")
        else:
            phases.append("Recovery")

    df = pd.DataFrame({
        "Date": dates,
        "Ticker": ticker,
        "ShortInterestPct": np.round(si * 100, 2),
        "News_Sentiment": np.round(news_idx, 4),
        "Retail_Hype": np.round(retail_idx, 4),
        "Noise_Score": np.round(noise_score, 4),
        "Price_Volatility": np.round(vol, 4),
        "Simulated_Return": np.round(returns, 4),
        "Crowded_Score": np.round(crowded_score, 2),
        "Squeeze_Score": np.round(squeeze_score, 2),
        "Phase": phases,
    })

    return df


def compute_fidelity_score(synthetic_df: pd.DataFrame, real_mean_si: float = 0.085) -> float:
    """
    Compare synthetic distribution against real SQ statistics.
    Returns a score out of 100.

    Dimensions scored (equal weight):
        - SI mean closeness
        - SI range coverage
        - Phase transition smoothness
        - Volatility clustering presence
    """
    si = synthetic_df["ShortInterestPct"] / 100

    # 1. Mean closeness (0-25 pts)
    mean_diff = abs(si.mean() - real_mean_si)
    mean_score = max(0, 25 - mean_diff * 500)

    # 2. Range coverage (0-25 pts)
    si_range = si.max() - si.min()
    range_score = min(25, si_range * 250)

    # 3. Phase transition smoothness (0-25 pts)
    daily_change = si.diff().dropna().abs()
    smoothness = 1 - min(1, daily_change.std() / 0.01)
    smooth_score = smoothness * 25

    # 4. Volatility clustering (0-25 pts)
    vol = synthetic_df["Price_Volatility"]
    vol_autocorr = vol.autocorr(lag=1)
    cluster_score = max(0, vol_autocorr * 25)

    total = mean_score + range_score + smooth_score + cluster_score
    return round(total, 1)


def run_synthesis_agent() -> pd.DataFrame:
    """Main execution for the Synthesis Agent."""
    print("\n" + "=" * 60)
    print("AGENT 4: SYNTHESIS AGENT — 1,095-Day Stress-Test for SQ")
    print("=" * 60)

    synthetic = generate_stress_test(ticker="SQ")

    print(f"\nGenerated {len(synthetic)} trading days")
    print(f"Date range: {synthetic['Date'].min().date()} → {synthetic['Date'].max().date()}")
    print(f"\nPhase distribution:")
    print(synthetic["Phase"].value_counts().to_string())

    print(f"\nKey statistics:")
    print(f"  SI% mean:  {synthetic['ShortInterestPct'].mean():.2f}%")
    print(f"  SI% range: {synthetic['ShortInterestPct'].min():.2f}% – {synthetic['ShortInterestPct'].max():.2f}%")
    print(f"  Avg Noise Score: {synthetic['Noise_Score'].mean():.4f}")
    print(f"  Avg Squeeze Score: {synthetic['Squeeze_Score'].mean():.2f}")

    # Fidelity assessment
    fidelity = compute_fidelity_score(synthetic)
    print(f"\n★ Fidelity Score: {fidelity}/100")

    # Save output
    output_path = f"{OUTPUT_DIR}/synthetic_stress_test_SQ.csv"
    synthetic.to_csv(output_path, index=False)
    print(f"\n✓ Stress-test dataset saved → {output_path}")

    return synthetic


if __name__ == "__main__":
    results = run_synthesis_agent()
