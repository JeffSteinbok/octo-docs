---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs

## Overview

This page describes the scheduled jobs that automate various tasks such as calendar fetching, backups, health checks, reminders, and briefings. These jobs help streamline daily operations by running at specified times and intervals, ensuring important actions are performed reliably and consistently.

Each job is scheduled according to its purpose, with some running hourly, daily, or weekly, and others triggered by specific events. The scheduling information includes the time zone and frequency, allowing for predictable execution.

## Key Concepts

- **Scheduled Jobs**: Automated tasks configured to run at specific times or intervals.
- **Cron Scheduling**: Jobs scheduled using cron expressions for precise timing.
- **Time Zone Awareness**: Most jobs are scheduled in the America/Los_Angeles time zone.
- **Enabled/Disabled Status**: Only enabled jobs are active and will run as scheduled.
- **Job Purpose**: Each job serves a distinct operational or informational function.

## How It Works

1. Jobs are defined with a name, description, enabled status, and schedule.
2. The schedule specifies when the job should run, using either cron expressions or interval-based timing.
3. Enabled jobs execute automatically at their scheduled times.
4. Each job performs its designated task, such as fetching calendars, sending reminders, or checking system health.

## Scheduled Jobs

### 🗓️ calendar-fetch-hourly

- **Description**: Fetch calendars hourly 7am-5pm PST
- **Schedule**: Hourly at the top of the hour from 7:00 AM to 5:00 PM (America/Los_Angeles)

### 💾 config-backup

- **Description**: Backup openclaw.json to Git daily (only commits if changed)
- **Schedule**: Every 24 hours

### 📰 evening-briefing

- **Description**: Weekday 9 PM briefing: what's on tap tomorrow morning
- **Schedule**: 9:00 PM, Monday through Friday (America/Los_Angeles)

### 📈 portfolio-closing-briefing

- **Description**: *(No description provided)*
- **Schedule**: 9:00 PM, Monday through Friday (America/Los_Angeles)

### ⏰ evening-alarm-reminder

- **Description**: Nightly 10:30 PM: remind Jeff to check alarm if early morning work meeting
- **Schedule**: 10:30 PM daily (America/Los_Angeles)

### 📦 Daily package delivery check

- **Description**: *(No description provided)*
- **Schedule**: 8:00 AM daily (America/Los_Angeles)

### 🩺 daily-health-check

- **Description**: Daily health check — verifies email sending works; DMs Jeff if anything fails
- **Schedule**: 9:00 AM daily (America/Los_Angeles)

### 🍽️ Remind Jeff to reach out to Zack Ali for dinner

- **Description**: One-shot reminder to schedule another dinner with Zack Ali
- **Schedule**: One-time (disabled)

### 🏅 WW Daily Points Check-in

- **Description**: *(No description provided)*
- **Schedule**: 5:30 PM daily (America/Los_Angeles)

### 🔄 late-early-conflict-morning-check

- **Description**: 10 AM daily: flag if today has late meeting (after 6 PM) and tomorrow has early meeting (before 9 AM)
- **Schedule**: 10:00 AM daily (America/Los_Angeles)

### 🦞 Lobster changelog weekly scan

- **Description**: Weekly Monday scan of lobster.shahine.com/changelog for new ideas
- **Schedule**: 9:00 AM every Monday (America/Los_Angeles)

### 🌙 calendar-fetch-midnight

- **Description**: Fetch calendars at midnight PST
- **Schedule**: 12:00 AM daily (America/Los_Angeles)

### 🥗 ww-diet-sync

- **Description**: *(No description provided)*
- **Schedule**: 4:00 AM daily (America/Los_Angeles)
