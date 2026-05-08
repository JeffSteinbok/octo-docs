---
layout: default
title: Markdown to HTML
nav_order: 9
nav_exclude: true
---

# 📝 Markdown to HTML

Convert styled Markdown reports to HTML using a CSS template

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/md-to-html)

## Configuration Schema

_No plugin config schema documented._

## Tools

### `md_to_html`

Convert a styled Markdown file to HTML using a CSS template. Supports fenced blocks (kpi, callout, svg, two-col), table row class hints, and inline text transforms. Call md_to_html_syntax for full syntax reference.

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_path` | string | Required | Absolute path to the Markdown file to render. |
| `output_path` | string | Required | Absolute path where the HTML should be saved (must end in .html). |
| `template_path` | string | Required | Absolute path to an HTML template containing CSS <style> blocks. |

### `md_to_html_syntax`

Returns the full Markdown syntax reference for the md_to_html renderer. Call this to learn what fenced blocks, inline hints, table row hints, and directives are supported.

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/md-to-html
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/md-to-html.js --help

## Convert a styled Markdown file to HTML using a CSS template. Supports fenced blocks (kpi, callout, svg, two-col), table row class hints, and inline text transforms. Call md_to_html_syntax for full syntax reference.
node dist/bin/md-to-html.js md-to-html <input_path> <output_path> <template_path>

## Returns the full Markdown syntax reference for the md_to_html renderer. Call this to learn what fenced blocks, inline hints, table row hints, and directives are supported.
node dist/bin/md-to-html.js md-to-html-syntax

## JSON output
node dist/bin/md-to-html.js <command> [args...] --json
```
