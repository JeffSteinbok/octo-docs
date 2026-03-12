---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This page provides an overview of the background services available. These services are designed to handle specific tasks such as real-time notifications, ensuring smooth and efficient operations for external developers integrating with the system.

## Key Concepts

- Background services operate independently to perform specialized tasks.
- Services are designed to integrate with external systems and provide real-time functionality.
- Notifications and data processing are key features of these services.

## FastMail SSE Service 📧

### Description

The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor new emails arriving in the Inbox. Upon detecting new emails, it formats notifications and sends them via OpenClaw's message system.

### Purpose

This service ensures timely delivery of email notifications, enabling external systems to act on new messages as they arrive. It simplifies the process of monitoring inbox activity and provides formatted notifications for downstream consumption.
