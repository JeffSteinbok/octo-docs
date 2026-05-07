---
layout: default
title: Stock Quotes
nav_order: 15
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
