#!/usr/bin/env python3
"""
Fetch fundamental data for S&P 500 stocks via yfinance.
Outputs stocks-data.json to the repo root.

Field conventions stored in JSON:
  roe        - return on equity        as a percentage (e.g. 15.5 = 15.5%)
  de         - debt-to-equity          as a ratio      (e.g. 0.5  = 0.5x)
  margin     - net profit margin       as a percentage
  opMargin   - operating margin        as a percentage
  epsGrowth  - trailing EPS growth     as a percentage
  roa        - return on assets        as a percentage
  pe         - trailing P/E ratio
  pb         - price-to-book ratio
  peg        - PEG ratio
  fcfYield   - free cash flow yield    as a percentage
  ev         - enterprise value        raw USD
  ebitda     - EBITDA                  raw USD
  currentRatio - current ratio         raw ratio
  marketCap  - market capitalisation   raw USD
"""

import json
import time
import datetime
import sys

from io import StringIO

import requests
import pandas as pd
import yfinance as yf


def _pct(val):
    """Convert a yfinance decimal ratio to a rounded percentage, or None if absent."""
    return round(float(val) * 100, 2) if val is not None else None


def get_sp500_tickers():
    """Fetch current S&P 500 ticker list from Wikipedia."""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    # urllib's default User-Agent is blocked by Wikipedia (403); use requests instead
    headers = {"User-Agent": "Mozilla/5.0 (compatible; stock-screener/1.0; +https://patelnix.github.io)"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    df = pd.read_html(StringIO(resp.text))[0]
    # Yahoo Finance uses hyphens where tickers have dots (e.g. BRK.B -> BRK-B)
    return [t.replace(".", "-") for t in df["Symbol"].tolist()]


def fetch_stock(ticker):
    """
    Return a dict of fundamentals for one ticker, or None on failure.
    yfinance info field notes:
      debtToEquity  - reported as percentage (173.22 means D/E ratio of 1.7322)
      returnOnEquity - reported as decimal  (0.1496 means 14.96% ROE)
    """
    try:
        info = yf.Ticker(ticker).info

        # Skip non-equity results (sometimes Yahoo returns a minimal dict)
        if not info or info.get("quoteType") not in ("EQUITY",):
            return None

        market_cap   = info.get("marketCap") or 0
        free_cashflow = info.get("freeCashflow") or 0

        # Normalise ROE: decimal → percentage
        roe_raw = info.get("returnOnEquity")
        roe = round(roe_raw * 100, 2) if roe_raw is not None else None

        # Normalise D/E: Yahoo percentage → ratio
        de_raw = info.get("debtToEquity")
        de = round(de_raw / 100, 3) if de_raw is not None else None

        # FCF yield as percentage of market cap
        fcf_yield = 0.0
        if market_cap > 0 and free_cashflow:
            fcf_yield = round((free_cashflow / market_cap) * 100, 2)

        price = info.get("currentPrice") or info.get("regularMarketPrice") or 0

        return {
            "ticker":    ticker,
            "name":      info.get("shortName") or info.get("longName") or ticker,
            "sector":    info.get("sector", ""),
            "industry":  info.get("industry", ""),
            "price":     round(float(price), 2),
            "marketCap": market_cap,
            "pe":        round(float(info.get("trailingPE") or 0), 2),
            "pb":        round(float(info.get("priceToBook") or 0), 2),
            "roe":         roe,
            "de":          de,
            "peg":         round(float(info.get("pegRatio") or 0), 2),
            "fcfYield":    fcf_yield,
            "margin":      _pct(info.get("profitMargins")),
            "opMargin":    _pct(info.get("operatingMargins")),
            "epsGrowth":   _pct(info.get("earningsGrowth")),
            "roa":         _pct(info.get("returnOnAssets")),
            "ev":          info.get("enterpriseValue") or 0,
            "ebitda":      info.get("ebitda") or 0,
            "currentRatio": round(float(info.get("currentRatio") or 0), 2) or None,
        }

    except Exception as exc:
        print(f"  WARN {ticker}: {exc}", file=sys.stderr)
        return None


def main():
    print("Fetching S&P 500 ticker list from Wikipedia…")
    tickers = get_sp500_tickers()
    total = len(tickers)
    print(f"Found {total} tickers\n")

    stocks = []
    failed = []

    for i, ticker in enumerate(tickers, 1):
        print(f"[{i:3}/{total}] {ticker:<8}", end=" ", flush=True)
        data = fetch_stock(ticker)
        if data:
            stocks.append(data)
            print("ok")
        else:
            failed.append(ticker)
            print("skip")
        time.sleep(0.25)   # polite delay; avoids rate-limit errors

    output = {
        "generated": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count":     len(stocks),
        "stocks":    stocks,
    }

    out_path = "stocks-data.json"
    with open(out_path, "w") as fh:
        json.dump(output, fh, separators=(",", ":"))

    print(f"\nSaved {len(stocks)} stocks → {out_path}")
    if failed:
        print(f"Skipped ({len(failed)}): {', '.join(failed)}")


if __name__ == "__main__":
    main()
