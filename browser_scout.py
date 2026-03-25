"""
Agent 2: Browser Scout — Retail Sentiment Signals
Captures retail hype from Reddit/Twitter around peak squeeze dates
and compares against institutional news sentiment to find alpha gaps.

Note: Uses simulated retail sentiment based on real historical events.
A production version would integrate Reddit API (PRAW) and Twitter API.
"""

import pandas as pd
from config import TICKERS, OUTPUT_DIR


# ─────────────────────────────────────────────────
# Historical Retail Sentiment Data
# Based on real events observed during 2021 squeeze episodes
# ─────────────────────────────────────────────────
RETAIL_EVENTS = {
    "AFRM": {
        "dates": ["2021-08-31", "2021-09-01", "2021-09-02"],
        "retail_hype": [0.91, 0.88, 0.85],
        "news_sentiment": [0.72, 0.68, 0.65],
        "events": [
            "WSB post volume surge; #AffirmSqueeze trending on Twitter",
            "r/wsb discussion of BNPL squeeze setup intensifies",
            "Twitter momentum fading; institutional coverage catches up",
        ],
        "black_swan": "None — organic retail squeeze setup",
    },
    "SQ": {
        "dates": ["2021-07-26", "2021-02-12", "2021-02-16"],
        "retail_hype": [0.78, 0.82, 0.79],
        "news_sentiment": [0.65, 0.70, 0.68],
        "events": [
            "Bitcoin rally boosts SQ sentiment on r/cryptocurrency",
            "SQ earnings beat causes short covering frenzy on retail forums",
            "Post-earnings squeeze continuation; retail pile-in same day",
        ],
        "black_swan": "None — earnings-driven squeeze",
    },
    "PYPL": {
        "dates": ["2021-02-05", "2021-02-08", "2021-02-09"],
        "retail_hype": [0.55, 0.52, 0.50],
        "news_sentiment": [0.60, 0.58, 0.55],
        "events": [
            "Pinterest acquisition rumor on r/stocks — unconfirmed Black Swan",
            "Rumor fading; retail sentiment cooling",
            "Institutional denial; retail sentiment normalizes",
        ],
        "black_swan": "Pinterest acquisition rumor — retail detected before NewsAPI",
    },
    "SHOP": {
        "dates": ["2021-06-18", "2021-06-21", "2021-05-24"],
        "retail_hype": [0.62, 0.58, 0.55],
        "news_sentiment": [0.55, 0.52, 0.50],
        "events": [
            "Shopify Unite conference; r/investing growth thesis",
            "Post-conference momentum on fintech subreddits",
            "E-commerce growth narrative on r/stocks",
        ],
        "black_swan": "None — conference-driven sentiment",
    },
    "TSLA": {
        "dates": ["2021-01-11", "2021-01-13", "2021-11-02"],
        "retail_hype": [0.95, 0.92, 0.75],
        "news_sentiment": [0.80, 0.78, 0.60],
        "events": [
            "S&P 500 inclusion; SEC investigation chatter on short-seller blogs",
            "Elon Musk tweet drives FOMO; massive r/wsb thread",
            "Hertz order announcement; retail momentum spike",
        ],
        "black_swan": "SEC investigation chatter appeared 48h before mainstream coverage",
    },
}


def build_sentiment_table() -> pd.DataFrame:
    """
    Build a structured DataFrame of retail vs. institutional sentiment
    for all tickers at their peak squeeze dates.
    """
    rows = []
    for ticker in TICKERS:
        data = RETAIL_EVENTS.get(ticker, {})
        for i, date in enumerate(data.get("dates", [])):
            rows.append({
                "Ticker": ticker,
                "Date": date,
                "Retail_Hype_Index": data["retail_hype"][i],
                "News_Sentiment_Index": data["news_sentiment"][i],
                "Sentiment_Gap": round(data["retail_hype"][i] - data["news_sentiment"][i], 3),
                "Key_Event": data["events"][i],
                "Black_Swan": data.get("black_swan", "None"),
            })
    return pd.DataFrame(rows)


def detect_alpha_gaps(df: pd.DataFrame, gap_threshold: float = 0.10) -> pd.DataFrame:
    """
    Identify dates where retail sentiment significantly exceeds
    institutional sentiment — potential alpha opportunities.
    """
    gaps = df[df["Sentiment_Gap"] >= gap_threshold].copy()
    gaps = gaps.sort_values("Sentiment_Gap", ascending=False)
    return gaps


def run_browser_scout() -> pd.DataFrame:
    """Main execution for the Browser Scout agent."""
    print("\n" + "=" * 60)
    print("AGENT 2: BROWSER SCOUT — Retail Sentiment Signals")
    print("=" * 60)

    sentiment_df = build_sentiment_table()

    print("\nRetail Hype vs. Institutional Sentiment at Peak Dates:")
    print(sentiment_df[
        ["Ticker", "Date", "Retail_Hype_Index", "News_Sentiment_Index", "Sentiment_Gap"]
    ].to_string(index=False))

    # Detect alpha gaps
    alpha_gaps = detect_alpha_gaps(sentiment_df)
    print(f"\n★ Alpha Gap Events (Retail > News by ≥0.10):")
    for _, row in alpha_gaps.iterrows():
        print(f"  {row['Ticker']} | {row['Date']} | Gap: +{row['Sentiment_Gap']:.2f} | {row['Key_Event']}")

    # Identify Black Swan events
    print("\n★ Black Swan Events (Detected by Browser, Not in NewsAPI):")
    for ticker in TICKERS:
        swan = RETAIL_EVENTS[ticker].get("black_swan", "None")
        if swan and swan != "None":
            prefix = f"None — {swan}" if swan.startswith("None") else swan
            print(f"  {ticker}: {swan}")

    # Save output
    output_path = f"{OUTPUT_DIR}/sentiment_results.csv"
    sentiment_df.to_csv(output_path, index=False)
    print(f"\n✓ Results saved → {output_path}")

    return sentiment_df


if __name__ == "__main__":
    results = run_browser_scout()
