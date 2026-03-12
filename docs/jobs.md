---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs available in the system. These jobs automate recurring tasks, such as fetching calendar data or backing up configuration files, to ensure consistent and reliable operation.

## Key Concepts

- **Scheduled Jobs**: Automate repetitive tasks based on predefined schedules.
- **Cron Expressions**: Define specific times for job execution.
- **Time Zones**: Jobs may operate in specific time zones.
- **Enabled Status**: Indicates whether a job is active.

## Scheduled Jobs

### 🕒 Calendar Fetch Hourly

**Description**: Fetch calendars hourly between 7 AM and 5 PM PST.  
**Schedule**: Cron expression `0 7-17 * * *` in the `America/Los_Angeles` time zone.  
**Purpose**: Ensures calendar data is updated throughout the day.

---

### 💾 Config Backup

**Description**: Backup `openclaw.json` to Git daily. Commits changes only if the file has been modified.  
**Schedule**: Runs every 24 hours (`86400000ms`).  
**Purpose**: Maintains a daily backup of critical configuration files.

---

### 🌙 Calendar Fetch Midnight

**Description**: Fetch calendars at midnight PST.  
**Schedule**: Cron expression `0 0 * * *` in the `America/Los_Angeles` time zone.  
**Purpose**: Updates calendar data at the start of each day.
