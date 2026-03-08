---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This page provides an overview of the background services available in the system. These services are designed to handle specific tasks, such as real-time notifications, to enhance functionality and improve user experience.

## Key Concepts

- Background services operate independently to perform specific tasks.
- Each service is designed to integrate seamlessly with external systems or internal components.
- Services are purpose-built to handle specialized operations, such as real-time notifications.

## Background Services

### 📧 FastMail SSE Service

**Description**:  
The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor new emails arriving in the Inbox. When a new email is detected, the service formats a notification and sends it via OpenClaw's message system.

**Purpose**:  
This service ensures users receive timely notifications for new emails, improving communication efficiency and responsiveness.
