---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This page provides an overview of scheduled jobs, their purpose, and their execution schedules. These jobs automate recurring tasks such as data fetching, backups, and notifications, ensuring consistent and timely operations.

## Key Concepts

- **Scheduled Jobs**: Automated tasks configured to run at specific times or intervals.
- **Cron Scheduling**: Jobs scheduled using cron expressions to define precise execution times.
- **Recurring Intervals**: Jobs scheduled to run at fixed intervals, such as daily.

## How It Works

Scheduled jobs are configured with specific execution times or intervals. Jobs using cron expressions define exact times and days for execution, while interval-based jobs specify a recurring duration in milliseconds. Each job is enabled and runs according to its defined schedule.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

**Description**: Fetch calendars hourly between 7 AM and 5 PM PST.  
**Schedule**: Cron expression `0 7-17 * * *` in the timezone `America/Los_Angeles`.

---

### 🕒 config-backup

**Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.  
**Schedule**: Runs every 24 hours (86400000 milliseconds).

---

### 🕒 calendar-fetch-midnight

**Description**: Fetch calendars at midnight PST.  
**Schedule**: Cron expression `0 0 * * *` in the timezone `America/Los_Angeles`.

---

### 🕒 evening-briefing

**Description**: Weekday 9 PM briefing summarizing tasks for the following morning.  
**Schedule**: Cron expression `0 21 * * 0-4` in the timezone `America/Los_Angeles`.

---

### 🕒 portfolio-closing-briefing

**Description**: No description provided.  
**Schedule**: Cron expression `0 21 * * *` in the timezone `America/Los_Angeles`.

---

### 🕒 weekend-morning-alarm-reminder

**Description**: No description provided.  
**Schedule**: Cron expression `0 22 * * 5,6` in the timezone `America/Los_Angeles`.

---

### 🕒 Daily package delivery check

**Description**: No description provided.  
**Schedule**: Cron expression `0 8 * * *` in the timezone `America/Los_Angeles`.
