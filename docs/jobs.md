---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs

## Overview

This page provides an overview of scheduled jobs that automate recurring tasks such as calendar fetching, backups, health checks, reminders, and briefings. These jobs help streamline daily operations by ensuring important actions are performed reliably and on schedule.

Each job is configured with a specific schedule and purpose, enabling consistent execution without manual intervention.

## Key Concepts

- **Scheduled Jobs**: Automated tasks configured to run at specific times or intervals.
- **Cron Scheduling**: Many jobs use cron expressions to define their execution times.
- **Time Zones**: Schedules are set in the America/Los_Angeles time zone unless otherwise specified.
- **Enabled/Disabled Status**: Jobs can be enabled or disabled; only enabled jobs are active.
- **Purpose**: Each job serves a distinct operational or informational function.

## How It Works

1. Jobs are defined with a name, description, enabled status, and schedule.
2. Schedules use either cron expressions or interval-based timing.
3. Enabled jobs execute automatically according to their schedule.
4. Each job performs its designated task, such as fetching calendars, sending reminders, or performing health checks.

## Scheduled Jobs

### 🗓️ calendar-fetch-hourly

- **Description**: Fetch calendars hourly 7am-5pm PST
- **Schedule**: Hourly at the top of the hour, from 7:00 AM to 5:00 PM (America/Los_Angeles)

---

### 💾 config-backup

- **Description**: Backup openclaw.json to Git daily (only commits if changed)
- **Schedule**: Every 24 hours

---

### 📰 evening-briefing

- **Description**: Weekday 9 PM briefing: what's on tap tomorrow morning
- **Schedule**: 9:00 PM, Monday to Friday (America/Los_Angeles)

---

### 📈 portfolio-closing-briefing

- **Description**: *(No description provided)*
- **Schedule**: 9:00 PM, Monday to Friday (America/Los_Angeles)

---

### ⏰ evening-alarm-reminder

- **Description**: Nightly 10:30 PM: remind Jeff to check alarm if early morning work meeting
- **Schedule**: 10:30 PM daily (America/Los_Angeles)

---

### 📦 Daily package delivery check

- **Description**: *(No description provided)*
- **Schedule**: 8:00 AM daily (America/Los_Angeles)

---

### 🩺 daily-health-check

- **Description**: Daily health check — verifies email sending works; DMs Jeff if anything fails
- **Schedule**: 9:00 AM daily (America/Los_Angeles)

---

### 🍽️ Remind Jeff to reach out to Zack Ali for dinner

- **Description**: One-shot reminder to schedule another dinner with Zack Ali
- **Schedule**: One-time (disabled)

---

### 🏅 WW Daily Points Check-in

- **Description**: *(No description provided)*
- **Schedule**: 5:30 PM daily (America/Los_Angeles)

---

### ⚠️ late-early-conflict-morning-check

- **Description**: 10 AM daily: flag if today has late meeting (after 6 PM) and tomorrow has early meeting (before 9 AM)
- **Schedule**: 10:00 AM daily (America/Los_Angeles)

---

### 🦞 Lobster changelog weekly scan

- **Description**: Weekly Monday scan of lobster.shahine.com/changelog for new ideas
- **Schedule**: 9:00 AM every Monday (America/Los_Angeles)

---

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST
- **Schedule**: 12:00 AM daily (America/Los_Angeles)

---

### 🥗 ww-diet-sync

- **Description**: *(No description provided)*
- **Schedule**: 4:00 AM daily (America/Los_Angeles)
