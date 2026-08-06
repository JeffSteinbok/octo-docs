---
layout: default
title: Scheduled Tasks
nav_order: 9
---

# Scheduled Tasks

Scheduled tasks are background jobs that run without direct user input. The public bundle only includes infrastructure jobs that keep Octo healthy or maintained.

Feature-specific reminders, briefs, personal nudges, and other user-facing automations are intentionally excluded from the public bundle and from this page.

Octo currently publishes **9 infrastructure tasks**.

## Infrastructure Tasks

| Task | Schedule | What it does |
|------|----------|--------------|
| `Lobster changelog weekly scan` | Unknown | Scans the Lobster changelog for new ideas worth adopting and reports only when something changed. |
| `plugin-health-check` | Unknown | Daily smoke test that calls one tool from every configured plugin and reports pass/fail to Discord. |
| `Log rotation - openclaw.log` | Unknown | Runs copy-truncate rotation for the main OpenClaw log and keeps a bounded archive set. |
| `Nightly browser recycle` | Unknown | Restarts the headless Camoufox browser instance overnight to reclaim memory and clear stale sessions. |
| `agent-review-weekly` | Unknown | Scans session transcripts, tool failures, and memory files for patterns; deduplicates recurring findings via fingerprint state, auto-files guarded GitHub issues, and delivers a prioritized weekly report via Discord DM. |
| `config-backup` | Unknown | Runs the config-backup plugin to commit OpenClaw configuration changes to git and report failures. |
| `openclaw-upgrade-readiness-check` | Unknown | Checks for new OpenClaw releases and evaluates whether an upgrade is safe based on changelog and config compatibility. |
| `usage-enrich-sessions` | Unknown | Runs daily at 4 AM PT to enrich session labels with category/subcategory metadata, improving the accuracy of the weekly usage report breakdown. |
| `usage-weekly-report` | Unknown | Generates the weekly LLM API usage and cost report, renders it to PDF, posts to Discord, and commits the artifacts. |
