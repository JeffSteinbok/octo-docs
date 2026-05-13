---
layout: default
title: stock-quotes
nav_order: 17
nav_exclude: true
---

# 📈 stock-quotes

Fetch current stock, ETF, and mutual fund quotes from Yahoo Finance or Finnhub.

> **Source:** [JeffSteinbok/carapace-stock-quotes](https://github.com/JeffSteinbok/carapace-stock-quotes)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>finnhubApiKey</code></td><td>string</td><td>Optional</td><td>Finnhub API key. When set, Finnhub is used as the primary data source (higher rate limits). Free key at finnhub.io.</td></tr>
  </tbody>
</table>

## Tools

### `stock_quote`

Get the latest quote for a stock, ETF, or mutual fund symbol.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbol` | string | Required | Ticker symbol (e.g. AAPL, GOOGL, QQQ, FXAIX). Case-insensitive. |

### `stock_quotes`

Get the latest quotes for multiple symbols in one call. Returns successful quotes and per-symbol errors separately.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `symbols` | array | Required | Array of ticker symbols (e.g. ['MSFT', 'QQQ', 'FXAIX']). |

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/stock-quotes
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/stock-quotes.js --help

## Get the latest quote for a stock, ETF, or mutual fund symbol.
node dist/bin/stock-quotes.js stock-quote <symbol>

## Get the latest quotes for multiple symbols in one call. Returns successful quotes and per-symbol errors separately.
node dist/bin/stock-quotes.js stock-quotes <symbols...>

## JSON output
node dist/bin/stock-quotes.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `STOCK_QUOTES_FINNHUB_API_KEY` | Finnhub API key. When set, Finnhub is used as the primary data source (higher rate limits). Free key at finnhub.io. |
