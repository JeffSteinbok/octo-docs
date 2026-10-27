---
layout: default
title: Scheduled Tasks
nav_order: 9
---

# Scheduled Tasks

Scheduled tasks are jobs that OpenClaw's scheduler (cron) runs on a timer, without anyone asking. For work triggered by outside events instead, see [Hooks](hooks).

This page lists the infrastructure jobs that keep Octo healthy and maintained. Personal jobs, such as reminders, briefings and nudges, aren't published.

Octo publishes **18 infrastructure tasks**.

## Infrastructure Tasks

Times are Pacific (PT). A job with no time zone of its own runs on the Mac mini's clock, which is also set to Pacific. Jobs marked "No model call" run a script directly, without an AI model.

| Task | Schedule | What it does |
|------|----------|--------------|
| `agent-review-labels` | Sundays at 10:00 PM PT (`0 22 * * 0`) | Script that asks the decision model which kind each new agent-review issue is and whether it duplicates an existing one. Log-only: it records the answers and changes nothing. |
| `agent-review-weekly` | Sundays at 9:00 PM PT (`0 21 * * 0`) | Runs the Agent Review skill: reviews the week's session transcripts, tool failures and memory files, files a GitHub issue for each new recurring problem (skipping ones already filed), and sends a prioritized report by Discord DM. |
| `config-backup` | Daily | Runs the Config Backup plugin to commit changes to OpenClaw's config and the agent workspaces to Git, and reports failures. |
| `decision-review-weekly` | Mondays at 9:00 AM PT (`0 9 * * 1`) | Texts the owner the past week's events where a log-only decision-model gate disagreed with current behavior, for review. No model call. |
| `docs-validate-weekly` | Mondays at 6:00 AM PT (`0 6 * * 1`) | Builds this docs site and checks it against live config (missing plugins, jobs and services, empty tables, unknown schedules, broken links); files a GitHub issue for each new warning. |
| `heartbeat-main` | Every 2 hours | Wakes the main agent to work through its HEARTBEAT.md checklist and follow up on anything pending. |
| `Lobster changelog weekly scan` | Mondays at 9:00 AM PT (`0 9 * * 1`) | Scans the Lobster changelog for ideas worth adopting and reports only when something is new. |
| `Log rotation - openclaw.log` | Daily at 3:00 AM PT (`0 3 * * *`) | Script that copy-truncates the gateway log past 50 MB and keeps 7 archives (newest uncompressed, older gzipped). No model call. |
| `macos-update-check` | Daily at 10:05 AM PT (`5 10 * * *`) | Script that checks `softwareupdate -l` on the Mac mini and announces each pending macOS update once on Discord. No model call. |
| `Memory Dreaming Promotion` | Daily at 3:00 AM (`0 3 * * *`) | Nightly memory "dreaming" sweep that promotes lasting facts from recent notes and sessions into each agent's MEMORY.md. See [Memory](memory). |
| `Nightly browser recycle` | Daily at 4:00 AM PT (`0 4 * * *`) | Restarts the headless Camoufox browser overnight to free memory and clear stale sessions. |
| `openclaw-upgrade-readiness-check` | Daily at 10:00 AM PT (`0 10 * * *`) | Script that checks npm for a new stable OpenClaw release and announces each new release once with an upgrade-readiness checklist. No model call. |
| `plugin-health-check` | Daily at 9:00 AM PT (`0 9 * * *`) | Calls one tool from every configured plugin and reports which passed and failed to Discord. |
| `readiness-check` | Repeating interval | Script that checks the Gateway's /readyz every 5 minutes and posts to the status channel when a check is failing (such as a refused agent database) and when it recovers. No model call. |
| `scratch-prune` | Daily at 4:30 AM PT (`30 4 * * *`) | Script that deletes files older than 30 days from the agents' scratch folders, where they keep downloads and temp files. Silent; no model call. |
| `usage-enrich-sessions` | Daily at 4:00 AM PT (`0 4 * * *`) | Labels the day's sessions with a category and subcategory so the weekly usage report can break costs down accurately. |
| `usage-weekly-report` | Mondays at 5:00 AM PT (`0 5 * * 1`) | Runs the Usage Report skill: builds the weekly model API usage and cost report, renders it to PDF, posts it to Discord and commits it. |
| `weekly-full-backup` | Sundays at 2:00 AM PT (`0 2 * * 0`) | Copies the whole OpenClaw state directory, secrets included, into a timestamped local backup, compresses older backups, and puts an encrypted copy in OneDrive (newest four kept). |
