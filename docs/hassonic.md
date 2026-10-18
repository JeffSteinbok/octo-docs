---
layout: default
title: Hassonic
parent: Connected Apps
grand_parent: Agents & Channels
nav_order: 1
---

# Hassonic

[Hassonic](https://github.com/JeffSteinbok/Hassonic-iOS) is a native iOS app for Home Assistant. Its assistant feature sends spoken or typed requests ("put the Seahawks game on", "turn off the family room lights") to Octo, which carries them out through Home Assistant.

This page covers only the OpenClaw side. For the app itself, see the [Hassonic-iOS repo on GitHub](https://github.com/JeffSteinbok/Hassonic-iOS).

## How it connects

- The app connects to the OpenClaw gateway as a paired device over the gateway WebSocket.
- It talks only to the dedicated `hassonic` agent. It can't reach `main` or any other agent.
- It requests the `operator.read`, `operator.write` and `operator.approvals` scopes. OpenClaw passes the connection's scopes on to each run, and its plugin-approval calls need `operator.approvals`.

## The `hassonic` agent

The agent has a deliberately small tool surface:

| Tool | Purpose |
|------|---------|
| `hass_state_get`, `hass_state_list` | Read Home Assistant state |
| `hass_service_call` | Call an allowlisted Home Assistant action |
| `web_search`, `web_fetch` | Look things up, e.g. which channel a game is on |

It can't send messages, read files, run commands or change automations. See [Agents & Channels](agents-channels) for how it compares to the other agents.

## Safety checks

Every Home Assistant action goes through the [Hass Guard](plugins/hass-guard) plugin before it runs:

1. **Allowlist.** Only listed domains and services can be called: lights, switches, fans, media players, remotes, scenes, climate, covers, input helpers and three named TV scripts. Calls without an `entity_id`, aimed at `all`, or targeting an entity from another domain are blocked.
2. **Safety rating.** Each allowed call is rated by the agent's decision model, [TypeSafe AI](https://docs.openclaw.ai/plugins/typesafe)'s Jev, as "routine and safe to do without asking?". At 85% or higher it runs.
3. **Blocked with a reason.** Below 85%, or when the check is unavailable, the call is not run. The agent is told why and passes the explanation back to the app.
