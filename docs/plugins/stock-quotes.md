---
layout: default
title: Stock Quotes
nav_order: 16
nav_exclude: true
---

# 📈 Stock Quotes

Fetch current stock, ETF, and mutual fund quotes

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/stock-quotes)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>finnhubApiKey</code></td><td>string</td><td>Optional</td><td>Optional Finnhub API key.</td></tr>
  </tbody>
</table>

## Example config

Set options in `plugins.entries["stock-quotes"].config`:

```json
{
  "plugins": {
    "entries": {
      "stock-quotes": {
        "enabled": true,
        "config": {
          "finnhubApiKey": "your-finnhub-api-key"
        }
      }
    }
  }
}
```

### Default behavior

The plugin works out of the box with no configuration. It fetches stocks, ETFs, and mutual funds from Yahoo Finance without requiring an API key. If `finnhubApiKey` is configured, the plugin tries Finnhub first and falls back to Yahoo Finance automatically.

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

## CLI Usage

The stock-quotes plugin can also run as a standalone command-line tool. No gateway required.

### Setup

```bash
cd plugins/stock-quotes
npm install && npm run build
```

### Commands

```bash
# Get a single quote
node dist/bin/stock-quotes.js stock-quote AAPL
# Output: AAPL  $198.11  ▲ +1.23 (+0.63%)  [REGULAR]

# Get multiple quotes
node dist/bin/stock-quotes.js stock-quotes MSFT GOOGL QQQ
# Output:
# MSFT   $420.77  ▲ +6.9 (+1.67%)   [REGULAR]
# GOOGL  $397.99  ▲ +0.17 (+0.04%)  [REGULAR]
# QQQ    $694.94  ▼ -0.81 (-0.12%)  [REGULAR]

# JSON output
node dist/bin/stock-quotes.js stock-quote AAPL --json

# Show help
node dist/bin/stock-quotes.js --help
```

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `STOCK_QUOTES_FINNHUB_API_KEY` | No | Optional Finnhub API key for premium data. Without it, falls back to Yahoo Finance. |

### Global install

After building, you can link the CLI globally:

```bash
npm link
stock-quotes stock-quote TSLA
```
