---
layout: default
title: Services
nav_order: 5
---

# Services Overview

## Overview

This page provides an overview of background services that facilitate various functionalities. These services are designed to handle specific tasks such as real-time notifications, ensuring seamless integration and efficient operations for external developers.

## Key Concepts

- Background services operate independently to perform specialized tasks.
- Each service is designed to integrate with external systems or APIs.
- Services are responsible for processing and delivering data to other systems.

## FastMail SSE Service 📧

### Description

The FastMail SSE Service is a real-time email notification daemon. It connects to FastMail's JMAP EventSource to monitor new emails in one or more mailboxes. Upon detecting new emails, it formats notifications and sends them via OpenClaw's message system.

### Purpose

This service ensures timely delivery of email notifications, enabling external systems to react to new emails as they arrive.
