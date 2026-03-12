---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This page provides an overview of scheduled jobs available in the system. Scheduled jobs automate recurring tasks such as fetching calendars and backing up configuration files. Each job is configured with a specific schedule and purpose to ensure consistent and reliable execution.

## Key Concepts

- **Jobs**: Automated tasks that run on a predefined schedule.
- **Schedules**: Define when and how often a job runs, using cron expressions or interval-based timing.
- **Time Zones**: Some jobs are scheduled relative to a specific time zone.

## Scheduled Jobs

### 🕒 Calendar Fetch Hourly

**Description**: Fetch calendars hourly between 7 AM and 5 PM PST.  
**Schedule**: Cron expression `0 7-17 * * *` (Time zone: America/Los_Angeles).  
**Purpose**: Ensures calendar data is updated hourly during business hours.

---

### 🕛 Calendar Fetch Midnight

**Description**: Fetch calendars at midnight PST.  
**Schedule**: Cron expression `0 0 * * *` (Time zone: America/Los_Angeles).  
**Purpose**: Updates calendar data daily at midnight.

---

### 💾 Config Backup

**Description**: Backup `openclaw.json` to Git daily. Commits changes only if the file has been modified.  
**Schedule**: Runs every 24 hours (`everyMs: 86400000`).  
**Purpose**: Maintains a daily backup of configuration data for version control and recovery.
