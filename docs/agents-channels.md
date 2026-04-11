---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents & Channels

This page lists the agent identities, model configuration, channel policies, and session settings exported in the public bundle.

Private execution permissions, tool allowlists, and detailed channel-to-agent bindings are intentionally not included in the public bundle, so this page documents only the configuration that is published.

## Models

- **Primary model:** `github-copilot/claude-sonnet-4.6`
- **Fallback models:** `github-copilot/gpt-5.4`
- **Primary image model:** `github-copilot/claude-sonnet-4.6`

## Agents

| Agent | ID | Public Summary |
|-------|----|----------------|
| 🐙 Octo | `main` | High-level role exported; private security details are omitted from the bundle. |
| 📬 mail-agent | `mail` | High-level role exported; private security details are omitted from the bundle. |
| 🔑 Root | `root` | High-level role exported; private security details are omitted from the bundle. |
| 👨‍👩‍👧‍👦 Family | `family` | High-level role exported; private security details are omitted from the bundle. |
| 📷 HA Hooks | `hass-hooks` | handle Home Assistant webhook events from `/hooks/hass`. When something interesting happens on any camera, pull all outdoor cameras, do a full situational analysis, and send a concise Discord summary with the most relevant image. |

## 🐙 Octo

- **Agent ID:** `main`
- **Public summary:** Not explicitly exported in the public bundle.
- **Security model:** Exec settings, permissions, and tool/plugin allowlists are not exported in the public bundle.
- **Bindings:** Channel-to-agent binding details are not exported in the public bundle.
- **Published instruction sections:** `First Run`, `Every Session`, `Memory`, `Discord Messaging Style`, `Safety`, `Web Fetching & Browsing`, `External vs Internal`, `Group Chats`, `Tools`, `💓 Heartbeats - Be Proactive!`, `Alarm Reminder Logic`, `Package Tracking`, `Security Guardrails`, `Theater Seating Charts`, `Make It Yours`

## 📬 mail-agent

- **Agent ID:** `mail`
- **Public summary:** Not explicitly exported in the public bundle.
- **Security model:** Exec settings, permissions, and tool/plugin allowlists are not exported in the public bundle.
- **Bindings:** Channel-to-agent binding details are not exported in the public bundle.
- **Published instruction sections:** `First Run`, `Every Session`, `Memory`, `Safety`, `External vs Internal`, `Group Chats`, `Tools`, `💓 Heartbeats - Be Proactive!`, `Make It Yours`

## 🔑 Root

- **Agent ID:** `root`
- **Public summary:** Not explicitly exported in the public bundle.
- **Security model:** Exec settings, permissions, and tool/plugin allowlists are not exported in the public bundle.
- **Bindings:** Channel-to-agent binding details are not exported in the public bundle.
- **Published instruction sections:** `First Run`, `Every Session`, `Memory`, `Safety`, `External vs Internal`, `Group Chats`, `Tools`, `💓 Heartbeats - Be Proactive!`, `Make It Yours`

## 👨‍👩‍👧‍👦 Family

- **Agent ID:** `family`
- **Public summary:** Not explicitly exported in the public bundle.
- **Security model:** Exec settings, permissions, and tool/plugin allowlists are not exported in the public bundle.
- **Bindings:** Channel-to-agent binding details are not exported in the public bundle.

## 📷 HA Hooks

- **Agent ID:** `hass-hooks`
- **Public summary:** handle Home Assistant webhook events from `/hooks/hass`. When something interesting happens on any camera, pull all outdoor cameras, do a full situational analysis, and send a concise Discord summary with the most relevant image.
- **Security model:** Exec settings, permissions, and tool/plugin allowlists are not exported in the public bundle.
- **Bindings:** Channel-to-agent binding details are not exported in the public bundle.
- **Published instruction sections:** `What arrives`, `Step 1: Decide if it's interesting`, `Step 2: Check presence`, `Step 3: Pull all outdoor + garage cameras`, `Camera entity → name mapping`, `Step 4: Send to Discord`, `Tool allowlist`

## Channels

| Channel | Enabled | DM Policy | Group Policy | Streaming |
|---------|---------|-----------|--------------|-----------|
| `discord` | Yes | pairing | allowlist | off |
| `telegram` | No | pairing | allowlist | off |

## Session Settings

| Setting | Value |
|---------|-------|
| Scope | `per-channel-peer` |
| Reset mode | `idle` |
| Reset hour | `4` |
