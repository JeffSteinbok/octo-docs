---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs

## Overview

This page describes the scheduled jobs that automate various tasks such as calendar fetching, backups, health checks, reminders, and briefings. These jobs help streamline daily operations by running at specific times or intervals, ensuring important tasks are performed reliably and on schedule.

Each job is configured with a schedule and purpose, enabling consistent execution of routine activities without manual intervention.

## Key Concepts

- **Scheduled Jobs**: Automated tasks configured to run at specific times or intervals.
- **Cron Scheduling**: Jobs scheduled using cron expressions for precise timing.
- **Enabled/Disabled Status**: Indicates whether a job is active.
- **Task Purpose**: Each job serves a distinct operational or informational function.

## How It Works

1. Jobs are defined with a name, description, enabled status, and schedule.
2. Schedules use either cron expressions (for specific times) or interval-based triggers.
3. Enabled jobs execute automatically according to their schedule.
4. Each job performs its designated task, such as fetching data, sending reminders, or performing health checks.

## Scheduled Jobs

### 🗓️ calendar-fetch-hourly

- **Description**: Fetch calendars hourly 7am-5pm PST.
- **Schedule**: Every hour from 7:00 AM to 5:00 PM (PST), using cron: `0 7-17 * * *` (America/Los_Angeles).

---

### 💾 config-backup

- **Description**: Backup openclaw.json to Git daily (only commits if changed).
- **Schedule**: Every 24 hours.

---

### 📰 evening-briefing

- **Description**: Weekday 9 PM briefing: what's on tap tomorrow morning.
- **Schedule**: 9:00 PM, Sunday through Thursday (PST), using cron: `0 22 * * 0-4` (America/Los_Angeles).

---

### 📈 portfolio-closing-briefing

- **Description**: (No description provided)
- **Schedule**: 9:00 PM, Monday through Friday (PST), using cron: `0 21 * * 1-5` (America/Los_Angeles).

---

### ⏰ evening-alarm-reminder

- **Description**: Nightly 10:30 PM: remind Jeff to check alarm if early morning work meeting.
- **Schedule**: 10:30 PM daily (PST), using cron: `30 22 * * *` (America/Los_Angeles).

---

### 📦 Daily package delivery check

- **Description**: (No description provided)
- **Schedule**: 8:00 AM daily (PST), using cron: `0 8 * * *` (America/Los_Angeles).

---

### 🩺 daily-health-check

- **Description**: Daily health check — verifies email sending works; DMs Jeff if anything fails.
- **Schedule**: 9:00 AM daily (PST), using cron: `0 9 * * *` (America/Los_Angeles).

---

### 🥘 Remind Jeff to reach out to Zack Ali for dinner

- **Description**: One-shot reminder to schedule another dinner with Zack Ali.
- **Schedule**: One-time (disabled).

---

### 🏅 WW Daily Points Check-in

- **Description**: (No description provided)
- **Schedule**: 5:30 PM daily (PST), using cron: `30 17 * * *` (America/Los_Angeles).

---

### ⚠️ late-early-conflict-morning-check

- **Description**: 10 AM daily: flag if today has late meeting (after 6 PM) and tomorrow has early meeting (before 9 AM).
- **Schedule**: 10:00 AM daily (PST), using cron: `0 10 * * *` (America/Los_Angeles).

---

### 🦞 Lobster changelog weekly scan

- **Description**: Weekly Monday scan of lobster.shahine.com/changelog for new ideas.
- **Schedule**: 9:00 AM every Monday (PST), using cron: `0 9 * * 1` (America/Los_Angeles).

---

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: 12:00 AM daily (PST), using cron: `0 0 * * *` (America/Los_Angeles).

---

### 🍏 ww-diet-sync

- **Description**: (No description provided)
- **Schedule**: 4:00 AM daily (PST), using cron: `0 4 * * *` (America/Los_Angeles).
