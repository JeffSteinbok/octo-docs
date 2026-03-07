---
output: services.md
title: Services
nav_order: 4
data_source: services
overrides:
  fastmail-sse: >-
    Monitors an email inbox in real time using Server-Sent Events (SSE).
    When new mail arrives, it formats a notification and delivers it to
    the configured messaging channel. Automated and marketing emails are
    filtered out. Calendar RSVP responses are detected and displayed with
    appropriate status indicators.
---

<!-- instructions:
  Lists long-running background services that watch for external events
  and route notifications through the OpenClaw system.

  For each service, show: name, description (from overrides or config),
  and running/stopped status. The "overrides" map provides richer
  descriptions keyed by service name.
-->

Services are long-running background processes that watch for events
and route notifications through the OpenClaw system.

{{ items }}
