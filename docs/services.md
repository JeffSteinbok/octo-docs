---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This page provides an overview of background services designed to support real-time and asynchronous operations. These services enable seamless integration and efficient communication between systems, solving specific operational challenges such as real-time notifications.

## Key Concepts

- Background services operate independently to handle specific tasks.
- Services are designed to integrate with external systems and protocols.
- Each service fulfills a distinct purpose, such as real-time notifications or data processing.

## FastMail SSE Service 📧

### Description

The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource, monitors new emails in one or more mailboxes, formats notifications, and sends them via OpenClaw's message system.

### Purpose

This service ensures users receive timely notifications for new emails, enabling efficient communication and responsiveness.
