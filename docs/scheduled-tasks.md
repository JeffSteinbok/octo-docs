---
layout: default
title: Scheduled Tasks
nav_order: 9
---

# Scheduled Tasks

Scheduled tasks are background jobs that run without direct user input. The public bundle only includes infrastructure jobs that keep Octo healthy or maintained.

Feature-specific reminders, briefs, personal nudges, and other user-facing automations are intentionally excluded from the public bundle and from this page.

Octo currently publishes **7 infrastructure tasks**.

## Infrastructure Tasks

| Task | Schedule | What it does |
|------|----------|--------------|
| `config-backup` | Every 24 hours | Runs the config-backup plugin to commit OpenClaw configuration changes to git and report failures. |
| `plugin-health-check` | `0 9 * * *` (America/Los_Angeles) | Daily smoke test that calls one tool from every configured plugin and reports pass/fail to Discord. |
| `Lobster changelog weekly scan` | `0 9 * * 1` (America/Los_Angeles) | Scans the Lobster changelog for new ideas worth adopting and reports only when something changed. |
| `Log rotation - openclaw.log` | `0 3 * * *` (America/Los_Angeles) | Runs copy-truncate rotation for the main OpenClaw log and keeps a bounded archive set. |
| `Nightly browser recycle` | `0 4 * * *` (America/Los_Angeles) | Restarts the headless Camoufox browser instance overnight to reclaim memory and clear stale sessions. |
| `openclaw-upgrade-readiness-check` | `0 10 * * *` (America/Los_Angeles) | Checks for new OpenClaw releases and evaluates whether an upgrade is safe based on changelog and config compatibility. |
| `agent-review-weekly` | `0 6 * * 1` (America/Los_Angeles) | Scans session transcripts, tool failures, and memory files for patterns; deduplicates recurring findings via fingerprint state, auto-files guarded GitHub issues, and delivers a prioritized weekly report via Discord DM. |
