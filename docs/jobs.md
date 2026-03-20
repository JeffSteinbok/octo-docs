---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs available in the system. Each job is designed to perform a specific task at a predefined schedule, ensuring the system operates efficiently and critical tasks are executed on time.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: The timing and frequency at which the job is executed.
  - **Cron**: Specifies the schedule using a cron expression.
  - **Every**: Specifies the interval in milliseconds between executions.
- **Time Zone**: The time zone in which the job's schedule is defined.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

- **Description**: Fetch calendars hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` (hourly from 7 AM to 5 PM).
- **Time Zone**: America/Los_Angeles.

---

### 🗂️ config-backup

- **Description**: Backup `openclaw.json` to Git daily. Only commits changes if the file has been modified.
- **Schedule**: Every 86,400,000 milliseconds (24 hours).

---

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` (daily at midnight).
- **Time Zone**: America/Los_Angeles.

---

### 🌅 evening-briefing

- **Description**: Weekday 9 PM briefing summarizing tasks for the following morning.
- **Schedule**: Cron expression `0 22 * * 0-4` (Sunday through Thursday at 9 PM).
- **Time Zone**: America/Los_Angeles.

---

### 🌇 portfolio-closing-briefing

- **Description**: No description provided.
- **Schedule**: Cron expression `0 21 * * 1-5` (Monday through Friday at 9 PM).
- **Time Zone**: America/Los_Angeles.

---

### ⏰ weekend-morning-alarm-reminder

- **Description**: No description provided.
- **Schedule**: Cron expression `0 22 * * 5,6` (Friday and Saturday at 10 PM).
- **Time Zone**: America/Los_Angeles.

---

### 📦 Daily package delivery check

- **Description**: No description provided.
- **Schedule**: Cron expression `0 8 * * *` (daily at 8 AM).
- **Time Zone**: America/Los_Angeles.
