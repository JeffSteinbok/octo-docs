---
layout: default
title: Package Tracking
nav_order: 14
nav_exclude: true
---

# 📦 Package Tracking

Track packages from UPS, FedEx, USPS, and Amazon

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/package-tracking)

## Configuration Schema

_No plugin config schema documented._

## Example config

| Key | Type | Description |
|-----|------|-------------|
| `status_providers` | `string[]` | Paths to external ESM carrier status provider modules |

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

### `get_package_status`

Get live carrier status for a tracking number. Requires a carrier status provider to be configured via status_providers.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tracking_number` | string | Required | Package tracking number to check status for. |
| `carrier` | string | Optional | Optional carrier override: UPS, FedEx, USPS, or Amazon. |

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/package-tracking
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/package-tracking.js --help

## Look up a package by tracking number and return the carrier and tracking URL.
node dist/bin/package-tracking.js package-track <tracking_number> <carrier>

## Save a package to the tracking list, with an optional label.
node dist/bin/package-tracking.js package-add <tracking_number> <carrier> <label>

## Remove a saved package from the tracking list.
node dist/bin/package-tracking.js package-remove <tracking_number>

## List saved packages with carriers, tracking URLs, labels, and added dates.
node dist/bin/package-tracking.js package-list

## Scan text for package tracking numbers and identify their carriers.
node dist/bin/package-tracking.js package-scan <text>

## Get live carrier status for a tracking number. Requires a carrier status provider to be configured via status_providers.
node dist/bin/package-tracking.js get-package-status <tracking_number> <carrier>

## JSON output
node dist/bin/package-tracking.js <command> [args...] --json
```
