---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This page provides an overview of background services that facilitate various functionalities. These services are designed to handle specific tasks such as real-time notifications, ensuring seamless integration and communication across systems.

## Key Concepts

- Background services operate independently to perform specialized tasks.
- Each service is tailored to solve a specific problem or provide a distinct functionality.
- Services interact with external systems and internal messaging frameworks.

## FastMail SSE Service 📧

### Description

The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor new emails in one or more mailboxes. When new emails are detected, the service formats notifications and sends them via OpenClaw's message system.

### Purpose

This service ensures users receive timely notifications about new emails, enhancing responsiveness and communication efficiency.
