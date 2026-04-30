---
layout: default
title: OpenTable
parent: Plugins
nav_order: 7
---

# 🍽️ OpenTable

Look up restaurants, check availability, and monitor health on OpenTable

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/opentable)

### `opentable_lookup`

Look up an OpenTable restaurant by its URL slug (e.g. 'carbone-new-york' from opentable.com/r/carbone-new-york) to get its numeric restaurant ID.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `slug` | string | Required | Restaurant URL slug from opentable.com/r/<slug>. |

### `opentable_availability`

Check real-time availability for a restaurant on OpenTable. Returns available time slots with booking URLs.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `restaurant_id` | integer | Required | Numeric restaurant ID (from opentable_lookup). |
| `date` | string | Required | Date in YYYY-MM-DD format. |
| `party_size` | integer | Optional | Number of guests (default: 2). Default: `2`. |
| `time` | string | Optional | Preferred time in HH:MM format (default: 19:00). Default: `19:00`. |

### `opentable_heartbeat_check`

Check whether the OpenTable integration is healthy. Verifies both restaurant lookup and availability queries.
