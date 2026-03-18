---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their execution schedules. These jobs are designed to automate recurring tasks, ensuring consistent and timely operations.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at predefined intervals or times.
- **Cron Schedule**: A time-based job scheduler format used to specify precise execution times.
- **Time Zones**: All schedules are specified in the `America/Los_Angeles` time zone unless otherwise noted.

## How It Works

Each job is configured with a specific schedule and description of its purpose. Jobs are triggered automatically based on their defined schedule, which can be either:
- **Cron Expression**: Specifies exact times and days for execution.
- **Interval-Based**: Specifies a recurring interval in milliseconds.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

- **Description**: Fetch calendars hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` (hourly from 7 AM to 5 PM, inclusive).

---

### 🕒 config-backup

- **Description**: Backup `openclaw.json` to Git daily. Only commits changes if the file has been modified.
- **Schedule**: Runs every 24 hours (86,400,000 milliseconds).

---

### 🕒 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` (daily at 12:00 AM).

---

### 🌅 evening-briefing

- **Description**: Weekday 9 PM briefing summarizing tasks for the following morning.
- **Schedule**: Cron expression `0 22 * * 0-4` (Sunday through Thursday at 9 PM).

---

### 🌇 portfolio-closing-briefing

- **Description**: *(No description provided)*.
- **Schedule**: Cron expression `0 21 * * 1-5` (Monday through Friday at 9 PM).

---

### ⏰ weekend-morning-alarm-reminder

- **Description**: *(No description provided)*.
- **Schedule**: Cron expression `0 22 * * 5,6` (Friday and Saturday at 10 PM).

---

### 📦 Daily package delivery check

- **Description**: *(No description provided)*.
- **Schedule**: Cron expression `0 8 * * *` (daily at 8 AM).
