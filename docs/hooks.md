---
layout: default
title: Hooks
nav_order: 8
---

# Hooks

Hooks are event-driven entry points that react to real-world signals instead of running on a timer.

Hooks reach OpenClaw in one of two ways:

- **Through the [Webhook Proxy](services/webhook-proxy)** (`/hooksproxy/...`) for senders on the public internet. The proxy checks each sender's own auth (such as GitHub's HMAC signature), can filter out events that shouldn't wake an agent, and forwards the rest with OpenClaw's hooks token added, so that token never leaves the machine.
- **Directly** (`/hooks/...`) for senders that can hold OpenClaw's hooks token themselves, such as Home Assistant and LAN services.

Apps that hold a conversation with Octo, rather than firing events at it, are covered under [Connected Apps](connected-apps).

Octo currently publishes **3 hooks** in the public bundle.

| | Hook | Endpoint | Description |
|---|------|----------|-------------|
| 🪝 | [GitHub Issues](hooks/coding) | `/hooksproxy/github-issues` | Receives GitHub issue and pull request events via HMAC-SHA256 webhook. Routed through webhook-proxy for auth validation before reaching OpenClaw. Triggers the coding agent for triage, planning, and lifecycle automation. |
| 🪝 | [Home Assistant Events](hooks/hass-hooks) | `/hooks/hass` | Receives HA automation webhooks (motion, camera/LLMVision detections, doorbell) and responds with camera collage analysis via Discord |
| 🪝 | [LAN Notify Relay](hooks/notify) | `/hooks/notify` | Relays notifications from LAN services directly to Discord DM without interpretation |
