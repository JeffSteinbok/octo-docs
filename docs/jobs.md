---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs in the system. These jobs are automated tasks designed to perform specific functions at predefined intervals. They help ensure the system operates efficiently and reliably by handling recurring tasks such as data fetching, backups, and notifications.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at specified intervals or times.
- **Cron Schedule**: A time-based job scheduler using cron expressions to define execution times.
- **Interval Schedule**: A job scheduler that runs tasks at fixed time intervals.

## How It Works

Scheduled jobs are configured with specific schedules and purposes. Jobs can be triggered using either a cron expression or a fixed interval in milliseconds. Each job is enabled by default and runs according to its defined schedule in the specified time zone.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

- **Description**: Fetch calendars hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron-based, runs every hour from 7 AM to 5 PM PST (`0 7-17 * * *` in `America/Los_Angeles` time zone).

---

### 🗂️ config-backup

- **Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Runs every 24 hours (86,400,000 milliseconds).

---

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron-based, runs daily at 12:00 AM PST (`0 0 * * *` in `America/Los_Angeles` time zone).

---

### 🌅 evening-briefing

- **Description**: Weekday 9 PM briefing to summarize tasks for the following morning.
- **Schedule**: Cron-based, runs Monday through Friday at 9 PM PST (`0 22 * * 0-4` in `America/Los_Angeles` time zone).

---

### 📈 portfolio-closing-briefing

- **Description**: *No description provided.*
- **Schedule**: Cron-based, runs Monday through Friday at 9 PM PST (`0 21 * * 1-5` in `America/Los_Angeles` time zone).

---

### ⏰ weekend-morning-alarm-reminder

- **Description**: *No description provided.*
- **Schedule**: Cron-based, runs Friday and Saturday at 10 PM PST (`0 22 * * 5,6` in `America/Los_Angeles` time zone).

---

### 📦 Daily package delivery check

- **Description**: *No description provided.*
- **Schedule**: Cron-based, runs daily at 8 AM PST (`0 8 * * *` in `America/Los_Angeles` time zone).

---

### ✅ daily-health-check

- **Description**: Daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron-based, runs daily at 9 AM PST (`0 9 * * *` in `America/Los_Angeles` time zone).
