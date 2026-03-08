---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of scheduled jobs available in the system. Scheduled jobs are automated tasks that run at predefined intervals to perform essential operations such as data fetching and backups. These jobs help ensure the system remains up-to-date and reliable without requiring manual intervention.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that execute at specific times or intervals.
- **Job Schedules**: Define when and how often a job runs, using either cron expressions or time intervals.
- **Job Descriptions**: Each job has a specific purpose, such as fetching data or creating backups.

## How It Works

Scheduled jobs are configured with specific schedules and run automatically based on their defined timing. Jobs use either cron expressions or fixed time intervals to determine their execution schedule. Each job is enabled by default and performs a specific function critical to the system's operation.

## List of Scheduled Jobs

### Calendar Fetch (Hourly)

- **Name**: `calendar-fetch-hourly`
- **Description**: Fetches calendar data hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: 
  - **Type**: Cron
  - **Expression**: `0 7-17 * * *`
  - **Time Zone**: America/Los_Angeles

### Calendar Fetch (Midnight)

- **Name**: `calendar-fetch-midnight`
- **Description**: Fetches calendar data at midnight PST.
- **Schedule**: 
  - **Type**: Cron
  - **Expression**: `0 0 * * *`
  - **Time Zone**: America/Los_Angeles

### Configuration Backup

- **Name**: `config-backup`
- **Description**: Backs up the `openclaw.json` configuration file to Git daily. Only commits changes if the file has been modified.
- **Schedule**: 
  - **Type**: Fixed Interval
  - **Interval**: Every 24 hours (86,400,000 milliseconds)
