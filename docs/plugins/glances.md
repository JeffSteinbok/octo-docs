---
layout: default
title: glances
nav_order: 4
nav_exclude: true
---

# glances

Read CPU, memory, disk, and summary metrics from a Glances server

> **Source:** [JeffSteinbok/openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/glances)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>url</code></td><td>string</td><td>Optional</td><td>Base URL for the Glances web server, e.g. http://127.0.0.1:61208. Default: `http://127.0.0.1:61208`.</td></tr>
  </tbody>
</table>

## Example config

Set Glances under `plugins.entries["glances"].config`:

```json
{
  "plugins": {
    "entries": {
      "glances": {
        "enabled": true,
        "config": {
          "url": "http://127.0.0.1:61208"
        }
      }
    }
  }
}
```

If omitted, the plugin defaults to `http://127.0.0.1:61208`.

## Tools

### `glances_summary_get`

Get a compact Glances summary with CPU, memory, uptime, and one filesystem.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mount_point` | string | Optional | Filesystem mount point to summarize (default: /). Default: `/`. |

### `glances_cpu_get`

Get current CPU metrics from Glances.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `include_percpu` | boolean | Optional | Include per-core CPU usage from the quicklook endpoint. Default: `False`. |

### `glances_memory_get`

Get current memory usage metrics from Glances.

### `glances_disk_get`

Get filesystem usage metrics for one mount point from Glances.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mount_point` | string | Optional | Filesystem mount point to query (default: /). Default: `/`. |

### `glances_endpoint_get`

Fetch a raw JSON payload from a specific Glances /api/3 endpoint.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | string | Required | Glances API path beginning with /api/3/ (for example /api/3/uptime). |

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/glances
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/glances.js --help

## Get a compact Glances summary with CPU, memory, uptime, and one filesystem.
node dist/bin/glances.js glances-summary-get <mount_point>

## Get current CPU metrics from Glances.
node dist/bin/glances.js glances-cpu-get <include_percpu>

## Get current memory usage metrics from Glances.
node dist/bin/glances.js glances-memory-get

## Get filesystem usage metrics for one mount point from Glances.
node dist/bin/glances.js glances-disk-get <mount_point>

## Fetch a raw JSON payload from a specific Glances /api/3 endpoint.
node dist/bin/glances.js glances-endpoint-get <path>

## JSON output
node dist/bin/glances.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `GLANCES_URL` | Base URL for the Glances web server, e.g. http://127.0.0.1:61208 |
