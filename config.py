"""
Short-Alpha Intelligence Pod — Configuration
Shared constants, ticker definitions, and API settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────
# API Configuration
# ─────────────────────────────────────────────────
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "YOUR_API_KEY_HERE")
NEWSAPI_BASE_URL = "https://newsapi.org/v2/everything"

# ─────────────────────────────────────────────────
# Ticker Universe
# ─────────────────────────────────────────────────
FOCUS_TICKERS = {
    "AFRM": {
        "name": "Affirm",
        "sector": "Fintech / BNPL",
        "peak_dates": ["2021-08-31", "2021-09-01", "2021-09-02"],
    },
    "SQ": {
        "name": "Block",
        "sector": "Fintech / Payments",
        "peak_dates": ["2021-07-26", "2021-02-12", "2021-02-16"],
    },
    "PYPL": {
        "name": "PayPal",
        "sector": "Fintech / Payments",
        "peak_dates": ["2021-02-05", "2021-02-08", "2021-02-09"],
    },
    "SHOP": {
        "name": "Shopify",
        "sector": "E-Commerce / SaaS",
        "peak_dates": ["2021-06-18", "2021-06-21", "2021-05-24"],
    },
    "TSLA": {
        "name": "Tesla",
        "sector": "EV / Manufacturing",
        "peak_dates": ["2021-01-11", "2021-01-13", "2021-11-02"],
    },
}

TICKERS = list(FOCUS_TICKERS.keys())

# ─────────────────────────────────────────────────
# Noise Score Weights
# ─────────────────────────────────────────────────
NEWS_WEIGHT = 0.4
RETAIL_WEIGHT = 0.6

# ─────────────────────────────────────────────────
# File Paths
# ─────────────────────────────────────────────────
DATA_DIR = "data"
OUTPUT_DIR = "outputs"
INPUT_CSV = os.path.join(DATA_DIR, "sample_short_interest.csv")
