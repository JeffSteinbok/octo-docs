---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs, their purposes, and their execution schedules. These jobs automate various tasks, such as data fetching, backups, and notifications, to ensure system reliability and operational efficiency.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at predefined intervals or times.
- **Cron Schedule**: A time-based job scheduler using cron expressions to define execution times.
- **Interval Schedule**: Jobs that run at regular intervals, defined in milliseconds.

## How It Works

Scheduled jobs are configured to run automatically based on their defined schedules. These schedules can either be specified using cron expressions or fixed intervals. Each job has a specific purpose, such as fetching data, sending notifications, or performing system checks. The jobs are executed in the specified time zone, ensuring consistency across operations.

## Scheduled Jobs

### 🗓️ calendar-fetch-hourly

- **Description**: Fetch calendars hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron-based, runs every hour from 7:00 AM to 5:00 PM (PST).
- **Cron Expression**: `0 7-17 * * *`
- **Time Zone**: America/Los_Angeles

---

### 💾 config-backup

- **Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Runs every 24 hours.
- **Interval**: 86,400,000 milliseconds (24 hours)

---

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron-based, runs daily at 12:00 AM (PST).
- **Cron Expression**: `0 0 * * *`
- **Time Zone**: America/Los_Angeles

---

### 🌅 evening-briefing

- **Description**: Weekday 9 PM briefing to summarize tasks for the next morning.
- **Schedule**: Cron-based, runs Monday through Friday at 9:00 PM (PST).
- **Cron Expression**: `0 22 * * 0-4`
- **Time Zone**: America/Los_Angeles

---

### 📈 portfolio-closing-briefing

- **Description**: Not provided.
- **Schedule**: Cron-based, runs Monday through Friday at 9:00 PM (PST).
- **Cron Expression**: `0 21 * * 1-5`
- **Time Zone**: America/Los_Angeles

---

### ⏰ weekend-morning-alarm-reminder

- **Description**: Not provided.
- **Schedule**: Cron-based, runs on Fridays and Saturdays at 10:00 PM (PST).
- **Cron Expression**: `0 22 * * 5,6`
- **Time Zone**: America/Los_Angeles

---

### 📦 Daily package delivery check

- **Description**: Not provided.
- **Schedule**: Cron-based, runs daily at 8:00 AM (PST).
- **Cron Expression**: `0 8 * * *`
- **Time Zone**: America/Los_Angeles

---

### 🩺 daily-health-check

- **Description**: Daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron-based, runs daily at 9:00 AM (PST).
- **Cron Expression**: `0 9 * * *`
- **Time Zone**: America/Los_Angeles
