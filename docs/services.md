---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This document provides an overview of the background services available in the system. These services are designed to handle specific tasks, such as real-time notifications, to enhance the functionality and responsiveness of the platform.

## Key Concepts

- Background services operate independently to perform specialized tasks.
- Services are designed to integrate with external systems and provide seamless functionality.
- Each service has a specific purpose and operates autonomously to fulfill its role.

## How It Works

1. Background services run continuously in the system to monitor or process specific events.
2. Each service connects to external systems or data sources as needed.
3. When a relevant event occurs, the service processes the data and triggers the appropriate actions, such as sending notifications or updating records.

## List of Services

### FastMail SSE Service

- **Description**: A real-time email notification daemon.
- **Purpose**: Connects to FastMail's JMAP EventSource to monitor new emails in the Inbox. When a new email is detected, the service formats a notification and sends it via OpenClaw's message system.
