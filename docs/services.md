---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This document provides an overview of the background services available in the system. These services are designed to handle specific tasks, such as real-time notifications, to enhance functionality and provide seamless integration with external systems.

## Key Concepts

- Background services operate independently to perform specific tasks.
- Services are designed to integrate with external systems and APIs.
- Each service has a defined purpose and operates autonomously.

## How It Works

Background services run continuously to perform their designated tasks. They often connect to external APIs or systems, monitor for specific events, and trigger actions based on those events. These services are designed to operate reliably and efficiently in the background.

## FastMail SSE Service 📧

**Description**:  
The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor for new emails in the Inbox. When a new email is detected, the service formats a notification and sends it through OpenClaw's message system.

**Purpose**:  
This service ensures users receive timely notifications for new emails, enabling faster response times and improved communication.
