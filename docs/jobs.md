---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This page provides information about scheduled jobs that automate recurring tasks. Each job has a specific purpose, schedule, and configuration to ensure consistent execution. These jobs help streamline processes such as data fetching and backups.

## Key Concepts

- **Scheduled Jobs**: Automated tasks configured to run at specific intervals.
- **Cron Scheduling**: Defines execution times using cron expressions.
- **Time Zones**: Some jobs specify a time zone for accurate scheduling.
- **Conditional Execution**: Certain jobs only perform actions if specific conditions are met.

## How It Works

Scheduled jobs are configured with a defined schedule and purpose. Depending on the job, execution times are determined using either cron expressions or interval-based scheduling. Jobs run automatically based on their configuration and do not require manual intervention.

## Scheduled Jobs

### 📅 Calendar Fetch Hourly

**Description**: Fetch calendars hourly between 7am and 5pm PST.  
**Schedule**: Cron expression `0 7-17 * * *` in the `America/Los_Angeles` time zone.  
**Purpose**: Ensures calendar data is updated regularly throughout the day.

---

### 🛠️ Config Backup

**Description**: Backup `openclaw.json` to Git daily. Only commits changes if the file has been modified.  
**Schedule**: Runs every 24 hours (`86400000ms`).  
**Purpose**: Maintains a daily backup of configuration data to ensure recovery and version control.

---

### 🌙 Calendar Fetch Midnight

**Description**: Fetch calendars at midnight PST.  
**Schedule**: Cron expression `0 0 * * *` in the `America/Los_Angeles` time zone.  
**Purpose**: Updates calendar data at the start of each day.
