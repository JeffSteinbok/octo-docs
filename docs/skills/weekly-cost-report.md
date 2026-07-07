---
layout: default
title: Weekly Cost Report
nav_order: 3
nav_exclude: true
---

# 🧠 Weekly Cost Report

Generate the weekly LLM API cost report, render it to PDF, post to Discord, and commit.

## Prerequisites

A daily cron job (`enrich-sessions-daily`, ID `457e5a07-8fd3-4e59-95f9-e851d6b58a26`) runs at 4 AM PT every day to keep `~/.openclaw/logs/session-labels.csv` fresh. This enriches sessions with accurate category/subcategory labels **before** the weekly report runs at 5 AM Monday PT. You do not need to run enrich_sessions.py manually.

## Steps

1. **Refresh usage data** — Run:
   ```bash
   python3 /home/openclaw/.openclaw/agents/root/workspace/scripts/usage_summary.py --all
   ```

2. **Generate the Markdown report** — Run:
   ```bash
   bash /home/openclaw/.openclaw/agents/root/workspace/scripts/generate_cost_report.sh
   ```
   The script prints the path of the generated `.md` file.

3. **Render to HTML** — Use the `md_to_html` tool:
   - `input_path`: the MD file path from step 2
   - `output_path`: same path but `.html` extension
   - `template_path`: `/home/openclaw/git/octo/agents/root/reports/api-cost/template.html`

4. **Render to PDF** — Use the `html_to_pdf` tool:
   - `input_path`: the HTML file from step 3
   - `output_path`: same path but `.pdf` extension

5. **Post to Discord** — Use the `message` tool with **only** these parameters:
   - `action`: `"send"`
   - `target`: `"channel:1480763223392260116"`
   - `message`: brief summary text (date range, total cost, daily average, and top recommendation from Section 7)
   - `media`: the PDF file path (e.g. `/home/openclaw/git/octo/agents/root/reports/api-cost/2026-06-15.pdf`)
   - `mimeType`: `"application/pdf"`
   - `filename`: e.g. `"2026-06-15-weekly-llm-cost-report.pdf"`

   **Do not include any poll-related fields** (`pollDurationHours`, `pollOption`, `pollMulti`, etc.) — their presence causes the tool to reject the call with a "Poll fields require action poll" error even when empty.

6. **Commit and push** — Run:
   ```bash
   cd /home/openclaw/git/octo && git add agents/root/reports/api-cost/ && git commit -m 'chore: weekly cost report' && git push
   ```

## Report Structure

The generated Markdown report has these sections:

| Section | Description |
|---|---|
| Summary | KPI callout: 7-day total, daily average, monthly projection |
| 1. Token Cost Breakdown | Input/output/cache tokens, rates, and cost share |
| 2. Interactive vs Automated | Chat vs cron/hook cost split |
| 3. Cost by Agent | Per-agent cost, call count, model(s) used |
| 3b. Session Breakdown | Category/subcategory breakdown for expensive agents |
| 3c. Cron Job Summary | All cron jobs: runs, calls, cost |
| 4. Daily Trend | Day-by-day cost for the week |
| 5. Model Split | Per-model cost and call count |
| **7. Recommendations** | **Actionable insights (see below)** |
| 8. Pricing Reference | GitHub Copilot per-model rates |

## Section 7: Recommendations

`generate_cost_report.sh` automatically generates a **Recommendations** section with four subsections:

### 7.1 Top 3 Cost Drivers
Top 3 `(agent, category, subcategory)` combos by 7-day cost. Identifies which agents and task types are dominating spend.

### 7.2 Week-over-Week Cost Trend
Compares this week vs last week cost. Flags a ⚠️ spike if >25% increase or ✅ reduction if >20% decrease.

### 7.3 Automated Jobs That Could Use a Cheaper Model
Lists cron/hook/pipeline/subagent sessions that ran on Sonnet or Opus — with estimated savings if switched to Haiku 4.5. Sorted by 7-day cost, top 5 shown.

### 7.4 Sessions with Unusually High Token Counts
Flags sessions exceeding 3× the p75 token count (or 1M tokens minimum). Useful for catching runaway sessions or unexpectedly long tool chains.

## Session Label Enrichment

Session labels (used for Section 3b/3c breakdowns and Recommendations) come from two sources:

1. **`session-labels.csv`** — Written by `enrich_sessions.py` (daily at 4 AM via cron). Provides high/medium confidence labels using heuristics + optional LLM fallback.
2. **Inline heuristics** — `usage_summary.py` falls back to reading the session `.jsonl` file directly for unlabeled sessions.

The daily enrichment cron ensures label coverage is maximized before each Monday report.
