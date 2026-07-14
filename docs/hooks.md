---
layout: default
title: Hooks
nav_order: 8
---

# Hooks

Hooks are event-driven entry points that react to real-world signals instead of running on a timer.

Octo currently publishes **3 hooks** in the public bundle.

| | Hook | Endpoint | Description |
|---|------|----------|-------------|
| 🪝 | [GitHub Issues](hooks/coding) | `/hooksproxy/github-issues` | Receives GitHub issue and pull request events via HMAC-SHA256 webhook. Routed through webhook-proxy for auth validation before reaching OpenClaw. Triggers the coding agent for triage, planning, and lifecycle automation. |
| 🪝 | [Home Assistant Events](hooks/hass-hooks) | `/hooks/hass` | Receives HA automation webhooks (motion, camera/LLMVision detections, doorbell) and responds with camera collage analysis via Discord |
| 🪝 | [LAN Notify Relay](hooks/notify) | `/hooks/notify` | Relays notifications from LAN services directly to Discord DM without interpretation |
