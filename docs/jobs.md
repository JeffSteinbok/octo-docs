---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, including their purpose and scheduling details. These jobs are designed to automate recurring tasks, ensuring consistent and timely execution of critical operations.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: Defines when and how often the job runs, using either a cron expression or a time interval.
- **Time Zone**: Specifies the time zone for the job's schedule.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

**Description**: Fetches calendar data hourly between 7:00 AM and 5:00 PM PST.  
**Schedule**: Cron schedule - `0 7-17 * * *` (Hourly from 7:00 AM to 5:00 PM, Pacific Time).  

---

### 🌙 calendar-fetch-midnight

**Description**: Fetches calendar data at midnight PST.  
**Schedule**: Cron schedule - `0 0 * * *` (Daily at 12:00 AM, Pacific Time).  

---

### 📦 config-backup

**Description**: Backs up the `openclaw.json` configuration file to Git daily. Commits changes only if the file has been modified.  
**Schedule**: Runs every 24 hours (86,400,000 milliseconds).  

---

### 🌅 evening-briefing

**Description**: Provides a weekday 9:00 PM briefing on the next morning's schedule.  
**Schedule**: Cron schedule - `0 22 * * 0-4` (Sunday through Thursday at 9:00 PM, Pacific Time).  

---

### 📈 portfolio-closing-briefing

**Description**: (No description provided).  
**Schedule**: Cron schedule - `0 21 * * 1-5` (Monday through Friday at 9:00 PM, Pacific Time).  

---

### ⏰ weekend-morning-alarm-reminder

**Description**: (No description provided).  
**Schedule**: Cron schedule - `0 22 * * 5,6` (Friday and Saturday at 10:00 PM, Pacific Time).  

---

### 📦 Daily package delivery check

**Description**: (No description provided).  
**Schedule**: Cron schedule - `0 8 * * *` (Daily at 8:00 AM, Pacific Time).  

---

### ✅ daily-health-check

**Description**: Performs a daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.  
**Schedule**: Cron schedule - `0 9 * * *` (Daily at 9:00 AM, Pacific Time).
