---
layout: default
title: Mail Runtime
nav_order: 3
permalink: /mail-runtime/
---

# 📬 Mail Runtime

Provider-agnostic mail processing runtime that separates **where mail comes from** from **what OpenClaw does with it**. The core runtime lives in [carapace-mail-runtime](https://github.com/JeffSteinbok/carapace-mail-runtime); this page covers the built-in actions and related components.

## Built-in Mail Actions

The octo repo ships a private action plugin (`@octo/mail-actions`) that registers the following actions with the mail runtime's action registry. Each action receives an incoming email context and returns zero or more results (messages, agent handoffs, etc.).

| Action | Description |
|--------|-------------|
| 📦 `process_amazon_shipment` | Detects Amazon shipping and delivery emails, extracts order IDs, fetches tracking numbers from the satellite, and automatically adds or removes packages in package-tracking. |
| ✉️ `process_self_email` | Forwards emails sent to the OpenClaw inbox as tasks to the main agent, which completes the request and replies-all to the thread. |

## Related Components

These external repos provide the runtime core, mail source, and additional actions:

| Component | Repo | Description |
|-----------|------|-------------|
| 📬 Mail Runtime | [carapace-mail-runtime](https://github.com/JeffSteinbok/carapace-mail-runtime) | Rule engine, action registry, and result dispatch |
| 📮 USPS Mail Action | [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/libs/ts/mail_action_usps) | Processes USPS Informed Delivery emails |
| 📦 Package Tracking | [carapace-package-tracking](https://github.com/JeffSteinbok/carapace-package-tracking) | Carrier-agnostic package tracking service |
| ⚡ FastMail SSE | [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/fastmail-sse) | Connects to FastMail via SSE and dispatches new emails to the mail runtime |
