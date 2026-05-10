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

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>status_providers</code></td><td>string[]</td><td>Optional</td><td>Paths to external ESM carrier status provider modules.</td></tr>
  </tbody>
</table>

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

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `PACKAGE_TRACKING_STATUS_PROVIDERS` | Paths to external ESM carrier status provider modules |
