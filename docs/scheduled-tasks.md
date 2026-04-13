---
layout: default
title: Scheduled Tasks
nav_order: 6
---

# Scheduled Tasks

Scheduled tasks are background jobs that run without direct user input. Some keep the system healthy; others produce user-facing reminders, syncs, and briefings.

The public docs only include the recurring jobs that are part of the stable setup. One-shot reminders and temporary test jobs are intentionally omitted.

Octo currently publishes **13 scheduled tasks**.

## Infrastructure Tasks

| Task | Schedule | What it does |
|------|----------|--------------|
| `config-backup` | Every 24 hours | Runs the config-backup plugin to commit OpenClaw configuration changes to git and report failures. |
| `daily-health-check` | `0 9 * * *` (America/Los_Angeles) | Sends a daily test email to verify outbound mail is healthy and alerts Jeff only if the send fails. |
| `Lobster changelog weekly scan` | `0 9 * * 1` (America/Los_Angeles) | Scans the Lobster changelog for new ideas worth adopting and reports only when something changed. |
| `Log rotation - openclaw.log` | `0 3 * * *` (America/Los_Angeles) | Runs copy-truncate rotation for the main OpenClaw log and keeps a bounded archive set. |

## Feature Tasks

| Task | Schedule | What it does |
|------|----------|--------------|
| `calendar-fetch-hourly` | `0 7-17 * * *` (America/Los_Angeles) | Refreshes the local calendar memory files that calendar briefings and reminder jobs rely on during the day. |
| `evening-briefing` | `0 22 * * 0-4` (America/Los_Angeles) | Reads the synced calendar snapshots and sends a short Discord briefing about tomorrow's schedule. |
| `portfolio-closing-briefing` | `0 21 * * 1-5` (America/Los_Angeles) | Pulls closing prices for Jeff's portfolio and sends a concise end-of-day market summary. |
| `evening-alarm-reminder` | `30 22 * * *` (America/Los_Angeles) | Checks for early work meetings or late-night/early-morning conflicts and warns Jeff to adjust plans or alarms. |
| `Daily package delivery check` | `0 8 * * *` (America/Los_Angeles) | Reviews tracked packages for today's deliveries or notable updates and removes delivered items. |
| `WW Daily Points Check-in` | `30 17 * * *` (America/Los_Angeles) | Checks WeightWatchers daily and weekly points and sends the remaining budget to Jeff. |
| `late-early-conflict-morning-check` | `0 10 * * *` (America/Los_Angeles) | Looks for late meetings today plus early meetings tomorrow and flags the conflict early enough to reschedule. |
| `calendar-fetch-midnight` | `0 0 * * *` (America/Los_Angeles) | Performs the same calendar sync overnight so the next day starts with fresh memory snapshots. |
| `ww-diet-sync` | `0 4 * * *` (America/Los_Angeles) | Runs the nightly WeightWatchers diet sync script from the main-agent workspace. |
