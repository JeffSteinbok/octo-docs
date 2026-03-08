---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This document provides an overview of the available background services. These services are designed to handle specific tasks and processes, enabling seamless integration and functionality for external developers.

## Key Concepts

- Background services operate independently to perform specific tasks.
- Each service is designed to address a particular need, such as real-time notifications or data processing.
- Services interact with external systems and APIs to deliver their functionality.

## Background Services

### 📧 FastMail SSE Service

**Description**: The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor new emails arriving in the Inbox. When a new email is detected, the service formats the notification and sends it through OpenClaw's message system.

**Purpose**: This service ensures that users receive timely notifications for new emails, enhancing communication efficiency and responsiveness.
