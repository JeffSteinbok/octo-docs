---
layout: default
title: Weekly Cost Report
nav_order: 3
nav_exclude: true
---

# 📊 Weekly Cost Report

Every Monday at 5 AM PT, the root agent automatically generates a full LLM cost report for the past 7 days, renders it to PDF, and posts it to Discord.

## What it produces

The report is broken into six sections:

| Section | What it shows |
|---------|--------------|
| **Summary KPIs** | 7-day total, daily average, monthly projection |
| **Token cost breakdown** | Input / output / cache-read / cache-write volumes and costs |
| **Interactive vs Automated** | Split between live chat sessions and cron jobs |
| **Cost by agent** | Per-agent spend, call count, models used |
| **Session breakdown** | Top agents drilled down by task/job category |
| **Daily trend** | Day-by-day cost across the 7-day window |
| **Model split** | Cost and call share across all models used |
| **Pricing reference** | Current GitHub Copilot per-token rates for all active models |

## How it works

The pipeline is fully automated and token-free — no LLM is invoked during report generation:

1. **Usage CSV refresh** — `usage_summary.py` reads raw OpenClaw usage logs (`~/.openclaw/logs/`) and writes structured per-agent, per-model, per-day CSVs
2. **Markdown generation** — `generate_cost_report.sh` reads the CSVs and emits a structured Markdown report
3. **HTML render** — the root agent calls the `md_to_html` plugin tool with a custom HTML template
4. **PDF render** — the root agent calls the `html_to_pdf` plugin tool
5. **Discord post** — the PDF is posted to the `#root` Discord channel with a brief text summary
6. **Git commit** — the Markdown and rendered files are committed to the repo for a permanent audit trail

## Cron schedule

```
0 5 * * 1  America/Los_Angeles   (Monday 5 AM PT)
```

Runs under the root agent, which has `exec` access to run the shell scripts.

## Why this approach

All the heavy lifting (CSV parsing, math, Markdown formatting) happens in a plain Python script — zero tokens. The root agent only handles the final rendering and posting steps, where tool calls are genuinely needed. This keeps the weekly report cost negligible.

The session-level CSV (`usage-sessions.csv`) lets the report attribute costs to specific cron jobs and chat sessions, making it easy to spot which recurring task is the biggest spender.

