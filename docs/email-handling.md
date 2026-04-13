---
layout: default
title: Email Handling
nav_order: 6
has_children: true
---

# Email Handling

Email handling covers the long-running mail ingestion surfaces and the shared runtime that turns provider-specific events into reusable OpenClaw mail workflows.

## What lives here

- [FastMail SSE Service](services/fastmail-sse) — the real-time ingestion daemon for FastMail mail events
- [Shared Mail Runtime](services/shared_mail_runtime) — the provider-agnostic rule/action runtime used by mail sources
- [USPS Mail Runtime](services/shared-mail-runtime-usps) — the USPS-specific action module layered on top of the shared mail runtime

This section exists separately from the generic services list because the mail runtime is a shared library-backed subsystem, not just a standalone daemon.
