---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This document provides an overview of the background services available in the system. These services are designed to handle specific tasks, such as real-time notifications, to ensure seamless functionality and integration with external systems.

## Key Concepts

- Background services operate independently to perform specific tasks.
- Each service has a defined purpose and integrates with external systems as needed.
- Services are designed to enhance system functionality and user experience.

## How It Works

1. Background services run continuously to monitor specific events or data sources.
2. When a relevant event is detected, the service processes the data and performs the necessary actions.
3. Services may integrate with external systems to send notifications or trigger workflows.

## List of Services

### FastMail SSE Service

- **Description**: The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor new emails in the Inbox. When a new email is detected, the service formats the notification and sends it via OpenClaw's message system.
- **Purpose**: Enables real-time email notifications for users, ensuring timely updates and improved communication.
