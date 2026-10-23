---
layout: default
title: Scheduled Tasks
nav_order: 9
---

# Scheduled Tasks

Scheduled tasks are background jobs that run without direct user input. The public bundle only includes infrastructure jobs that keep Octo healthy or maintained.

Feature-specific reminders, briefs, personal nudges, and other user-facing automations are intentionally excluded from the public bundle and from this page.

Octo currently publishes **14 infrastructure tasks**.

## Infrastructure Tasks

Times are Pacific (PT). Jobs without a listed time zone run on the gateway host's clock, which is also Pacific.

| Task | Schedule | What it does |
|------|----------|--------------|
| `agent-review-weekly` | Sundays at 9:00 PM PT (`0 21 * * 0`) | Scans session transcripts, tool failures, and memory files for patterns; deduplicates recurring findings via fingerprint state, auto-files guarded GitHub issues, and delivers a prioritized weekly report via Discord DM. |
| `config-backup` | Daily | Runs the config-backup plugin to commit OpenClaw configuration changes to git and report failures. |
| `docs-validate-weekly` | Mondays at 6:00 AM PT (`0 6 * * 1`) | Renders the docs site and checks the manifest, jobs, services and rendered pages (empty tables, unknown schedules, broken links) against live config; files deduplicated GitHub issues for warnings. |
| `heartbeat-main` | Every 2 hours | Periodic heartbeat turn for the main agent to work through its HEARTBEAT checklist and follow up on anything pending. |
| `Lobster changelog weekly scan` | Mondays at 9:00 AM PT (`0 9 * * 1`) | Scans the Lobster changelog for new ideas worth adopting and reports only when something changed. |
| `Log rotation - openclaw.log` | Daily at 3:00 AM PT (`0 3 * * *`) | Script that copy-truncates the gateway log past 50 MB and keeps 7 archives (newest uncompressed, older gzipped). No model call. |
| `macos-update-check` | Daily at 10:05 AM PT (`5 10 * * *`) | Script that checks `softwareupdate -l` on the Mac mini and announces each pending macOS update once to the upgrades channel. No model call. |
| `Memory Dreaming Promotion` | Daily at 3:00 AM (`0 3 * * *`) | Nightly memory "dreaming" pass that promotes durable notes from recent sessions into long-term memory. |
| `Nightly browser recycle` | Daily at 4:00 AM PT (`0 4 * * *`) | Restarts the headless Camoufox browser instance overnight to reclaim memory and clear stale sessions. |
| `openclaw-upgrade-readiness-check` | Daily at 10:00 AM PT (`0 10 * * *`) | Script that checks npm for a new stable OpenClaw release and announces each new release once with an upgrade-readiness checklist. No model call. |
| `plugin-health-check` | Daily at 9:00 AM PT (`0 9 * * *`) | Daily smoke test that calls one tool from every configured plugin and reports pass/fail to Discord. |
| `usage-enrich-sessions` | Daily at 4:00 AM PT (`0 4 * * *`) | Runs daily at 4 AM PT to enrich session labels with category/subcategory metadata, improving the accuracy of the weekly usage report breakdown. |
| `usage-weekly-report` | Mondays at 5:00 AM PT (`0 5 * * 1`) | Generates the weekly LLM API usage and cost report, renders it to PDF, posts to Discord, and commits the artifacts. |
| `weekly-full-backup` | Sundays at 2:00 AM PT (`0 2 * * 0`) | Copies the whole OpenClaw state directory, secrets included, into a timestamped local backup and compresses older backups. |
