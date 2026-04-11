---
layout: default
title: Opentable
parent: Plugins
nav_order: 8
---

# 🍽️ Opentable

Check restaurant availability on OpenTable.

### opentable_lookup

Look up an OpenTable restaurant by its URL slug (e.g. 'carbone-new-york' from opentable.com/r/carbone-new-york) to get its numeric restaurant ID.

| Name  | Type   | Description                                      |
|-------|--------|--------------------------------------------------|
| slug  | string | Restaurant URL slug from opentable.com/r/&lt;slug&gt; |

### opentable_availability

Check real-time availability for a restaurant on OpenTable. Returns available time slots with booking URLs.

| Name          | Type    | Description                                 |
|---------------|---------|---------------------------------------------|
| restaurant_id | integer | Numeric restaurant ID (from opentable_lookup) |
| date          | string  | Date in YYYY-MM-DD format                   |
| party_size    | integer | Number of guests (default: 2)               |
| time          | string  | Preferred time in HH:MM format (default: 19:00) |
