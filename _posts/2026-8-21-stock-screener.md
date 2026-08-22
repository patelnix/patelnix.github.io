---
layout: post
title: "Building a Value Investor Stock Screener"
---

I have been thinking about a simple, opinionated stock screener — one that filters the market through the lens of investors I respect rather than arbitrary technical signals.

The idea: pull fundamentals for a broad universe of stocks, run them through a few well-defined strategies, and surface candidates worth a closer look. Not a buy list. A starting point.

The strategies I plan to implement:

- **Buffett** — ROE above 15%, net profit margin above 15%, conservative debt, positive FCF
- **Greenblatt (Magic Formula)** — earnings yield (EBITDA / enterprise value) + return on invested capital
- **Pabrai** — low P/E, minimal debt, high FCF yield, capital-efficient (ROE > 15%), healthy balance sheet
- **Peter Lynch (GARP)** — PEG below 1, earnings growth above 10%, P/E below 40

Data comes from Yahoo Finance via the open-source [yfinance](https://github.com/ranaroussi/yfinance) library, refreshed weekly by a GitHub Action. Everything runs client-side — no server, no backend, no API keys.

The page is live now. It is mostly scaffolding until the API key is wired in, but the strategy logic is already written.

→ [Open the Stock Screener](/stocks/)

I will keep refining the scoring as I learn more about what actually works in practice. Suggestions welcome.
