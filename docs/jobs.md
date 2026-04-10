---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs

## Overview

This page provides an overview of scheduled jobs that automate recurring tasks such as calendar fetching, health checks, briefings, reminders, and backups. These jobs help streamline daily operations by ensuring important actions are performed at specific times or intervals.

Each job is described with its purpose and schedule, allowing developers to understand what tasks are automated and when they run.

## Key Concepts

- **Scheduled Jobs**: Automated tasks configured to run at specific times or intervals.
- **Cron Scheduling**: Jobs scheduled using cron expressions, often with a specified timezone.
- **Enabled/Disabled Jobs**: Only enabled jobs are active; disabled jobs do not run.
- **Job Purpose**: Each job has a specific function, such as fetching calendars or sending reminders.

## How It Works

1. Jobs are defined with a name, description, enabled status, and schedule.
2. Enabled jobs are executed automatically according to their schedule.
3. Schedules use either cron expressions (with timezone) or interval-based timing.
4. Each job performs its designated task, such as fetching data, sending notifications, or performing checks.

## Scheduled Jobs

### 🗓️ calendar-fetch-hourly

- **Description**: Fetch calendars hourly 7am-5pm PST
- **Schedule**: Hourly at 7:00–17:00 (7am–5pm) Pacific Time (`0 7-17 * * *`, America/Los_Angeles)

---

### 💾 config-backup

- **Description**: Backup openclaw.json to Git daily (only commits if changed)
- **Schedule**: Every 24 hours

---

### 📰 evening-briefing

- **Description**: Weekday 9 PM briefing: what's on tap tomorrow morning
- **Schedule**: 9:00 PM, Sunday–Thursday (weekdays) Pacific Time (`0 22 * * 0-4`, America/Los_Angeles)

---

### 📈 portfolio-closing-briefing

- **Description**: *(No description provided)*
- **Schedule**: 9:00 PM, Monday–Friday Pacific Time (`0 21 * * 1-5`, America/Los_Angeles)

---

### ⏰ evening-alarm-reminder

- **Description**: Nightly 10:30 PM: remind Jeff to check alarm if early morning work meeting
- **Schedule**: 10:30 PM daily Pacific Time (`30 22 * * *`, America/Los_Angeles)

---

### 📦 Daily package delivery check

- **Description**: *(No description provided)*
- **Schedule**: 8:00 AM daily Pacific Time (`0 8 * * *`, America/Los_Angeles)

---

### 🩺 daily-health-check

- **Description**: Daily health check — verifies email sending works; DMs Jeff if anything fails
- **Schedule**: 9:00 AM daily Pacific Time (`0 9 * * *`, America/Los_Angeles)

---

### 🥗 WW Daily Points Check-in

- **Description**: *(No description provided)*
- **Schedule**: 5:30 PM daily Pacific Time (`30 17 * * *`, America/Los_Angeles)

---

### ⚠️ late-early-conflict-morning-check

- **Description**: 10 AM daily: flag if today has late meeting (after 6 PM) and tomorrow has early meeting (before 9 AM)
- **Schedule**: 10:00 AM daily Pacific Time (`0 10 * * *`, America/Los_Angeles)

---

### 🦞 Lobster changelog weekly scan

- **Description**: Weekly Monday scan of lobster.shahine.com/changelog for new ideas
- **Schedule**: 9:00 AM every Monday Pacific Time (`0 9 * * 1`, America/Los_Angeles)

---

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST
- **Schedule**: Midnight daily Pacific Time (`0 0 * * *`, America/Los_Angeles)

---

### 🍽️ ww-diet-sync

- **Description**: *(No description provided)*
- **Schedule**: 4:00 AM daily Pacific Time (`0 4 * * *`, America/Los_Angeles)

---

## Disabled Jobs

### 🥘 Remind Jeff to reach out to Zack Ali for dinner

- **Description**: One-shot reminder to schedule another dinner with Zack Ali
- **Schedule**: One-time (disabled)
