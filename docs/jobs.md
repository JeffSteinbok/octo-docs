---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their execution schedules. These jobs are designed to automate recurring tasks, ensuring consistent and timely operations.

## Key Concepts

- **Job Name**: A unique identifier for each scheduled job.
- **Description**: A brief explanation of the job's purpose.
- **Schedule**: Defines when and how often the job runs, using either cron expressions or fixed intervals.
- **Time Zone**: Specifies the time zone for the job's schedule.

## How It Works

Each job is configured with a schedule that determines its execution frequency. Schedules are defined using either:
- **Cron expressions**: Specify precise times and days for execution.
- **Fixed intervals**: Define a recurring time period in milliseconds.

Jobs are executed automatically based on their defined schedules.

## Scheduled Jobs

### 🗓️ Calendar Fetch Hourly

- **Description**: Fetch calendars hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron-based, runs at the start of every hour from 7 AM to 5 PM PST.
- **Cron Expression**: `0 7-17 * * *`
- **Time Zone**: America/Los_Angeles

---

### 🛠️ Config Backup

- **Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Runs every 24 hours.
- **Interval**: 86,400,000 milliseconds (24 hours)

---

### 🌙 Calendar Fetch Midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron-based, runs daily at midnight PST.
- **Cron Expression**: `0 0 * * *`
- **Time Zone**: America/Los_Angeles

---

### 🌅 Evening Briefing

- **Description**: Weekday 9 PM briefing to prepare for the next morning.
- **Schedule**: Cron-based, runs at 9 PM PST on weekdays (Sunday through Thursday).
- **Cron Expression**: `0 22 * * 0-4`
- **Time Zone**: America/Los_Angeles

---

### 📈 Portfolio Closing Briefing

- **Description**: (No description provided)
- **Schedule**: Cron-based, runs at 9 PM PST on weekdays (Monday through Friday).
- **Cron Expression**: `0 21 * * 1-5`
- **Time Zone**: America/Los_Angeles

---

### ⏰ Weekend Morning Alarm Reminder

- **Description**: (No description provided)
- **Schedule**: Cron-based, runs at 10 PM PST on weekends (Friday and Saturday).
- **Cron Expression**: `0 22 * * 5,6`
- **Time Zone**: America/Los_Angeles

---

### 📦 Daily Package Delivery Check

- **Description**: (No description provided)
- **Schedule**: Cron-based, runs daily at 8 AM PST.
- **Cron Expression**: `0 8 * * *`
- **Time Zone**: America/Los_Angeles
