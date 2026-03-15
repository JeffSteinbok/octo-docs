---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This page provides an overview of background services designed to support real-time and asynchronous operations. These services enable developers to integrate and leverage functionality such as notifications and event handling in their applications.

## Key Concepts

- Background services operate independently to provide specific functionalities.
- Services are designed to handle real-time or asynchronous tasks.
- Each service has a distinct purpose and integrates with external systems or APIs.

## FastMail SSE Service 📧

### Description

The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor new emails in one or more mailboxes. When a new email is detected, the service formats notifications and sends them via OpenClaw's message system.

### Purpose

This service enables applications to receive real-time notifications for new emails, ensuring timely updates and seamless integration with FastMail's email infrastructure.
