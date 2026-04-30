---
layout: default
title: Stock Quotes
parent: Plugins
nav_order: 13
---

# 📈 Stock Quotes

Fetch current stock, ETF, and mutual fund quotes

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/stock-quotes)

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
