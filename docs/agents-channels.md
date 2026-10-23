---
layout: default
title: Agents & Channels
nav_order: 2
has_children: true
---

# Agents & Channels

This page explains each published agent's permission profile and why it is isolated that way.

The public bundle includes agent identity and a simplified permission/config posture. Exact peer bindings, raw filesystem paths, and detailed private allowlists are still omitted.

For AI model and voice configuration, see the [Models](models) page. Apps that connect to the gateway as paired devices, such as Hassonic and OctoDot, are covered under [Connected Apps](connected-apps).

## Agent Architecture

Each published agent has its own permission boundary. Interactive helpers stay separated from delegated workers and webhook-driven automations.

| Agent | Used for | Permissions | Why it is set up this way |
|-------|----------|-------------|---------------------------|
| `main` | Jeff's primary direct chats and proactive assistant flows | `customized` tools; exec `allowed`; browser `default`; writes `default`; sub-agents `root`, `family`, `finance`. | Keeps the everyday assistant capable with exec restricted to safebin CLIs only — no arbitrary shell access. |
| `mail` | Internal delegated mail-processing workflows | `profile:minimal` tools; read `allowed`; writes `denied`; browser `denied`; exec `denied`. | Treats mail as untrusted input and isolates mail processing from broader tools. |
| `root` | Explicit owner escalations for admin/debugging work | `customized` tools; broad inherited access posture; exec `default`. | Concentrates privileged admin/debug access in a separate escalation path. |
| `family` | Family members' iMessage DMs and the family group chat | `profile:messaging` tools; writes `denied`; browser `denied`; exec `allowed`; sub-agents none. | Limits family-facing conversations to a narrow, safer tool surface. Calendar plugins enforce per-person read/write rules from the sender's handle. |
| `finance` | Household finance and retirement planning | `profile:minimal` tools. | Keeps account data and planning notes away from everyday chat, with read-only finance tools. |
| `hass-hooks` | Home Assistant webhook events | `custom-allowlist` tools; tightly scoped allowlist for camera, image, and message handling only. | Ensures webhook automation can inspect camera events and notify, but not wander outside that workflow. |
| `coding` | Coding specialist in #coding on Discord | `inherited-default` tools. | Dedicated coding agent for code review, architecture, ACP agent delegation, and infra/DevOps work. Kept separate from main to allow elevated shell access without exposing it to everyday chat. |
| `notify` | Relays LAN notification hooks to Jeff as Discord DMs | `custom-allowlist` tools; can only send messages. | Hook payloads are untrusted, so the agent that receives them can do nothing but forward them. |
| `claude` | One-shot Claude Code runs delegated over ACP | `inherited-default` tools. | Runs Claude Code as an external ACP agent so coding work happens outside the gateway's own tool policy. |
| `hassonic` | Home control from the [Hassonic](hassonic) iPhone app | `custom-allowlist` tools; Home Assistant state and an allowlisted set of actions, plus web search. | The app talks only to this agent, so a phone request can reach Home Assistant but nothing else. Every action is checked by the hass-guard plugin. |
| `group` | Other iMessage group chats (replies only when mentioned) | `profile:messaging` tools. | Group chats can include people outside the family, so this agent gets only messaging, web search and read access to the family calendar — no exec, files or browser. |

### Exec & Safebin

Exec permissions are configured **per agent** using `agents.entries.<id>.tools.exec`:

- **`main`** — `security: allowlist` — can only run binaries listed in `safeBins` (vetted CLI scripts in `~/safebin/`)
- **`root`** — `security: full` — unrestricted shell access for admin/debug escalation
- **Other agents** — exec denied entirely

See [CLI Tools](clis) for the available safebin inventory.

## Channels

| Channel | Enabled | DM Policy | Group Policy | Streaming |
|---------|---------|-----------|--------------|-----------|
| `discord` | Yes | pairing | allowlist | partial |
| `imessage` | Yes | allowlist | allowlist |  |
| `telegram` | Yes | pairing | allowlist | off |

## Session Settings

| Setting | Value |
|---------|-------|
| Scope | `per-channel-peer` |
| Reset mode | `idle` |
| Reset hour | `4` |
