---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This document provides an overview of the background services available in the system. These services are designed to handle specific tasks, enabling seamless functionality and enhancing the overall user experience. Each service operates independently to perform its designated role.

## Key Concepts

- Background services operate independently to handle specific tasks.
- Services are designed to integrate with external systems and provide real-time functionality.
- Each service has a defined purpose and operates within its scope to support the system.

## How It Works

Each service runs as a standalone process, performing its designated function. These services may interact with external systems, monitor specific events, and trigger actions based on predefined conditions. The services are designed to work together to ensure smooth and efficient operations.

## List of Services

### FastMail SSE Service

- **Description**: The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor new emails arriving in the Inbox. When a new email is detected, the service formats the notification and sends it via OpenClaw's message system.
- **Purpose**: Enables real-time email notifications by integrating with FastMail and delivering timely updates to users.
