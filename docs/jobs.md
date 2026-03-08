---
layout: default
title: Scheduled Jobs
nav_order: 6
---

# Jobs Overview

## Overview

This document provides an overview of the scheduled jobs available in the system. These jobs perform automated tasks such as fetching calendar data and backing up configuration files. Each job is configured with a specific schedule and purpose to ensure timely and efficient execution.

## Key Concepts

- **Scheduled Jobs**: Automated tasks that run at predefined intervals or times.
- **Job Schedule**: Defines when and how often a job runs, using either cron expressions or interval-based timing.
- **Job Purpose**: Each job has a specific function, such as data fetching or file backup.

## How It Works

Scheduled jobs are configured to run automatically based on their defined schedules. The system supports two types of scheduling:
- **Cron-based scheduling**: Jobs run at specific times based on a cron expression.
- **Interval-based scheduling**: Jobs run at regular intervals defined in milliseconds.

Each job is enabled by default and performs its designated task according to its schedule.

## List of Scheduled Jobs

### `calendar-fetch-hourly`

- **Description**: Fetches calendar data hourly between 7:00 AM and 5:00 PM PST.
- **Schedule**: 
  - **Type**: Cron
  - **Expression**: `0 7-17 * * *`
  - **Time Zone**: America/Los_Angeles

### `config-backup`

- **Description**: Backs up the `openclaw.json` configuration file to Git daily. The job commits changes only if the file has been modified.
- **Schedule**: 
  - **Type**: Interval
  - **Interval**: Every 24 hours (86,400,000 milliseconds)

### `calendar-fetch-midnight`

- **Description**: Fetches calendar data at midnight PST.
- **Schedule**: 
  - **Type**: Cron
  - **Expression**: `0 0 * * *`
  - **Time Zone**: America/Los_Angeles`
