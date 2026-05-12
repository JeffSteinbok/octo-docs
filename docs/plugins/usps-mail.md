---
layout: default
title: USPS Mail Analyzer
nav_order: 15
nav_exclude: true
---

# 📬 USPS Mail Analyzer

Analyze USPS Informed Delivery digest emails: parse mailpiece scans, vision-classify, apply rules, write memory, send notifications

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/usps-mail)

## Configuration Schema

_No plugin config schema documented._

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/usps-mail
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/usps-mail.js --help

## JSON output
node dist/bin/usps-mail.js <command> [args...] --json
```
