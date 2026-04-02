---
layout: default
title: Agents & Channels
nav_order: 2
---

# Agents & Channels

OpenClaw uses multiple agents with distinct roles and security boundaries, connected to users via communication channels.

## Agents

| Agent | Emoji | Role | Exec |
|-------|-------|------|------|
| **Octo** (main) | 🐙 | Primary assistant — handles most tasks | ❌ Denied |
| **mail-agent** | 📬 | Email processing — minimal profile, read-only | ❌ Denied |
| **Root** | 🔑 | Privileged agent with full system access | ✅ Enabled |
| **Family** | 👨‍👩‍👧‍👦 | Family agent (placeholder) | ❌ Denied |

### 🐙 Octo (main)

The primary agent responsible for handling most user interactions. **Exec, process, and gateway access are denied** — Octo operates through plugins and tools only. When system-level operations are needed, Octo delegates to the Root agent.

### 📬 mail-agent

Handles email processing with a minimal, read-only profile. Used for automated email notification tasks.

### 🔑 Root

A high-privilege agent with full access to system tools and exec capabilities. Root is never directly exposed to users — it is invoked explicitly by the main agent when elevated permissions are required.

### 👨‍👩‍👧‍👦 Family

A specialized agent for family-related interactions (currently a placeholder).

## Channels

| Channel Type | Enabled | DM Policy | Group Policy | Streaming | Bound Agents |
|--------------|---------|-----------|--------------|-----------|--------------|
| Discord      | Yes     | Pairing   | Allowlist    | Off       | Octo, Root, Family |
| Telegram     | Yes     | Pairing   | Open         | Off       | Octo, Root, Family |

### Channel Details

- **Discord**: Supports direct messages with a pairing policy and group interactions restricted to an allowlist.
- **Telegram**: Allows direct messages with a pairing policy and open group interactions.

## Sessions

Sessions are scoped **per-channel-peer** and reset daily at 4:00 AM UTC.
