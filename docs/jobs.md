---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs in the system. Each job is designed to perform a specific task at a predefined schedule, ensuring the system operates efficiently and critical processes are executed on time.

## Key Concepts

- **Job Name**: A unique identifier for the scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: The timing and frequency at which the job is executed.
  - **Cron**: Specifies a schedule using a cron expression.
  - **Every**: Specifies a schedule based on a fixed interval in milliseconds.
- **Timezone**: The timezone in which the schedule is defined.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

- **Description**: Fetch calendars hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron expression `0 7-17 * * *` (hourly from 7 AM to 5 PM).
- **Timezone**: America/Los_Angeles.

---

### 🗂️ config-backup

- **Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Every 86,400,000 milliseconds (24 hours).

---

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron expression `0 0 * * *` (daily at midnight).
- **Timezone**: America/Los_Angeles.

---

### 🌅 evening-briefing

- **Description**: Weekday 9 PM briefing summarizing what's on tap for the next morning.
- **Schedule**: Cron expression `0 22 * * 0-4` (Sunday to Thursday at 9 PM).
- **Timezone**: America/Los_Angeles.

---

### 📈 portfolio-closing-briefing

- **Description**: *(No description provided)*.
- **Schedule**: Cron expression `0 21 * * 1-5` (Monday to Friday at 9 PM).
- **Timezone**: America/Los_Angeles.

---

### ⏰ weekend-morning-alarm-reminder

- **Description**: *(No description provided)*.
- **Schedule**: Cron expression `0 22 * * 5,6` (Friday and Saturday at 10 PM).
- **Timezone**: America/Los_Angeles.

---

### 📦 Daily package delivery check

- **Description**: *(No description provided)*.
- **Schedule**: Cron expression `0 8 * * *` (daily at 8 AM).
- **Timezone**: America/Los_Angeles.

---

### ✅ daily-health-check

- **Description**: Daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron expression `0 9 * * *` (daily at 9 AM).
- **Timezone**: America/Los_Angeles.
