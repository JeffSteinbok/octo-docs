---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents & Channels

This page explains each published agent's permission profile and why it is isolated that way.

The public bundle includes agent identity and a simplified permission/config posture. Exact peer bindings, raw filesystem paths, and detailed private allowlists are still omitted.

## Models

- **Primary model:** `github-copilot/claude-sonnet-4.6`
- **Fallback models:** `github-copilot/gpt-5.4`
- **Primary image model:** `github-copilot/claude-sonnet-4.6`

## Agent Architecture

Each published agent has its own permission boundary. Interactive helpers stay separated from delegated workers and webhook-driven automations.

| Agent | Used for | Permissions | Why it is set up this way |
|-------|----------|-------------|---------------------------|
| `main` | Jeff's primary direct chats and proactive assistant flows | `customized` tools; exec `allowed`; browser `default`; writes `default`; sub-agents `root`, `family`, `finance`. | Keeps the everyday assistant capable with exec restricted to safebin CLIs only — no arbitrary shell access. |
| `mail` | Internal delegated mail-processing workflows | `profile:minimal` tools; read `allowed`; writes `denied`; browser `denied`; exec `denied`. | Treats mail as untrusted input and isolates mail processing from broader tools. |
| `root` | Explicit owner escalations for admin/debugging work | `inherited-default` tools; broad inherited access posture; exec `default`. | Concentrates privileged admin/debug access in a separate escalation path. |
| `family` | Family-facing direct chats | `profile:messaging` tools; writes `denied`; browser `denied`; exec `denied`; sub-agents none. | Limits family-facing conversations to a narrow, safer tool surface. |
| `finance` | Published agent surface | `profile:minimal` tools. | Separates this agent from the rest of the system. |
| `hass-hooks` | Home Assistant webhook events | `custom-allowlist` tools; tightly scoped allowlist for camera, image, and message handling only. | Ensures webhook automation can inspect camera events and notify, but not wander outside that workflow. |
| `coding` | Coding specialist in #coding on Discord | `inherited-default` tools. | Dedicated coding agent for code review, architecture, ACP agent delegation, and infra/DevOps work. Kept separate from main to allow elevated shell access without exposing it to everyday chat. |
| `notify` | Published agent surface | `custom-allowlist` tools. | Separates this agent from the rest of the system. |

### Exec & Safebin

Exec permissions are configured **per agent** using `agents.list[].tools.exec`:

- **`main`** — `security: allowlist` — can only run binaries listed in `safeBins` (vetted CLI scripts in `~/safebin/`)
- **`root`** — `security: full` — unrestricted shell access for admin/debug escalation
- **Other agents** — exec denied entirely

See [CLI Tools](clis) for the available safebin inventory.

## Channels

| Channel | Enabled | DM Policy | Group Policy | Streaming |
|---------|---------|-----------|--------------|-----------|
| `discord` | Yes | pairing | allowlist | partial |
| `telegram` | Yes | pairing | allowlist | off |

## Session Settings

| Setting | Value |
|---------|-------|
| Scope | `per-channel-peer` |
| Reset mode | `idle` |
| Reset hour | `4` |
