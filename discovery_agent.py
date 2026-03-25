"""
Agent 1: Discovery Agent — API Oracle
Analyzes Short Interest CSV, identifies Top 3 peak Squeeze Score dates per ticker,
and generates NewsAPI queries for institutional headlines during those windows.
"""

import pandas as pd
import requests
from datetime import datetime, timedelta

from config import (
    NEWSAPI_KEY, NEWSAPI_BASE_URL, FOCUS_TICKERS,
    TICKERS, INPUT_CSV, OUTPUT_DIR
)


def load_short_interest_data(filepath: str) -> pd.DataFrame:
    """Load and prepare the short interest dataset."""
    df = pd.read_csv(filepath)
    df["Business Date"] = pd.to_datetime(df["Business Date"], infer_datetime_format=True)
    df = df.sort_values(["Ticker", "Business Date"]).reset_index(drop=True)
    print(f"Loaded {len(df)} rows | Tickers: {TICKERS}")
    print(f"Date range: {df['Business Date'].min().date()} → {df['Business Date'].max().date()}")
    return df


def find_peak_squeeze_dates(df: pd.DataFrame, top_n: int = 3) -> dict:
    """Identify Top N peak Squeeze Score dates for each ticker."""
    peak_dates = {}
    for ticker in TICKERS:
        subset = df[df["Ticker"] == ticker].nlargest(top_n, "Squeeze Score")
        peak_dates[ticker] = subset[
            ["Business Date", "Squeeze Score", "Crowded Score",
             "ShortInterestPct", "S3Utilization"]
        ].reset_index(drop=True)
        print(f"\n{ticker} — Top {top_n} Squeeze Score Dates:")
        print(peak_dates[ticker].to_string(index=False))
    return peak_dates


def identify_most_crowded(df: pd.DataFrame) -> str:
    """Find the stock with the highest average Crowded Score."""
    avg_scores = df.groupby("Ticker")[
        ["Crowded Score", "Squeeze Score", "ShortInterestPct"]
    ].mean()
    most_crowded = avg_scores["Crowded Score"].idxmax()
    print(f"\n★ MOST CROWDED STOCK (avg Crowded Score): {most_crowded}")
    print(avg_scores.round(3))
    return most_crowded


def fetch_headlines(ticker: str, company_name: str, peak_date: str, window_days: int = 3) -> list:
    """
    Fetch news headlines ±N days around a peak squeeze date via NewsAPI.
    Returns a list of article dicts.
    """
    dt = datetime.strptime(peak_date, "%Y-%m-%d")
    params = {
        "q": f"{ticker} OR {company_name} short squeeze",
        "from": (dt - timedelta(days=window_days)).strftime("%Y-%m-%d"),
        "to": (dt + timedelta(days=window_days)).strftime("%Y-%m-%d"),
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWSAPI_KEY,
        "pageSize": 20,
    }
    try:
        response = requests.get(NEWSAPI_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        print(f"  {ticker} | {peak_date} | {len(articles)} articles fetched")
        return articles
    except requests.RequestException as e:
        print(f"  {ticker} | {peak_date} | ERROR: {e}")
        return []


def simple_sentiment(title: str) -> int:
    """
    Rule-based sentiment scoring on headline text.
    Returns: -1 (bearish), 0 (neutral), or 1 (bullish)
    """
    bullish_words = ["surge", "rally", "squeeze", "beat", "jump", "soar", "boom", "breakout"]
    bearish_words = ["fall", "drop", "short", "fraud", "lawsuit", "miss", "crash", "plunge"]
    title_lower = title.lower()
    score = (
        sum(1 for w in bullish_words if w in title_lower)
        - sum(1 for w in bearish_words if w in title_lower)
    )
    return max(-1, min(1, score))


def run_discovery_agent(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main execution: find peak dates, fetch headlines, score sentiment.
    Returns a DataFrame of headlines with sentiment scores.
    """
    print("\n" + "=" * 60)
    print("AGENT 1: DISCOVERY AGENT — Peak Squeeze Detection + NewsAPI")
    print("=" * 60)

    peak_dates = find_peak_squeeze_dates(df)
    most_crowded = identify_most_crowded(df)

    # Fetch headlines for each ticker's top peak date
    all_results = []
    for ticker in TICKERS:
        company = FOCUS_TICKERS[ticker]["name"]
        top_date = peak_dates[ticker]["Business Date"].iloc[0].strftime("%Y-%m-%d")
        articles = fetch_headlines(ticker, company, top_date)

        for article in articles:
            title = article.get("title", "")
            all_results.append({
                "Ticker": ticker,
                "Peak_Date": top_date,
                "Headline": title,
                "Source": article.get("source", {}).get("name", "Unknown"),
                "Published": article.get("publishedAt", ""),
                "Sentiment": simple_sentiment(title),
            })

    results_df = pd.DataFrame(all_results)

    # Save output
    output_path = f"{OUTPUT_DIR}/peak_squeeze_summary.csv"
    results_df.to_csv(output_path, index=False)
    print(f"\n✓ Results saved → {output_path}")
    print(f"  Total headlines: {len(results_df)}")

    return results_df


if __name__ == "__main__":
    df = load_short_interest_data(INPUT_CSV)
    results = run_discovery_agent(df)
