---
layout: default
title: HTML to PDF
nav_order: 6
nav_exclude: true
---

# 📄 HTML to PDF

Convert HTML files to PDF using Chromium headless

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/html-to-pdf)

## Configuration Schema

_No plugin config schema documented._

## Example config

No configuration required.

## Tools

### `html_to_pdf`

Convert an HTML file to PDF using Chromium headless.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_path` | string | Required | Absolute path to the HTML file to render. |
| `output_path` | string | Required | Absolute path where the PDF should be saved (must end in .pdf). |
| `timeout_ms` | number | Optional | Max ms to wait for Chromium (default: 30000). |

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/html-to-pdf
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/html-to-pdf.js --help

## Convert an HTML file to PDF using Chromium headless.
node dist/bin/html-to-pdf.js html-to-pdf <input_path> <output_path> <timeout_ms>

## JSON output
node dist/bin/html-to-pdf.js <command> [args...] --json
```
