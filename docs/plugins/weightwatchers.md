---
layout: default
title: Weightwatchers
parent: Plugins
nav_order: 16
---

🍽️ Weightwatchers

Search foods, log meals, view your food diary, and manage points budget via the unofficial Weightwatchers (WW) API.

### ww_daily

Get daily WW food diary. Returns tracked meals and points summary.

| Name  | Type   | Description                                      |
|-------|--------|--------------------------------------------------|
| date  | string | Date in YYYY-MM-DD format (default: today)       |

### ww_search

Search the WW food database. Returns food IDs, points, and portion options needed for logging.

| Name  | Type    | Description                                      |
|-------|---------|--------------------------------------------------|
| query | string  | Food search query (e.g. 'grilled chicken breast')|
| limit | integer | Max results to return (default: 10)              |

### ww_log

Log a food item to the WW diary. Requires food_id, version_id, and portion_id from ww_search results.

| Name         | Type    | Description                                                                                   |
|--------------|---------|-----------------------------------------------------------------------------------------------|
| food_id      | string  | WW food ID (from ww_search results)                                                           |
| portion_id   | string  | Portion ID (from ww_search results)                                                           |
| version_id   | string  | Food version ID (from ww_search results)                                                      |
| portion_size | number  | Portion multiplier (default: 1.0)                                                             |
| date         | string  | Date in YYYY-MM-DD format (default: today)                                                    |
| meal_type    | string  | Meal slot to log to (default: snacks). Options: breakfast, lunch, dinner, snacks              |
| source_type  | string  | Food source type: WWFOOD, WWRECIPE, MEMBERFOOD, etc. (default: WWFOOD)                       |

### ww_points

Calculate WW SmartPoints offline from nutrition data. No authentication required.

| Name          | Type   | Description                |
|---------------|--------|----------------------------|
| calories      | number | Total calories             |
| saturated_fat | number | Saturated fat in grams     |
| sugar         | number | Sugar in grams             |
| protein       | number | Protein in grams           |

### ww_budget

Get remaining WW points budget for a date. Shows daily and weekly allowances.

| Name  | Type   | Description                                      |
|-------|--------|--------------------------------------------------|
| date  | string | Date in YYYY-MM-DD format (default: today)       |

### ww_quick_add

Quick-add a points value to the WW diary without specifying a food item. Useful when you know the points but not the exact food.

| Name      | Type    | Description                                                                 |
|-----------|---------|-----------------------------------------------------------------------------|
| points    | integer | Number of SmartPoints to add                                                 |
| name      | string  | Label for the diary entry (default: 'Quick Add')                             |
| meal_type | string  | Meal slot to log to (default: snacks). Options: breakfast, lunch, dinner, snacks |
| date      | string  | Date in YYYY-MM-DD format (default: today)                                   |

### ww_delete

Delete a tracked food entry from the WW diary by its tracking ID. Use ww_daily to get tracking IDs.

| Name        | Type   | Description                                                    |
|-------------|--------|----------------------------------------------------------------|
| tracking_id | string | Tracking ID of the diary entry to delete (from ww_daily results)|
| date        | string | Date of the entry in YYYY-MM-DD format (default: today)        |
