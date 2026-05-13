---
layout: default
title: Services
nav_order: 5
---

# Services

OpenClaw services are background processes that keep long-running automations available between conversations.


## Service Summary

| Service | Description | Docs |
|---------|-------------|------|
| 🛰️ Octo Satellite | Local secrets broker for credentialed access to Amazon and Monarch Money | [GitHub ↗](https://github.com/JeffSteinbok/octo-satellite) |
| 📡 FastMail SSE Service | Real-time email notification daemon using JMAP EventSource | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/fastmail-sse) |

---

## 🛰️ Octo Satellite

A local secrets broker that sits between OpenClaw and credentialed services. It exposes a REST API on `localhost` so OpenClaw can access sensitive data without directly holding passwords or session cookies.

**Repo:** [octo-satellite](https://github.com/JeffSteinbok/octo-satellite)

### Providers

| Provider | Auth Method | Capabilities |
|----------|-------------|--------------|
| **Amazon** | Browser-automated via Playwright | Order history, order details with tracking, product search, cart management |
| **Monarch Money** | API token | Account balances, net worth, spending trends, sync status, account refresh |

### How it fits together

The satellite runs as an isolated service under a separate user account. The [octo-satellite plugin](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/octo-satellite) in openclaw-hub provides the OpenClaw tool layer — it translates tool calls into REST requests against the satellite's API.

Other components also use the satellite indirectly:
- The `process_amazon_shipment` mail action (in octo) calls the satellite to look up tracking numbers for incoming Amazon shipping emails.
- The `@octo/amazon-client` library wraps the satellite's Amazon endpoints for use by internal code.
