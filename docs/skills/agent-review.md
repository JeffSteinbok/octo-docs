---
layout: default
title: Agent Review
nav_order: 1
nav_exclude: true
---

# 🔍 Agent Review

Perform a weekly self-improvement analysis of Octo's own session transcripts, cron run history, and memory files. Identify what's broken, friction-heavy, or missing, then deliver a prioritized summary to Jeff.

## Steps

1. **Run the extraction script** — Execute:
   ```bash
   python3 /home/openclaw/git/octo/agents/root/scripts/agent_review.py --days 7 --file-issues --issue-repo JeffSteinbok/octo --issue-min-count 3 --issue-min-runs 2 --issue-max-open-per-run 3
   ```
   The script scans trajectory files and memory files, updates fingerprint state at `~/.openclaw/state/agent-review/fingerprints.json`, takes a lightweight local backup under `~/.openclaw/state/agent-review/backups/`, and prints a structured JSON summary to stdout.

2. **Read recent memory files** — For additional context, read the last 7 days of daily memory notes from both agents (files match `YYYY-MM-DD.md` and will be dated within the past week):
   - `/home/openclaw/.openclaw/agents/main/memory/` — scan files newer than 7 days
   - `/home/openclaw/.openclaw/agents/root/memory/` — scan files newer than 7 days

3. **Synthesize findings** — Review the script output and memory files together. Identify and rank:
   - **Tool failures** — which tools errored most frequently, with representative error messages
   - **Cron errors** — which cron jobs failed, errored, or timed out most often
   - **User corrections** — places where Jeff had to correct Octo or re-ask (look for "wrong", "no, ", "actually", "correction", correction-related memory notes)
   - **Repeated friction** — tasks Octo struggled with or took multiple retries
   - **Capability gaps** — things Jeff asked for that Octo couldn't do or had to partially refuse

4. **Compose the Discord DM** — Send ONE Discord DM to `target='user:819456855092494356'` with the weekly review. Format:

   ```
   🔍 **Weekly Agent Review** — week of <date>

   **Top findings this week:**

   🔴 Critical (fix ASAP)
   - [item]: [brief description + frequency]

   🟡 High priority
   - [item]: [brief description + frequency]

   🟢 Low priority / ideas
   - [item]: [brief description]

   **Cron health:** X/Y jobs ran clean · Z had errors
   ```

   Keep it scannable — bullet points, no walls of text. Omit any section that has nothing to report. If there are zero issues across all categories, send a brief "✅ Clean week — nothing to flag" message.

5. **Issue filing policy** — The script only auto-files issues for recurring, high-confidence findings (count threshold + recurrence threshold) and deduplicates using fingerprints in local state. Do not file issues manually unless explicitly requested.

6. **Do not auto-commit from cron** — The weekly review job should not run `git commit`/`git push`. Leave report files on disk for manual review and commit.
