---
layout: default
title: Package Tracking
parent: Plugins
nav_order: 12
---

# 📦 Package Tracking

Track packages from UPS, FedEx, USPS, and Amazon

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/package-tracking)

## Tools

### `package_track`

Look up a package by tracking number and return the carrier and tracking URL.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tracking_number` | string | Required | Package tracking number (e.g., 1Z999AA10123456784, 940000000000000000000, TBA012345678901US). |
| `carrier` | string | Optional | Optional carrier override: UPS, FedEx, USPS, or Amazon. |

### `package_add`

Save a package to the tracking list, with an optional label.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tracking_number` | string | Required | Package tracking number. |
| `carrier` | string | Optional | Optional carrier override: UPS, FedEx, USPS, or Amazon. |
| `label` | string | Optional | Optional label/description for the package. |

### `package_remove`

Remove a saved package from the tracking list.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tracking_number` | string | Required | Package tracking number to remove. |

### `package_list`

List saved packages with carriers, tracking URLs, labels, and added dates.

### `package_scan`

Scan text for package tracking numbers and identify their carriers.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | string | Required | Text to scan for tracking numbers (e.g., email body). |
