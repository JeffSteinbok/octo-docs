---
layout: default
title: Stock Quotes
parent: Plugins
nav_order: 14
---

📈 Stock Quotes

Fetch real-time stock, ETF, and mutual fund prices server-side.

### stock_quote

Get current stock price, change, and percent change for a single ticker symbol. Works for stocks, ETFs, and mutual funds (e.g., MSFT, QQQ, FXAIX). Uses Yahoo Finance by default (no auth required). If FINNHUB_API_KEY is set, uses Finnhub API as primary source with Yahoo Finance fallback.

| Name   | Type   | Description                                                |
|--------|--------|------------------------------------------------------------|
| symbol | string | Stock ticker symbol (e.g., AAPL, GOOGL, QQQ, FXAIX)        |

### stock_quotes

Get current stock prices for multiple ticker symbols in a single batch request. Works for stocks, ETFs, and mutual funds. Returns all successful quotes plus any errors for failed symbols. Uses Yahoo Finance by default (no auth required). If FINNHUB_API_KEY is set, uses Finnhub API as primary source with Yahoo Finance fallback.

| Name    | Type  | Description                                                        |
|---------|-------|--------------------------------------------------------------------|
| symbols | array | Array of stock ticker symbols (e.g., ['MSFT', 'QQQ', 'FXAIX'])     |
