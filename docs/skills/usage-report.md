---
layout: default
title: Usage Report
nav_order: 3
nav_exclude: true
---

# 📊 Usage Report

This is Octo's thin wrapper around the shared `usage-report` skill in `openclaw-hub`.

- Shared implementation: `/home/openclaw/git/openclaw-hub/skills/usage-report`
- Octo-specific output dir: `/home/openclaw/git/octo/agents/root/reports/api-cost`
- Delivery target: `#root`
- Daily label enrichment cron: `usage-enrich-sessions`
- Weekly report cron: `usage-weekly-report`

## What lives where

### Shared in openclaw-hub

These files are canonical and reusable across OpenClaw installs:

- `scripts/usage_summary.py`
- `scripts/generate_usage_report.sh`
- `assets/template.html`
- generic `SKILL.md` + `README.md`

### Local to Octo

These stay Octo-specific:

- report output under `agents/root/reports/api-cost/`
- the `usage-enrich-sessions` and `usage-weekly-report` cron jobs
- the Discord destination (`#root`)
- any local env-var overrides

## How Octo runs it

1. Refresh usage CSVs:
   ```bash
   python3 /home/openclaw/git/openclaw-hub/skills/usage-report/scripts/usage_summary.py --all
   ```

2. Generate the Markdown report:
   ```bash
   OPENCLAW_LOGS_DIR=/home/openclaw/.openclaw/logs \
   USAGE_REPORT_OUT_DIR=/home/openclaw/git/octo/agents/root/reports/api-cost \
   USAGE_REPORT_TEMPLATE=/home/openclaw/git/openclaw-hub/skills/usage-report/assets/template.html \
   bash /home/openclaw/git/openclaw-hub/skills/usage-report/scripts/generate_usage_report.sh
   ```

3. Render to HTML with `md_to_html`
4. Render to PDF with `html_to_pdf`
5. Post the PDF to `#root`
6. Commit and push `agents/root/reports/api-cost/`

## Report contents

The generated report includes:

- total weekly cost, daily average, monthly projection
- token breakdowns (input, output, cache read, cache write, total)
- interactive vs automated spend
- cost by agent
- per-session and cron breakdowns
- daily trend
- model split
- recommendations
- pricing reference

## Token visibility

The report now surfaces token counts in the summary and in the per-agent and cron summary tables, not just cost.

## Session label enrichment

Session labels for the breakdown sections come from:

1. `session-labels.csv` written daily by `enrich_sessions.py`
2. inline heuristics in `usage_summary.py` for any unlabeled sessions

That daily enrichment is why `usage-enrich-sessions` runs before the weekly report.

## Public docs / website

The public website entry for this skill is generated from this wrapper and points back to the shared source in `openclaw-hub`.

Source: <https://github.com/JeffSteinbok/openclaw-hub/tree/main/skills/usage-report>
