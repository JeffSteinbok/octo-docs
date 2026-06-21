---
layout: default
title: Hooks
nav_order: 6
---

# Hooks

Hooks are event-driven entry points that react to real-world signals instead of running on a timer.

Octo currently publishes **2 hooks** in the public bundle.

| | Hook | Endpoint | Description |
|---|------|----------|-------------|
| 🪝 | [Home Assistant Events](hooks/hass-hooks) | `/hooks/hass` | Receives HA automation webhooks (motion, camera/LLMVision detections, doorbell) and responds with camera collage analysis via Discord |
| 🪝 | [LAN Notify Relay](hooks/notify) | `/hooks/notify` | Relays notifications from LAN services directly to Discord DM without interpretation |
