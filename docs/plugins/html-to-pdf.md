---
layout: default
title: HTML to PDF
nav_order: 5
nav_exclude: true
---

# 📄 HTML to PDF

Convert HTML files to PDF using Chromium headless

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/html-to-pdf)

## Configuration Schema

_No plugin config schema documented._

## Example config

No configuration required.

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

## JSON output
node dist/bin/html-to-pdf.js <command> [args...] --json
```
