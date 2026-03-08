# Services Overview

## Overview

This document provides an overview of the background services available in the system. These services are designed to handle specific tasks, such as real-time email notifications, to ensure smooth and efficient operations.

## Key Concepts

- **Background Services**: Independent components that perform specific tasks in the system.
- **Real-Time Notifications**: Services that monitor external systems and trigger actions based on events.

## How It Works

1. The service connects to an external system or data source.
2. It monitors for specific events or changes in the external system.
3. When an event is detected, the service processes the data and triggers the appropriate action.

## List of Services

### FastMail SSE Service

- **Description**: A real-time email notification daemon.
- **Purpose**: Connects to FastMail's JMAP EventSource to monitor for new emails in the Inbox. When a new email is detected, the service formats the notification and sends it via OpenClaw's message system.
