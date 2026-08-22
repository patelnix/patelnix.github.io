---
layout: post
title: "Building a Value Investor Stock Screener"
---

I have been thinking about a simple, opinionated stock screener — one that filters the market through the lens of investors I respect rather than arbitrary technical signals.

The idea: pull fundamentals for a broad universe of stocks, run them through a few well-defined strategies, and surface candidates worth a closer look. Not a buy list. A starting point.

The strategies I plan to implement:

- **Buffett** — ROE above 15%, low price-to-book, conservative debt, durable earnings
- **Greenblatt (Magic Formula)** — rank by earnings yield and return on invested capital
- **Pabrai** — low P/E, clean balance sheet, high free cash flow, detectable moat
- **Peter Lynch (PEG)** — PEG ratio below 1, growth priced cheaply

Data comes from [Financial Modeling Prep](https://financialmodelingprep.com), which has a generous free tier. Everything runs client-side — no server, no backend, no data stored anywhere.

The page is live now. It is mostly scaffolding until the API key is wired in, but the strategy logic is already written.

→ [Open the Stock Screener](/stocks/)

I will keep refining the scoring as I learn more about what actually works in practice. Suggestions welcome.
