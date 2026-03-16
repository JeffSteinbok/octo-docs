---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This page provides an overview of scheduled jobs within the system. Each job is designed to perform specific tasks at predefined intervals, ensuring consistent and reliable execution of critical operations. The schedules are configured using cron expressions or interval-based timing.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at specific times or intervals.
- **Cron Expressions**: Define precise schedules for jobs based on time and day.
- **Time Zones**: Jobs are scheduled in the `America/Los_Angeles` time zone unless otherwise specified.
- **Enabled Jobs**: Only jobs marked as enabled are actively running.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

**Description**: Fetch calendars hourly between 7 AM and 5 PM PST.  
**Schedule**: Cron expression `0 7-17 * * *` in `America/Los_Angeles` time zone.

---

### 🌙 calendar-fetch-midnight

**Description**: Fetch calendars at midnight PST.  
**Schedule**: Cron expression `0 0 * * *` in `America/Los_Angeles` time zone.

---

### 💾 config-backup

**Description**: Backup `openclaw.json` to Git daily. Only commits changes if the file has been modified.  
**Schedule**: Runs every 24 hours (`86400000 ms`).

---

### 📋 evening-briefing

**Description**: Weekday 9 PM briefing summarizing tasks scheduled for the next morning.  
**Schedule**: Cron expression `0 21 * * 0-4` in `America/Los_Angeles` time zone.

---

### 📈 portfolio-closing-briefing

**Description**: No description provided.  
**Schedule**: Cron expression `0 21 * * 1-5` in `America/Los_Angeles` time zone.

---

### ⏰ weekend-morning-alarm-reminder

**Description**: No description provided.  
**Schedule**: Cron expression `0 22 * * 5,6` in `America/Los_Angeles` time zone.

---

### 📦 Daily package delivery check

**Description**: No description provided.  
**Schedule**: Cron expression `0 8 * * *` in `America/Los_Angeles` time zone.
