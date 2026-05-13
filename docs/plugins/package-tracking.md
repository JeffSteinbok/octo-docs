---
layout: default
title: Package Tracking
nav_order: 14
nav_exclude: true
---

# 📦 Package Tracking

Track packages from UPS, FedEx, USPS, and Amazon

> **Source:** [JeffSteinbok/openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/package-tracking)

## Configuration Schema

_No plugin config schema documented._

## Example config

| Key | Type | Description |
|-----|------|-------------|
| `status_providers` | `string[]` | Paths to external ESM carrier status provider modules (optional — built-ins work without this) |

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

## JSON output
node dist/bin/package-tracking.js <command> [args...] --json
```
