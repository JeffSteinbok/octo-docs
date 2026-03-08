# Services Overview

## Overview

This document provides an overview of the background services available in the system. These services are designed to handle specific tasks, such as real-time notifications, to enhance functionality and provide seamless integration with external systems.

## Key Concepts

- **Background Services**: Independent processes that perform specific tasks in the system.
- **Real-Time Notifications**: Services that monitor external systems and deliver updates as they occur.
- **Integration**: Services that connect with external APIs or systems to provide additional functionality.

## How It Works

Background services operate independently to perform their designated tasks. For example, a service may connect to an external API, monitor for specific events, process the data, and then relay the information to other components in the system. These services ensure that tasks are handled efficiently and in real time without requiring direct user intervention.

## List of Services

### FastMail SSE Service

- **Description**: The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor for new emails in the Inbox. When a new email is detected, the service formats the notification and sends it through OpenClaw's message system.
- **Purpose**: Provides real-time email notifications by integrating with FastMail's JMAP EventSource and relaying updates to the system.

## Common Pitfalls

- Ensure that the FastMail SSE Service is properly configured to connect to FastMail's JMAP EventSource.
- Verify that the OpenClaw message system is operational to avoid notification delivery failures.
