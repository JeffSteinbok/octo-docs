---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This document provides an overview of the background services available. These services are designed to handle specific tasks, such as real-time notifications, to support seamless functionality and improve user experience.

## Key Concepts

- **Background Services**: Independent processes that perform specific tasks in the system.
- **Real-Time Notifications**: Services that monitor external systems and deliver updates as events occur.
- **EventSource Integration**: A mechanism for subscribing to and processing live updates from external sources.

## How It Works

1. The service connects to an external system or API to monitor for specific events.
2. When an event is detected, the service processes the data and formats it as needed.
3. The processed data is sent to the appropriate destination, such as a messaging system, for further handling or user notification.

## List of Services

### FastMail SSE Service

- **Description**: The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor for new emails in the Inbox. When a new email is detected, the service formats the notification and sends it via OpenClaw's message system.
- **Purpose**: To provide users with timely notifications of new emails in their FastMail Inbox.
