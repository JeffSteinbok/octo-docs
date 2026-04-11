---
layout: default
title: Hooks
nav_order: 6
has_children: true
---

# Hooks

Hooks are event-driven entry points that react to real-world signals instead of running on a timer.

Octo currently publishes **1 hook** in the public bundle.

| | Hook | Description | Sections |
|---|------|-------------|:--------:|
| 🪝 | [Hass Hooks](hooks/hass-hooks) | Handle Home Assistant webhook events from `/hooks/hass`. When something interesting happens on any camera, pull all outdoor cameras, do a full situational analysis, and send a concise Discord summary with the most relevant image. | 7 |
