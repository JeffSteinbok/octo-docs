---
output: services.md
title: Services
nav_order: 5
data_keys:
  - services
---

Generate a documentation section for OpenClaw **services**.

Services are long-running background processes that watch for external events
and route notifications through the OpenClaw system.

Use the `services` array from the provided data.

For each service, generate:
1. An H2 heading with ⚙️ and the service name (e.g., `## ⚙️ service-name`)
2. A description paragraph
3. If the service `type` is `"systemd"`, add: **Deployment:** systemd user service (auto-restart on failure)
4. A horizontal rule (`---`) divider

### Manual Overrides

For the services listed below, use the provided description instead of the
raw data description:

**fastmail-sse** — Monitors an email inbox in real time using Server-Sent Events (SSE).
When new mail arrives, it formats a notification and delivers it to the configured
messaging channel. Automated and marketing emails are filtered out. Calendar RSVP
responses are detected and displayed with appropriate status indicators.

Keep descriptions concise and factual.
