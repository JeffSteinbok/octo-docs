---
layout: default
parent: External Integrations
title: Hooks
nav_order: 3
---

# Hooks

A hook is a web address on the Gateway that another system calls when something happens, such as a doorbell press or a GitHub label change. Each call starts a turn for one agent, so Octo reacts to events as they happen instead of on a schedule (for timed work, see [Scheduled Tasks](scheduled-tasks)).

Every call to OpenClaw's hooks endpoint (`/hooks/...`) must carry OpenClaw's hooks token. Senders reach it in one of two ways:

- **Through the [Webhook Proxy](services/webhook-proxy)**, for senders that shouldn't hold that token: GitHub, from the public internet through Tailscale Funnel (`/hooksproxy/...`), and Home Assistant, on the home network. The proxy checks each sender's own credential (such as GitHub's HMAC signature), drops events that shouldn't wake an agent, and forwards the rest with the hooks token added, so that token never leaves the Mac mini.
- **Directly**, for services on the home network that hold the hooks token themselves.

Apps that hold a conversation with Octo, rather than sending it events, are covered under [Connected Apps](connected-apps).

Octo publishes **3 hooks**:

| | Hook | Endpoint | Description |
|---|------|----------|-------------|
| 🪝 | [GitHub Issues](hooks/coding) | `/hooksproxy/github-issues` | GitHub issue label changes, signed with HMAC-SHA256 and checked by the Webhook Proxy, start the coding agent on the next step of the [issue lifecycle](harness/issue-lifecycle). |
| 🪝 | [Home Assistant Events](hooks/hass-hooks) | `/hooks/hass` | Home Assistant reports motion, LLM Vision detections and doorbell presses; the hass-hooks agent sends a one-line summary with the camera snapshot on Discord. |
| 🪝 | [LAN Notify Relay](hooks/notify) | `/hooks/notify` | Forwards notifications from services on the home network to the owner as Discord DMs, word for word. |
