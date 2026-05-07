---
layout: default
title: Octo Satellite
nav_order: 10
nav_exclude: true
---

# 🛰️ Octo Satellite

OpenClaw toolset providing structured access to the [Octo Satellite](https://github.com/JeffSteinbok/octo-satellite) service. Exposes Amazon order management and Monarch Money financial tools.

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>token</code></td><td>string</td><td>Optional</td><td>Satellite API &lt;redacted-bearer-token&gt;.</td></tr>
    <tr><td><code>baseUrl</code></td><td>string</td><td>Optional</td><td>Satellite base URL (default: http://localhost:9000).</td></tr>
  </tbody>
</table>

## Example config

Set Octo Satellite under `plugins.entries["octo-satellite"].config`:

```json
{
  "plugins": {
    "entries": {
      "octo-satellite": {
        "enabled": true,
        "config": {
          "token": "${OCTO_SATELLITE_TOKEN}",
          "baseUrl": "http://localhost:9000"
        }
      }
    }
  }
}
```

## Tools

### `amazon_list_orders`

List or search Amazon orders with pagination (10 per page). Optionally filter by search query. Returns order id, date, total, status, item titles, total count, and pagination info.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `q` | string | Optional | Optional search query to filter orders. |
| `page` | integer | Optional | Page number, 1-based (default: 1, 10 orders per page). |

### `amazon_get_order`

Get full details and tracking info for a specific Amazon order. Returns items, quantities, prices, shipping address, and carrier tracking.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `order_id` | string | Required | Amazon order ID (e.g. 113-1234567-8901234). |

### `amazon_search`

Search Amazon products by query string. Returns product titles, prices, ratings, ASINs, and pagination info.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `q` | string | Required | Search query. |
| `page` | integer | Optional | Page number, 1-based (default: 1). |

### `amazon_get_product`

Get product details by ASIN. Returns title, price, rating, features, availability, and more.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asin` | string | Required | Amazon product identifier (e.g. B0FQFB8FMG). |

### `amazon_get_cart`

View current Amazon cart contents.

### `amazon_add_to_cart`

Add a product to the Amazon cart by ASIN.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asin` | string | Required | Amazon product identifier (e.g. B0FQFB8FMG). |

### `amazon_remove_from_cart`

Remove an item from the Amazon cart by item_id (the ephemeral cart item ID from amazon_get_cart).

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `item_id` | string | Required | Cart item ID (from amazon_get_cart response). |

### `monarch_get_accounts`

Get financial accounts and balances from Monarch Money, grouped by type (Investments, Cash, Credit Cards, etc). Each account shows name, balance, institution, and last updated timestamp.

### `monarch_get_net_worth`

Get net worth summary from Monarch Money. Returns total assets, total liabilities, and net worth.

### `monarch_get_spending`

Get spending trends from Monarch Money — income, expenses, and savings broken down by month. Defaults to the last 3 months.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `months` | integer | Optional | Number of months to look back (default: 3). |
