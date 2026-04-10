---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs

## Overview

This page describes the scheduled jobs that automate recurring tasks such as calendar fetching, backups, health checks, reminders, and briefings. These jobs help maintain system reliability, provide timely notifications, and ensure important routines are executed without manual intervention.

Each job runs on a defined schedule, using either cron expressions or interval timers, and is designed to address specific operational needs.

## Key Concepts

- **Scheduled Jobs**: Automated tasks executed at specified times or intervals.
- **Cron Scheduling**: Jobs scheduled using cron expressions, often with a timezone.
- **Interval Scheduling**: Jobs scheduled to run at regular intervals (e.g., daily).
- **Job Enablement**: Only enabled jobs are active and executed.
- **Job Purpose**: Each job serves a distinct function, such as fetching data, sending reminders, or performing health checks.

## How It Works

1. Each job is defined with a name, description, enabled status, and schedule.
2. Jobs are scheduled using either cron expressions (with timezone support) or interval timers.
3. When the scheduled time arrives, the job executes its designated task.
4. Disabled jobs are not executed.

---

## Scheduled Jobs

### 🗓️ calendar-fetch-hourly

- **Description**: Fetch calendars hourly 7am-5pm PST
- **Schedule**: Every hour at the top of the hour, from 7:00 AM to 5:00 PM (America/Los_Angeles timezone)

---

### 💾 config-backup

- **Description**: Backup openclaw.json to Git daily (only commits if changed)
- **Schedule**: Every 24 hours

---

### 📰 evening-briefing

- **Description**: Weekday 9 PM briefing: what's on tap tomorrow morning
- **Schedule**: Every weekday at 9:00 PM (America/Los_Angeles timezone)

---

### 📈 portfolio-closing-briefing

- **Description**: *(No description provided)*
- **Schedule**: Monday to Friday at 9:00 PM (America/Los_Angeles timezone)

---

### ⏰ evening-alarm-reminder

- **Description**: Nightly 10:30 PM: remind Jeff to check alarm if early morning work meeting
- **Schedule**: Every night at 10:30 PM (America/Los_Angeles timezone)

---

### 📦 Daily package delivery check

- **Description**: *(No description provided)*
- **Schedule**: Every day at 8:00 AM (America/Los_Angeles timezone)

---

### 🩺 daily-health-check

- **Description**: Daily health check — verifies email sending works; DMs Jeff if anything fails
- **Schedule**: Every day at 9:00 AM (America/Los_Angeles timezone)

---

### 🍽️ Remind Jeff to reach out to Zack Ali for dinner

- **Description**: One-shot reminder to schedule another dinner with Zack Ali
- **Schedule**: One-time (currently disabled)

---

### 🏅 WW Daily Points Check-in

- **Description**: *(No description provided)*
- **Schedule**: Every day at 5:30 PM (America/Los_Angeles timezone)

---

### ⚠️ late-early-conflict-morning-check

- **Description**: 10 AM daily: flag if today has late meeting (after 6 PM) and tomorrow has early meeting (before 9 AM)
- **Schedule**: Every day at 10:00 AM (America/Los_Angeles timezone)

---

### 🦞 Lobster changelog weekly scan

- **Description**: Weekly Monday scan of lobster.shahine.com/changelog for new ideas
- **Schedule**: Every Monday at 9:00 AM (America/Los_Angeles timezone)

---

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST
- **Schedule**: Every day at 12:00 AM (America/Los_Angeles timezone)

---

### 🥗 ww-diet-sync

- **Description**: *(No description provided)*
- **Schedule**: Every day at 4:00 AM (America/Los_Angeles timezone)
