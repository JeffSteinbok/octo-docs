---
layout: default
title: restaurant-cli
nav_order: 15
nav_exclude: true
---

# 🍽️ restaurant-cli

Pluggable reservation booking via Resy, OpenTable, Tock, and other providers

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>resy_apiKey</code></td><td>string</td><td>Optional</td><td></td></tr>
    <tr><td><code>resy_authToken</code></td><td>string</td><td>Optional</td><td></td></tr>
  </tbody>
</table>

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/restaurant-cli
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/restaurant-cli.js --help

## JSON output
node dist/bin/restaurant-cli.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `RESTAURANT_CLI_RESY_API_KEY` |  |
| `RESTAURANT_CLI_RESY_AUTH_TOKEN` |  |
