---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This page provides an overview of scheduled jobs within the system. Scheduled jobs are automated tasks designed to perform specific operations at predefined intervals. These jobs ensure regular updates, backups, and data synchronization without manual intervention.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at specific intervals or times.
- **Cron Expressions**: Define precise schedules for jobs based on time and date.
- **Time Zones**: Some jobs operate in specific time zones to align with regional requirements.
- **Enabled Jobs**: Only jobs marked as enabled are active and executed.

## Scheduled Jobs

### 🕒 Calendar Fetch Hourly

**Description**: Fetches calendar data hourly between 7 AM and 5 PM PST.  
**Schedule**: Cron expression `0 7-17 * * *` in the `America/Los_Angeles` time zone.  
**Purpose**: Ensures calendar data is updated regularly throughout the day.

---

### 📋 Config Backup

**Description**: Backs up the `openclaw.json` configuration file to Git daily. Commits are only made if changes are detected.  
**Schedule**: Runs every 24 hours (`86400000` milliseconds).  
**Purpose**: Maintains a daily backup of configuration data for recovery and auditing purposes.

---

### 🌙 Calendar Fetch Midnight

**Description**: Fetches calendar data at midnight PST.  
**Schedule**: Cron expression `0 0 * * *` in the `America/Los_Angeles` time zone.  
**Purpose**: Ensures calendar data is updated at the start of each day.
