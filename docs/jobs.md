---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs

## Overview

This page describes the scheduled jobs that automate recurring tasks such as calendar fetching, health checks, briefings, reminders, and backups. These jobs help streamline daily operations by running at specified times and intervals, ensuring important tasks are handled consistently and reliably.

Each job is defined with a purpose, schedule, and activation status. Schedules use either cron expressions or interval-based timing, and all times are specified in the America/Los_Angeles timezone unless otherwise noted.

## Key Concepts

- **Scheduled Jobs**: Automated tasks configured to run at specific times or intervals.
- **Cron Expressions**: Define complex schedules for jobs, specifying exact times and days.
- **Interval Scheduling**: Jobs can run at fixed intervals (e.g., every 24 hours).
- **Enabled/Disabled Status**: Jobs can be active or inactive based on configuration.
- **Timezone Awareness**: Most jobs are scheduled in the America/Los_Angeles timezone.

## How It Works

1. Each job is configured with a name, description, schedule, and enabled status.
2. Jobs use either cron expressions or interval-based scheduling to determine when they run.
3. When a job's scheduled time arrives, it executes its defined task (e.g., fetching calendars, sending reminders, performing health checks).
4. Disabled jobs do not run until enabled.
5. The system ensures that jobs execute reliably according to their schedule.

## Scheduled Jobs

### 🗓️ calendar-fetch-hourly

- **Description**: Fetch calendars hourly 7am-5pm PST
- **Schedule**: Hourly at the top of the hour, from 7:00 AM to 5:00 PM (America/Los_Angeles)

---

### 💾 config-backup

- **Description**: Backup openclaw.json to Git daily (only commits if changed)
- **Schedule**: Every 24 hours

---

### 📰 evening-briefing

- **Description**: Weekday 9 PM briefing: what's on tap tomorrow morning
- **Schedule**: 9:00 PM, Sunday through Thursday (America/Los_Angeles)

---

### 📈 portfolio-closing-briefing

- **Description**: *(No description provided)*
- **Schedule**: 9:00 PM, Monday through Friday (America/Los_Angeles)

---

### ⏰ evening-alarm-reminder

- **Description**: Nightly 10:30 PM: remind Jeff to check alarm if early morning work meeting
- **Schedule**: 10:30 PM daily (America/Los_Angeles)

---

### 📦 Daily package delivery check

- **Description**: *(No description provided)*
- **Schedule**: 8:00 AM daily (America/Los_Angeles)

---

### 🩺 daily-health-check

- **Description**: Daily health check — verifies email sending works; DMs Jeff if anything fails
- **Schedule**: 9:00 AM daily (America/Los_Angeles)

---

### 🍽️ Remind Jeff to reach out to Zack Ali for dinner

- **Description**: One-shot reminder to schedule another dinner with Zack Ali
- **Schedule**: One-time (disabled)

---

### 🏅 WW Daily Points Check-in

- **Description**: *(No description provided)*
- **Schedule**: 5:30 PM daily (America/Los_Angeles)

---

### 🔄 late-early-conflict-morning-check

- **Description**: 10 AM daily: flag if today has late meeting (after 6 PM) and tomorrow has early meeting (before 9 AM)
- **Schedule**: 10:00 AM daily (America/Los_Angeles)

---

### 🦞 Lobster changelog weekly scan

- **Description**: Weekly Monday scan of lobster.shahine.com/changelog for new ideas
- **Schedule**: 9:00 AM every Monday (America/Los_Angeles)

---

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST
- **Schedule**: 12:00 AM daily (America/Los_Angeles)

---

### 🥗 ww-diet-sync

- **Description**: *(No description provided)*
- **Schedule**: 4:00 AM daily (America/Los_Angeles)
