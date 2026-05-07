---
layout: default
title: WeightWatchers
nav_order: 18
nav_exclude: true
---

# 🍽️ WeightWatchers

Search foods, log meals, view diary and points budget via the unofficial WW API

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>jwt</code></td><td>string</td><td>Optional</td><td>WW API JWT token (preferred auth method).</td></tr>
    <tr><td><code>email</code></td><td>string</td><td>Optional</td><td>WW account email used for fallback login.</td></tr>
    <tr><td><code>password</code></td><td>string</td><td>Optional</td><td>WW account password used for fallback login.</td></tr>
    <tr><td><code>tld</code></td><td>string</td><td>Optional</td><td>WW regional TLD (for example `com`). Default: `com`.</td></tr>
  </tbody>
</table>

## Example config

Set WeightWatchers under `plugins.entries["weightwatchers"].config`:

```json
{
  "plugins": {
    "entries": {
      "weightwatchers": {
        "enabled": true,
        "config": {
          "jwt": "${WW_JWT}",
          "email": "${WW_EMAIL}",
          "password": "${WW_PASSWORD}",
          "tld": "${WW_TLD}"
        }
      }
    }
  }
}
```

`jwt` is preferred. `email` and `password` are only needed when the plugin has to log in and refresh auth automatically. If `tld` is omitted, the plugin defaults to `com`.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WW_JWT` | No | Backing value for plugin config `jwt |
| `WW_EMAIL` | No | Backing value for plugin config `email |
| `WW_PASSWORD` | No | Backing value for plugin config `password |
| `WW_TLD` | No | Backing value for plugin config `tld |

## Tools

### `ww_daily`

Get daily WW food diary. Returns tracked meals and points summary.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `date` | string | Optional | Date in YYYY-MM-DD format (default: today). |

### `ww_search`

Search the WW food database. Returns food IDs, points, and portion options needed for logging.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | Required | Food search query (e.g. 'grilled chicken breast'). |
| `limit` | integer | Optional | Max results to return (default: 10). |

### `ww_log`

Log a food item to the WW diary. Requires food_id, version_id, and portion_id from ww_search results.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `food_id` | string | Required | WW food ID (from ww_search results). |
| `version_id` | string | Required | Food version ID (from ww_search results). |
| `portion_id` | string | Required | Portion ID (from ww_search results). |
| `portion_size` | number | Optional | Portion multiplier (default: 1.0). |
| `date` | string | Optional | Date in YYYY-MM-DD format (default: today). |
| `meal_type` | string | Optional | Meal slot (default: snacks). |
| `source_type` | string | Optional | Food source type: WWFOOD, WWRECIPE, MEMBERFOOD (default: WWFOOD). |

### `ww_points`

Calculate WW SmartPoints offline from nutrition data. No authentication required.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `calories` | number | Required | Total calories. |
| `saturated_fat` | number | Required | Saturated fat in grams. |
| `sugar` | number | Required | Sugar in grams. |
| `protein` | number | Required | Protein in grams. |

### `ww_budget`

Get remaining WW points budget for a date. Shows daily and weekly allowances.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `date` | string | Optional | Date in YYYY-MM-DD format (default: today). |

### `ww_quick_add`

Quick-add a points value to the WW diary without specifying a food item. Useful when you know the points but not the exact food.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `points` | integer | Required | Number of SmartPoints to add. |
| `name` | string | Optional | Label for the diary entry (default: 'Quick Add'). |
| `meal_type` | string | Optional | Meal slot (default: snacks). |
| `date` | string | Optional | Date in YYYY-MM-DD format (default: today). |

### `ww_delete`

Delete a tracked food entry from the WW diary by its tracking ID. Use ww_daily to get tracking IDs.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tracking_id` | string | Required | Tracking ID of the diary entry to delete (from ww_daily results). |
| `date` | string | Optional | Date of the entry in YYYY-MM-DD format (default: today). |
