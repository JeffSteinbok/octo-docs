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

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/octo-satellite
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/octo-satellite.js --help

## JSON output
node dist/bin/octo-satellite.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `OCTO_SATELLITE_TOKEN` | Satellite API <redacted-bearer-token> |
| `OCTO_SATELLITE_BASE_URL` | Satellite base URL (default: http://localhost:9000) |
