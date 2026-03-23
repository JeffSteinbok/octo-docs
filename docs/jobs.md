---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs in the system. Each job is designed to perform a specific task at a predefined schedule, ensuring the system operates efficiently and critical tasks are executed on time.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: The timing and frequency at which the job is executed.
  - **Cron Schedule**: Specifies the exact times and days a job runs.
  - **Interval Schedule**: Specifies the time interval between job executions.
- **Time Zone**: The time zone in which the job's schedule is defined.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

- **Description**: Fetch calendars hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` (hourly from 7:00 AM to 5:00 PM).
- **Time Zone**: America/Los_Angeles.

---

### 🗂️ config-backup

- **Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Every 24 hours (86400000 milliseconds).

---

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` (daily at 12:00 AM).
- **Time Zone**: America/Los_Angeles.

---

### 🌅 evening-briefing

- **Description**: Weekday 9:00 PM briefing to prepare for the next morning.
- **Schedule**: Cron expression `0 22 * * 0-4` (Sunday through Thursday at 9:00 PM).
- **Time Zone**: America/Los_Angeles.

---

### 📈 portfolio-closing-briefing

- **Description**: *(No description provided)*.
- **Schedule**: Cron expression `0 21 * * 1-5` (Monday through Friday at 9:00 PM).
- **Time Zone**: America/Los_Angeles.

---

### ⏰ weekend-morning-alarm-reminder

- **Description**: *(No description provided)*.
- **Schedule**: Cron expression `0 22 * * 5,6` (Friday and Saturday at 10:00 PM).
- **Time Zone**: America/Los_Angeles.

---

### 📦 Daily package delivery check

- **Description**: *(No description provided)*.
- **Schedule**: Cron expression `0 8 * * *` (daily at 8:00 AM).
- **Time Zone**: America/Los_Angeles.

---

### ✈️ nicole-flight-DL347-checkin

- **Description**: *(No description provided)*.
- **Schedule**: Cron expression `0 8,10,11 * * *` (daily at 8:00 AM, 10:00 AM, and 11:00 AM).
- **Time Zone**: America/Los_Angeles.

---

### ✅ daily-health-check

- **Description**: Daily health check to verify email sending functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron expression `0 9 * * *` (daily at 9:00 AM).
- **Time Zone**: America/Los_Angeles.
