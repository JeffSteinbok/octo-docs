---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This document provides an overview of the background services available in the system. Each service is designed to perform a specific function, solving key problems such as real-time notifications and message processing.

## Key Concepts

- Background services operate independently to handle specific tasks.
- Services are designed to integrate with external systems and provide seamless functionality.
- Notifications and messaging are core components of the system.

## Background Services

### 📧 FastMail SSE Service

**Description:**  
The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor new emails arriving in the Inbox. When a new email is detected, the service formats a notification and sends it through OpenClaw's message system.

**Purpose:**  
This service ensures users receive timely notifications for new emails, enhancing communication efficiency.
