---
layout: default
title: Stock Quotes
parent: Plugins
nav_order: 14
---

# 📈 Stock Quotes

Fetch current stock, ETF, and mutual fund quotes

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/stock-quotes)

## Example config

### Default behavior

The plugin works out of the box with no configuration. It can fetch stocks, ETFs, and mutual funds without requiring an API key.

### Optional environment variables

| Variable | Description |
|----------|-------------|
| `FINNHUB_API_KEY` | Optional Finnhub API key |

If `FINNHUB_API_KEY` is set, the plugin will try Finnhub first and fall back automatically when needed.

## Tools

### `stock_quote`

Get the latest quote for a stock, ETF, or mutual fund symbol.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | Required | Stock ticker symbol (e.g., AAPL, GOOGL, QQQ, FXAIX). |

### `stock_quotes`

Get the latest quotes for multiple stock, ETF, or mutual fund symbols.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbols` | array | Required | Array of stock ticker symbols (e.g., ['MSFT', 'QQQ', 'FXAIX']). |
