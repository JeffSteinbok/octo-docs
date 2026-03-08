---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This document provides an overview of the background services available in the system. These services are designed to handle specific tasks, such as real-time notifications, to enhance functionality and improve user experience.

## Key Concepts

- Background services operate independently to perform specialized tasks.
- Each service is designed to integrate seamlessly with external systems and internal components.
- Services are event-driven and operate in real-time where applicable.

## Background Services

### 📧 FastMail SSE Service

**Description:**  
The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor new emails arriving in the Inbox. Upon detecting a new email, it formats the notification and sends it through OpenClaw's message system.

**Purpose:**  
This service ensures users receive timely notifications about new emails, improving responsiveness and communication efficiency.
