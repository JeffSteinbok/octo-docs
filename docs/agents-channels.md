---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents & Channels

This page explains each published agent's permission profile and why it is isolated that way.

The public bundle includes agent identity and a simplified permission/config posture. Exact peer bindings, raw filesystem paths, and detailed private allowlists are still omitted.

For AI model and voice configuration, see the [Models](models) page.

## Agent Architecture

Each published agent has its own permission boundary. Interactive helpers stay separated from delegated workers and webhook-driven automations.

| Agent | Used for | Permissions | Why it is set up this way |
|-------|----------|-------------|---------------------------|

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
