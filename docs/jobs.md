---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This page provides an overview of scheduled jobs available in the system. Scheduled jobs automate recurring tasks such as data fetching and backups, ensuring consistent and timely execution without manual intervention.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at predefined intervals.
- **Cron Scheduling**: Specifies execution times using cron expressions.
- **Time Zones**: Some jobs are scheduled in specific time zones.
- **Event-Driven Execution**: Jobs execute based on their defined schedules.

## How It Works

Scheduled jobs are configured with specific schedules and purposes. Jobs can use cron expressions for precise timing or interval-based scheduling for recurring execution. Enabled jobs run automatically according to their defined schedule, ensuring tasks are performed consistently.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

**Description**: Fetch calendars hourly between 7am and 5pm PST.  
**Schedule**: Cron expression `0 7-17 * * *` in the `America/Los_Angeles` time zone.

---

### 🌙 calendar-fetch-midnight

**Description**: Fetch calendars at midnight PST.  
**Schedule**: Cron expression `0 0 * * *` in the `America/Los_Angeles` time zone.

---

### 💾 config-backup

**Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.  
**Schedule**: Runs every 24 hours (`86400000ms`).
