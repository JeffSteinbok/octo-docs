---
layout: default
title: Mail Runtime
nav_order: 3
---

# Mail Runtime

The mail runtime is the shared rule-and-action layer behind OpenClaw's mail processing. It is documented separately from background services because it is a reusable runtime subsystem rather than a daemon.

## What lives here

- [Shared Mail Runtime](mail-runtime/shared_mail_runtime) — the provider-agnostic envelope, rule, and action runtime used by mail sources
- [Package Tracking Core](mail-runtime/package-tracking) — the tracking subsystem behind the built-in `detect_tracking` rule action
- [USPS Mail Runtime](mail-runtime/usps) — the USPS-specific action module registered into the shared mail runtime

Background services such as [FastMail SSE](services/fastmail-sse) call into this runtime; they do not own the runtime itself.
