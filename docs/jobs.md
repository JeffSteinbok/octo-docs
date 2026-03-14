---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This page provides an overview of scheduled jobs, their purpose, and their execution schedules. These jobs automate recurring tasks such as fetching data, backing up configurations, and generating briefings.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run on predefined schedules.
- **Cron Expressions**: Used to define specific times for job execution.
- **Time Zones**: Jobs may be scheduled in specific time zones.
- **Enabled Status**: Indicates whether a job is active and running.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

**Description**: Fetch calendars hourly between 7 AM and 5 PM PST.  
**Schedule**: Cron expression `0 7-17 * * *` in the time zone `America/Los_Angeles`.

---

### 🕒 config-backup

**Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.  
**Schedule**: Runs every 24 hours (`86400000 ms`).

---

### 🕒 calendar-fetch-midnight

**Description**: Fetch calendars at midnight PST.  
**Schedule**: Cron expression `0 0 * * *` in the time zone `America/Los_Angeles`.

---

### 🕒 evening-briefing

**Description**: Weekday 9 PM briefing summarizing tasks for the next morning.  
**Schedule**: Cron expression `0 21 * * 0-4` in the time zone `America/Los_Angeles`.
