---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This document provides an overview of the background services available in the system. These services are designed to handle specific tasks, enabling seamless functionality and integration for various features.

## Key Concepts

- Background services operate independently to perform specific tasks.
- Each service is designed to address a particular need, such as real-time notifications or data processing.
- Services communicate with external systems and internal components to deliver their functionality.

## How It Works

Background services run continuously in the system, monitoring specific events or data sources. When a relevant event occurs, the service processes the information and performs the necessary actions, such as sending notifications or updating records. These services are designed to operate efficiently and reliably, ensuring smooth operation of the system.

## FastMail SSE Service 📧

**Description:**  
The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor new emails arriving in the Inbox. When a new email is detected, the service formats a notification and sends it through OpenClaw's message system.

**Purpose:**  
This service ensures users receive timely notifications for new emails, enhancing communication efficiency and user experience.
