---
layout: default
title: Markdown to HTML
nav_order: 8
nav_exclude: true
---

# 📝 Markdown to HTML

Convert styled Markdown reports to HTML using a CSS template

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/md-to-html)

## Configuration Schema

_No plugin config schema documented._

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

## JSON output
node dist/bin/md-to-html.js <command> [args...] --json
```
