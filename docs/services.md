# Services Overview

## Overview

This document provides an overview of the background services available in the system. These services are designed to handle specific tasks, such as real-time notifications, to ensure smooth and efficient operation of the platform.

## Key Concepts

- **Background Services**: Independent processes that perform specific tasks in the system.
- **Real-Time Notifications**: Services that monitor external systems for updates and trigger notifications as needed.
- **Integration with External APIs**: Some services connect to external APIs to retrieve or process data.

## How It Works

1. Background services run continuously to perform their designated tasks.
2. Services may connect to external APIs or systems to monitor events or retrieve data.
3. When an event of interest occurs, the service processes the data and triggers the appropriate action, such as sending a notification.

## List of Services

### FastMail SSE Service

- **Description**: A real-time email notification daemon.
- **Purpose**: Connects to FastMail's JMAP EventSource to monitor for new emails in the Inbox. When a new email is detected, it formats the notification and sends it via OpenClaw's message system.

## Common Pitfalls

- Ensure that the FastMail SSE Service has proper access to FastMail's JMAP EventSource to avoid connection issues.
- Misconfigured notification formatting may lead to incorrect or incomplete notifications being sent.
