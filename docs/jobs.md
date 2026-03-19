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
- **Schedule**: Defines when and how often the job runs, using either cron expressions or interval-based timing.
- **Time Zone**: Specifies the time zone for the job's schedule.

## How It Works

Scheduled jobs are configured to run automatically based on their defined schedules. Jobs use either:
- **Cron-based schedules**: Specify exact times and days for execution.
- **Interval-based schedules**: Specify a fixed time interval between executions.

## Scheduled Jobs

### 📅 calendar-fetch-hourly

- **Description**: Fetch calendars hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based, runs at the start of every hour from 7:00 AM to 5:00 PM (PST).
  - **Cron Expression**: `0 7-17 * * *`
  - **Time Zone**: America/Los_Angeles

---

### 🗂️ config-backup

- **Description**: Backup `openclaw.json` to Git daily. Commits changes only if the file has been modified.
- **Schedule**: Interval-based, runs every 24 hours (86,400,000 milliseconds).

---

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron-based, runs at 12:00 AM (midnight) daily.
  - **Cron Expression**: `0 0 * * *`
  - **Time Zone**: America/Los_Angeles

---

### 🌅 evening-briefing

- **Description**: Provides a weekday 9:00 PM briefing about the next morning's schedule.
- **Schedule**: Cron-based, runs at 9:00 PM (PST) from Monday to Friday.
  - **Cron Expression**: `0 22 * * 0-4`
  - **Time Zone**: America/Los_Angeles

---

### 📈 portfolio-closing-briefing

- **Description**: Not provided.
- **Schedule**: Cron-based, runs at 9:00 PM (PST) from Monday to Friday.
  - **Cron Expression**: `0 21 * * 1-5`
  - **Time Zone**: America/Los_Angeles

---

### ⏰ weekend-morning-alarm-reminder

- **Description**: Not provided.
- **Schedule**: Cron-based, runs at 10:00 PM (PST) on Fridays and Saturdays.
  - **Cron Expression**: `0 22 * * 5,6`
  - **Time Zone**: America/Los_Angeles

---

### 📦 Daily package delivery check

- **Description**: Not provided.
- **Schedule**: Cron-based, runs at 8:00 AM (PST) daily.
  - **Cron Expression**: `0 8 * * *`
  - **Time Zone**: America/Los_Angeles
