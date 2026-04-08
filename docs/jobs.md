---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their execution schedules. These jobs automate various tasks, such as fetching data, sending reminders, and performing system checks, to ensure smooth operations and timely notifications.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled task.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: Defines when and how often the job runs, using cron expressions or interval-based timing.
- **Time Zone**: All schedules are specified in the `America/Los_Angeles` time zone unless otherwise noted.

## How It Works

Scheduled jobs are configured to run automatically based on predefined schedules. These schedules are either:
- **Cron-based**: Using cron expressions to specify exact times and days for execution.
- **Interval-based**: Running at fixed intervals, such as every 24 hours.

Each job is enabled or disabled based on its configuration. Disabled jobs do not execute.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

- **Description**: Fetches calendars hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based (`0 7-17 * * *`).

---

### 🕛 calendar-fetch-midnight

- **Description**: Fetches calendars at midnight PST.
- **Schedule**: Cron-based (`0 0 * * *`).

---

### 💾 config-backup

- **Description**: Backs up `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Interval-based (every 24 hours).

---

### 🌅 evening-briefing

- **Description**: Provides a weekday 9:00 PM briefing about the next morning's schedule.
- **Schedule**: Cron-based (`0 22 * * 0-4`).

---

### 🛎️ evening-alarm-reminder

- **Description**: Sends a nightly reminder at 10:30 PM to check the alarm if there is an early morning work meeting.
- **Schedule**: Cron-based (`30 22 * * *`).

---

### 📦 Daily package delivery check

- **Description**: (No description provided).
- **Schedule**: Cron-based (`0 8 * * *`).

---

### 🩺 daily-health-check

- **Description**: Performs a daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron-based (`0 9 * * *`).

---

### 📊 WW Daily Points Check-in

- **Description**: (No description provided).
- **Schedule**: Cron-based (`30 17 * * *`).

---

### ⚠️ late-early-conflict-morning-check

- **Description**: Runs daily at 10:00 AM to flag if there is a late meeting (after 6:00 PM) today and an early meeting (before 9:00 AM) tomorrow.
- **Schedule**: Cron-based (`0 10 * * *`).

---

### 🦞 Lobster changelog weekly scan

- **Description**: Scans the Lobster changelog every Monday for new ideas.
- **Schedule**: Cron-based (`0 9 * * 1`).
