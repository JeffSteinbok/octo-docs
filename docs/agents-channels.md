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
| `main` | Jeff's primary direct chats and proactive assistant flows | `customized` tools; exec `denied`; browser `default`; writes `default`; sub-agents `root`, `family`, `finance`. | Keeps the everyday assistant capable without giving the default chat direct shell/process control. |
| `mail` | Internal delegated mail-processing workflows | `profile:minimal` tools; read `allowed`; writes `denied`; browser `denied`; exec `denied`. | Treats mail as untrusted input and isolates mail processing from broader tools. |
| `root` | Explicit owner escalations for admin/debugging work | `inherited-default` tools; broad inherited access posture; exec `inherited`. | Concentrates privileged admin/debug access in a separate escalation path. |
| `family` | Family-facing direct chats | `profile:messaging` tools; writes `denied`; browser `denied`; exec `denied`; sub-agents none. | Limits family-facing conversations to a narrow, safer tool surface. |
| `finance` | Published agent surface | `profile:minimal` tools. | Separates this agent from the rest of the system. |
| `hass-hooks` | Home Assistant webhook events | `custom-allowlist` tools; tightly scoped allowlist for camera, image, and message handling only. | Ensures webhook automation can inspect camera events and notify, but not wander outside that workflow. |
| `coding` | Coding specialist in #coding on Discord | Full exec/process/browser access; elevated permissions. | Dedicated coding agent for code review, architecture, ACP agent delegation, and infra/DevOps work. Kept separate from main to allow elevated shell access without exposing it to everyday chat. |

## `main`

- **Used for:** Jeff's primary direct chats and proactive assistant flows
- **Permissions:** `customized` tools; exec `denied`; browser `default`; writes `default`; sub-agents `root`, `family`, `finance`.
- **Why:** Keeps the everyday assistant capable without giving the default chat direct shell/process control.
- **Tool mode:** `customized`
- **Sub-agent access:** `root`, `family`, `finance`
- **Private details still omitted:** exact peer bindings and detailed tool allowlists.

## `mail`

- **Used for:** Internal delegated mail-processing workflows
- **Permissions:** `profile:minimal` tools; read `allowed`; writes `denied`; browser `denied`; exec `denied`.
- **Why:** Treats mail as untrusted input and isolates mail processing from broader tools.
- **Tool mode:** `profile:minimal`
- **Sub-agent access:** None published.
- **Private details still omitted:** exact peer bindings and detailed tool allowlists.

## `root`

- **Used for:** Explicit owner escalations for admin/debugging work
- **Permissions:** `inherited-default` tools; broad inherited access posture; exec `inherited`.
- **Why:** Concentrates privileged admin/debug access in a separate escalation path.
- **Tool mode:** `inherited-default`
- **Sub-agent access:** None published.
- **Private details still omitted:** exact peer bindings and detailed tool allowlists.

## `family`

- **Used for:** Family-facing direct chats
- **Permissions:** `profile:messaging` tools; writes `denied`; browser `denied`; exec `denied`; sub-agents none.
- **Why:** Limits family-facing conversations to a narrow, safer tool surface.
- **Tool mode:** `profile:messaging`
- **Sub-agent access:** None published.
- **Private details still omitted:** exact peer bindings and detailed tool allowlists.

## `finance`

- **Used for:** Published agent surface
- **Permissions:** `profile:minimal` tools.
- **Why:** Separates this agent from the rest of the system.
- **Tool mode:** `profile:minimal`
- **Sub-agent access:** None published.
- **Private details still omitted:** exact peer bindings and detailed tool allowlists.

## `coding`

- **Used for:** Coding specialist — code review, architecture, ACP agent delegation, infra/DevOps. Lives in #coding on Discord.
- **Permissions:** Full exec/process/browser access; elevated permissions enabled.
- **Why:** Dedicated coding agent that can run shell commands and delegate to ACP coding agents (Codex, Claude Code), kept separate from main to isolate elevated access.
- **Tool mode:** Full (elevated)
- **Sub-agent access:** ACP coding agents (Codex, Claude Code).
- **Private details still omitted:** exact peer bindings and detailed tool allowlists.

## `hass-hooks`

- **Used for:** Home Assistant webhook events
- **Permissions:** `custom-allowlist` tools; tightly scoped allowlist for camera, image, and message handling only.
- **Why:** Ensures webhook automation can inspect camera events and notify, but not wander outside that workflow.
- **Tool mode:** `custom-allowlist`
- **Sub-agent access:** None published.
- **Private details still omitted:** exact peer bindings and detailed tool allowlists.

## Channels

| Channel | Enabled | DM Policy | Group Policy | Streaming |
|---------|---------|-----------|--------------|-----------|
| `discord` | Yes | pairing | allowlist | partial |
| `telegram` | No | pairing | allowlist | off |

## Session Settings

| Setting | Value |
|---------|-------|
| Scope | `per-channel-peer` |
| Reset mode | `idle` |
| Reset hour | `4` |
