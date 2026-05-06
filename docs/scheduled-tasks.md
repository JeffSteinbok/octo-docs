---
layout: default
title: Scheduled Tasks
nav_order: 6
---

# Scheduled Tasks

Scheduled tasks are background jobs that run without direct user input. The public bundle only includes infrastructure jobs that keep Octo healthy or maintained.

Feature-specific reminders, briefs, personal nudges, and other user-facing automations are intentionally excluded from the public bundle and from this page.

Octo currently publishes **2 infrastructure tasks**.

## Infrastructure Tasks

| Task | Schedule | What it does |
|------|----------|--------------|
| `config-backup` | Every 24 hours | Runs the config-backup plugin to commit OpenClaw configuration changes to git and report failures. |
| `Log rotation - openclaw.log` | `0 3 * * *` (America/Los_Angeles) | Runs copy-truncate rotation for the main OpenClaw log and keeps a bounded archive set. |
