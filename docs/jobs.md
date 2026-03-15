---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This page provides an overview of scheduled jobs, including their descriptions, purposes, and scheduling information. These jobs are automated tasks designed to perform specific functions at predefined intervals or times.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at specific times or intervals.
- **Cron Schedule**: A time-based job scheduler format used to specify when jobs should run.
- **Time Zones**: Some jobs are scheduled based on specific time zones (e.g., PST).
- **Enabled Jobs**: Only jobs marked as enabled are active and operational.

## Scheduled Jobs

### 🗓️ calendar-fetch-hourly

**Description**: Fetch calendars hourly between 7 AM and 5 PM PST.  
**Schedule**: Cron expression `0 7-17 * * *` in the `America/Los_Angeles` time zone.

---

### 📋 config-backup

**Description**: Backup `openclaw.json` to Git daily. The job only commits changes if the file has been modified.  
**Schedule**: Runs every 24 hours (`86400000 ms`).

---

### 🌙 calendar-fetch-midnight

**Description**: Fetch calendars at midnight PST.  
**Schedule**: Cron expression `0 0 * * *` in the `America/Los_Angeles` time zone.

---

### 🌅 evening-briefing

**Description**: Weekday 9 PM briefing summarizing tasks scheduled for the next morning.  
**Schedule**: Cron expression `0 21 * * 0-4` in the `America/Los_Angeles` time zone.

---

### 📈 portfolio-closing-briefing

**Description**: No description provided.  
**Schedule**: Cron expression `0 21 * * *` in the `America/Los_Angeles` time zone.

---

### ⏰ weekend-morning-alarm-reminder

**Description**: No description provided.  
**Schedule**: Cron expression `0 22 * * 5,6` in the `America/Los_Angeles` time zone.

---

### 📦 Daily package delivery check

**Description**: No description provided.  
**Schedule**: Cron expression `0 8 * * *` in the `America/Los_Angeles` time zone.
