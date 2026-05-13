---
layout: default
title: Mail Runtime
nav_order: 3
permalink: /mail-runtime/
---

# 📬 Mail Runtime

Provider-agnostic mail processing runtime that separates **where mail comes from** from **what OpenClaw does with it**.

The mail runtime has moved to its own repo:

👉 **[carapace-mail-runtime](https://github.com/JeffSteinbok/carapace-mail-runtime)** — rule engine, action registry, and result dispatch

### Related Components

| Component | Location |
|-----------|----------|
| 📮 [USPS Mail Action](https://github.com/JeffSteinbok/openclaw-hub/tree/main/libs/ts/mail_action_usps) | openclaw-hub |
| 📦 [Package Tracking](https://github.com/JeffSteinbok/carapace-package-tracking) | carapace-package-tracking |
| ⚡ [FastMail SSE Service](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/fastmail-sse) | openclaw-hub |
