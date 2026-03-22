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
- **Schedule**: Specifies when and how often the job runs, using either cron expressions or interval-based timing.
- **Time Zone**: All schedules are specified in the `America/Los_Angeles` time zone unless otherwise noted.

## Scheduled Jobs

### 🕒 calendar-fetch-hourly

- **Description**: Fetch calendars hourly between 7 AM and 5 PM PST.
- **Schedule**: Cron expression: `0 7-17 * * *`  
  Time zone: America/Los_Angeles

---

### 🗂️ config-backup

- **Description**: Backup `openclaw.json` to Git daily. Commits only if changes are detected.
- **Schedule**: Every 24 hours (86400000 ms)

---

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST.
- **Schedule**: Cron expression: `0 0 * * *`  
  Time zone: America/Los_Angeles

---

### 🌅 evening-briefing

- **Description**: Weekday 9 PM briefing to summarize tasks scheduled for the next morning.
- **Schedule**: Cron expression: `0 22 * * 0-4`  
  Time zone: America/Los_Angeles

---

### 📊 portfolio-closing-briefing

- **Description**: *No description provided.*
- **Schedule**: Cron expression: `0 21 * * 1-5`  
  Time zone: America/Los_Angeles

---

### ⏰ weekend-morning-alarm-reminder

- **Description**: *No description provided.*
- **Schedule**: Cron expression: `0 22 * * 5,6`  
  Time zone: America/Los_Angeles

---

### 📦 Daily package delivery check

- **Description**: *No description provided.*
- **Schedule**: Cron expression: `0 8 * * *`  
  Time zone: America/Los_Angeles

---

### ✈️ nicole-flight-DL347-checkin

- **Description**: *No description provided.*
- **Schedule**: Cron expression: `0 8,10,11 * * *`  
  Time zone: America/Los_Angeles

---

### 🩺 daily-health-check

- **Description**: Daily health check to verify email functionality. Sends a direct message to Jeff if any issues are detected.
- **Schedule**: Cron expression: `0 9 * * *`  
  Time zone: America/Los_Angeles
