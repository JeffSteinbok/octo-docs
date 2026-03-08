---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their execution schedules. These jobs automate recurring tasks, ensuring consistent and timely operations.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at predefined intervals or times.
- **Cron Schedule**: A time-based job scheduler using cron expressions.
- **Interval Schedule**: A job scheduler that runs tasks at fixed intervals.

## Scheduled Jobs

### 🕒 Calendar Fetch Hourly

**Description**: Fetches calendar data hourly between 7:00 AM and 5:00 PM PST.  
**Schedule**: Cron schedule, runs at the start of each hour from 7:00 AM to 5:00 PM PST.  
**Cron Expression**: `0 7-17 * * *`  
**Time Zone**: America/Los_Angeles  

---

### 🌙 Calendar Fetch Midnight

**Description**: Fetches calendar data at midnight PST.  
**Schedule**: Cron schedule, runs daily at 12:00 AM PST.  
**Cron Expression**: `0 0 * * *`  
**Time Zone**: America/Los_Angeles  

---

### 💾 Config Backup

**Description**: Backs up the `openclaw.json` configuration file daily. The backup is only committed if changes are detected.  
**Schedule**: Interval schedule, runs every 24 hours (86,400,000 milliseconds).
