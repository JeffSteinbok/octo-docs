---
layout: default
title: Weekly Cost Report
nav_order: 3
nav_exclude: true
---

# 🧠 Weekly Cost Report

Generate the weekly LLM API cost report, render it to PDF, post to Discord, and commit.

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
   - `message`: brief summary text (date range, total cost, daily average)
   - `media`: the PDF file path (e.g. `/home/openclaw/git/octo/agents/root/reports/api-cost/2026-06-15.pdf`)
   - `mimeType`: `"application/pdf"`
   - `filename`: e.g. `"2026-06-15-weekly-llm-cost-report.pdf"`

   **Do not include any poll-related fields** (`pollDurationHours`, `pollOption`, `pollMulti`, etc.) — their presence causes the tool to reject the call with a "Poll fields require action poll" error even when empty.

6. **Commit and push** — Run:
   ```bash
   cd /home/openclaw/git/octo && git add agents/root/reports/api-cost/ && git commit -m 'chore: weekly cost report' && git push
   ```
