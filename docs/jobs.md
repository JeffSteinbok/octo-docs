---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This page provides information about scheduled jobs that perform automated tasks within the system. Each job is designed to address specific operational needs, such as data fetching or configuration backups, and runs on a predefined schedule.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at specific intervals or times.
- **Cron Scheduling**: Defines jobs that run based on a cron expression.
- **Interval Scheduling**: Defines jobs that run at fixed intervals in milliseconds.
- **Time Zones**: Some jobs are scheduled in specific time zones.

## Scheduled Jobs

### 🕒 Calendar Fetch Hourly

**Description**: Fetches calendar data hourly between 7 AM and 5 PM PST.  
**Schedule**: Cron expression `0 7-17 * * *` in the `America/Los_Angeles` time zone.  

---

### 🕛 Calendar Fetch Midnight

**Description**: Fetches calendar data at midnight PST.  
**Schedule**: Cron expression `0 0 * * *` in the `America/Los_Angeles` time zone.  

---

### 📦 Config Backup

**Description**: Backs up the `openclaw.json` configuration file daily. Only commits changes if the file has been modified.  
**Schedule**: Runs every 86,400,000 milliseconds (24 hours).  

## How It Works

1. **Job Scheduling**: Each job is configured with a schedule, either using a cron expression or a fixed interval in milliseconds.
2. **Execution**: Jobs automatically execute at their scheduled times.
3. **Purpose-Specific Tasks**: Each job performs a specific function, such as fetching data or backing up configurations.
4. **Time Zone Awareness**: Jobs scheduled with cron expressions account for the specified time zone, ensuring accurate execution timing.
