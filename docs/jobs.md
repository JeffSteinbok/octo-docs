---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purpose, and their execution schedules. These jobs automate recurring tasks, ensuring consistent and timely operations.

## Key Concepts

- **Scheduled Jobs**: Automated tasks configured to run at specific times or intervals.
- **Cron Schedule**: A time-based job scheduler using cron expressions to define execution times.
- **Recurring Interval**: Jobs scheduled to run at fixed intervals, defined in milliseconds.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

**Description**: Fetch calendars hourly between 7 AM and 5 PM PST.  
**Schedule**: Cron expression `0 7-17 * * *` in timezone `America/Los_Angeles`.

---

### 🌙 calendar-fetch-midnight

**Description**: Fetch calendars at midnight PST.  
**Schedule**: Cron expression `0 0 * * *` in timezone `America/Los_Angeles`.

---

### 📋 config-backup

**Description**: Backup `openclaw.json` to Git daily. Only commits changes if the file has been modified.  
**Schedule**: Recurring interval of 86,400,000 milliseconds (24 hours).

---

### 🌅 evening-briefing

**Description**: Weekday 9 PM briefing summarizing tasks scheduled for the next morning.  
**Schedule**: Cron expression `0 21 * * 0-4` in timezone `America/Los_Angeles`.

---

### 📈 portfolio-closing-briefing

**Description**: No description provided.  
**Schedule**: Cron expression `0 21 * * *` in timezone `America/Los_Angeles`.

---

### ⏰ weekend-morning-alarm-reminder

**Description**: No description provided.  
**Schedule**: Cron expression `0 22 * * 5,6` in timezone `America/Los_Angeles`.

---

### 📦 Daily package delivery check

**Description**: No description provided.  
**Schedule**: Cron expression `0 8 * * *` in timezone `America/Los_Angeles`.
