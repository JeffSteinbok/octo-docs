---
layout: default
title: Agent Review
nav_order: 1
nav_exclude: true
---

# 🔍 Agent Review

Octo's thin wrapper around the shared `agent-review` skill in `openclaw-hub`.

- Shared implementation: `<host-path>`
- Octo-specific report output: `<host-path>`
- Issue repo: `JeffSteinbok/octo`
- Delivery target: Jeff's Discord DM (`user:<redacted>`)

## What lives where

### Shared in openclaw-hub

- `scripts/agent_review.py` — trajectory + memory scanner, fingerprint dedup, issue filing
- `SKILL.md` — full CLI reference, output schema, synthesis steps, Discord format
- `README.md`

### Local to Octo

- Report output under `agents/root/reports/agent-review/`
- The `agent-review-weekly` cron job
- Issue target (`JeffSteinbok/octo`) and Discord DM target

## Synthesis rules

These rules reinforce the grounding constraint from the shared SKILL.md. The
root agent **must** follow them when composing the weekly delivery message.

- Surface only findings traceable to `tool_errors`, `cron_errors`,
  `memory_flags`, or `source_health.issues` in the JSON output.
- If those fields are all empty/minimal → send a short **"clean week"** note.
  Do not fill the absence of real findings with invented suggestions.
- **Never recommend a schedule change** unless the JSON contains a
  `cron_job_schedules` block with the job's actual schedule expression.
  The script currently never emits that block, so schedule suggestions are
  always prohibited until a future enhancement adds them.
- **Never state or estimate run counts or dollar costs** (e.g. "ran 73x/week",
  "saves $0.87/week") — the script has no such data.
- `cron_stats.total_cron_sessions` counts session-level errors, not per-job
  run frequencies. Do **not** use it to infer how often a named job runs.
- `source_health` entries (e.g. "WARNING: 0 events extracted") describe scan
  quality, not operational metrics. Do not derive cost/schedule claims from
  them.

## How Octo runs it

1. **Run the extraction script:**

2. **Read recent memory files** — scan files newer than 7 days from:
   - `<host-path>`
   - `<host-path>`

3. **Synthesize and deliver** — follow the synthesis and Discord DM format steps in the shared SKILL.md.

4. **Do not auto-commit from cron** — leave report files on disk for manual review.


> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/skills/agent-review)
