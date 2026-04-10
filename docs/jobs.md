---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This page provides an overview of scheduled jobs, including their purpose, schedule, and key details. These jobs automate recurring tasks such as calendar updates, health checks, and reminders, ensuring consistent and timely execution.

## Key Concepts

- **Enabled Jobs**: Only jobs marked as enabled are actively scheduled.
- **Schedules**: Jobs use various scheduling methods, including cron expressions and fixed intervals.
- **Time Zones**: All schedules are configured in the `America/Los_Angeles` time zone unless otherwise specified.

## Scheduled Jobs

### 🗓️ Calendar Fetch Hourly

**Description**: Fetch calendars hourly between 7 AM and 5 PM PST.  
**Schedule**: Cron expression `0 7-17 * * *` (hourly from 7 AM to 5 PM).  

---

### 🗂️ Config Backup

**Description**: Backup `openclaw.json` daily to Git, committing only if changes are detected.  
**Schedule**: Every 24 hours (`86400000 ms`).  

---

### 🌅 Evening Briefing

**Description**: Weekday 9 PM briefing summarizing tasks for the next morning.  
**Schedule**: Cron expression `0 22 * * 0-4` (Monday to Friday at 9 PM).  

---

### 📈 Portfolio Closing Briefing

**Description**: No description provided.  
**Schedule**: Cron expression `0 21 * * 1-5` (Monday to Friday at 9 PM).  

---

### ⏰ Evening Alarm Reminder

**Description**: Nightly 10:30 PM reminder for Jeff to check the alarm if an early morning work meeting is scheduled.  
**Schedule**: Cron expression `30 22 * * *` (daily at 10:30 PM).  

---

### 📦 Daily Package Delivery Check

**Description**: No description provided.  
**Schedule**: Cron expression `0 8 * * *` (daily at 8 AM).  

---

### 🩺 Daily Health Check

**Description**: Daily health check verifying email functionality; sends a direct message to Jeff if any issues are detected.  
**Schedule**: Cron expression `0 9 * * *` (daily at 9 AM).  

---

### 🕙 Late-Early Conflict Morning Check

**Description**: Daily 10 AM check to flag conflicts where today has a late meeting (after 6 PM) and tomorrow has an early meeting (before 9 AM).  
**Schedule**: Cron expression `0 10 * * *` (daily at 10 AM).  

---

### 🦞 Lobster Changelog Weekly Scan

**Description**: Weekly Monday scan of `lobster.shahine.com/changelog` for new ideas.  
**Schedule**: Cron expression `0 9 * * 1` (Monday at 9 AM).  

---

### 🌙 Calendar Fetch Midnight

**Description**: Fetch calendars at midnight PST.  
**Schedule**: Cron expression `0 0 * * *` (daily at midnight).  

---

### 🍴 WW Daily Points Check-in

**Description**: No description provided.  
**Schedule**: Cron expression `30 17 * * *` (daily at 5:30 PM).  

---

### 🥗 WW Diet Sync

**Description**: No description provided.  
**Schedule**: Cron expression `0 4 * * *` (daily at 4 AM).
