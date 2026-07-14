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

## How Octo runs it

1. **Run the extraction script:**

2. **Read recent memory files** — scan files newer than 7 days from:
   - `<host-path>`
   - `<host-path>`

3. **Synthesize and deliver** — follow the synthesis and Discord DM format steps in the shared SKILL.md.

4. **Do not auto-commit from cron** — leave report files on disk for manual review.
