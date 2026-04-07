---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their execution schedules. These jobs are designed to automate recurring tasks, ensuring consistent and timely operations.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled task.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: Specifies when and how often the job runs, using either cron expressions or time intervals.
- **Time Zone**: All schedules are based on the `America/Los_Angeles` time zone unless otherwise specified.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

- **Description**: Fetch calendars hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` (hourly from 7 AM to 5 PM).

---

### 🕒 config-backup

- **Description**: Backup `openclaw.json` to Git daily. Commits changes only if the file has been modified.
- **Schedule**: Every 24 hours (86400000 milliseconds).

---

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` (daily at midnight).

---

### 🌅 evening-briefing

- **Description**: Weekday 9 PM briefing summarizing tasks for the following morning.
- **Schedule**: Cron expression `0 22 * * 0-4` (Sunday through Thursday at 9 PM).

---

### 🌇 portfolio-closing-briefing

- **Description**: (No description provided).
- **Schedule**: Cron expression `0 21 * * 1-5` (Monday through Friday at 9 PM).

---

### ⏰ weekend-morning-alarm-reminder

- **Description**: (No description provided).
- **Schedule**: Cron expression `0 22 * * 5,6` (Friday and Saturday at 10 PM).

---

### 📦 Daily package delivery check

- **Description**: (No description provided).
- **Schedule**: Cron expression `0 8 * * *` (daily at 8 AM).

---

### ✅ daily-health-check

- **Description**: Daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron expression `0 9 * * *` (daily at 9 AM).

---

### 📊 WW Daily Points Check-in

- **Description**: (No description provided).
- **Schedule**: Cron expression `30 17 * * *` (daily at 5:30 PM).
