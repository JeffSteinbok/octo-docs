---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their execution schedules. These jobs are designed to automate recurring tasks, ensuring consistent and timely operations.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled task.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: Defines when and how often the job runs, using either cron expressions or interval-based timing.
- **Time Zone**: All schedules are specified in the `America/Los_Angeles` time zone unless otherwise noted.

## Scheduled Jobs

### 🗓️ Calendar Fetch Hourly

- **Description**: Fetches calendar data hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: Cron-based, runs at the start of every hour between 7:00 AM and 5:00 PM (inclusive).

### 🗂️ Config Backup

- **Description**: Backs up `openclaw.json` to Git daily. Commits changes only if the file has been modified.
- **Schedule**: Runs every 24 hours.

### 🌙 Calendar Fetch Midnight

- **Description**: Fetches calendar data at midnight PST.
- **Schedule**: Cron-based, runs daily at 12:00 AM.

### 🌅 Evening Briefing

- **Description**: Provides a weekday 9:00 PM briefing about the next morning's schedule.
- **Schedule**: Cron-based, runs at 9:00 PM Monday through Friday.

### 📈 Portfolio Closing Briefing

- **Description**: (No description provided)
- **Schedule**: Cron-based, runs at 9:00 PM Monday through Friday.

### ⏰ Evening Alarm Reminder

- **Description**: Sends a nightly reminder at 10:30 PM to check the alarm if there is an early morning work meeting the next day.
- **Schedule**: Cron-based, runs daily at 10:30 PM.

### 📦 Daily Package Delivery Check

- **Description**: (No description provided)
- **Schedule**: Cron-based, runs daily at 8:00 AM.

### ✅ Daily Health Check

- **Description**: Verifies email sending functionality daily. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron-based, runs daily at 9:00 AM.

### 🕙 Late-Early Conflict Morning Check

- **Description**: Flags conflicts where today's schedule includes a late meeting (after 6:00 PM) and tomorrow's schedule includes an early meeting (before 9:00 AM).
- **Schedule**: Cron-based, runs daily at 10:00 AM.

### 🦞 Lobster Changelog Weekly Scan

- **Description**: Scans the Lobster changelog for new ideas every Monday.
- **Schedule**: Cron-based, runs weekly at 9:00 AM on Mondays.

### 🏋️ WW Daily Points Check-in

- **Description**: (No description provided)
- **Schedule**: Cron-based, runs daily at 5:30 PM.
