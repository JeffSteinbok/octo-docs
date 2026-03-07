---
output: agents-channels.md
title: Agents & Channels
nav_order: 2
data_source: agents_channels
overrides:
  main: "Primary personal assistant — full access to all plugins and tools"
  family-agent: "Family group chat agent with limited permissions"
  group-agent: "Generic group chat agent — responds only when mentioned"
  mail: "Email processing agent with read-only access"
  root: "Privileged agent with exec/process access — invoked explicitly by main"
---

<!-- instructions:
  List out all the agents in use and channels. Be descriptive about their
  configuration but redact any personal information or identifiers like
  URIs, IDs, Accounts, etc.

  Agents table: show emoji (from identity config), agent name, role
  description, and active/inactive status. An agent is "active" if it
  has at least one binding in the config.

  Channels table: show platform name and enabled/disabled status.
-->

## Agents

Agents are LLM-powered personas, each with their own identity, permissions,
and context. They decide which plugins to invoke based on user requests.

{{ agents }}

## Channels

Channels are the messaging platforms through which users interact with agents.

{{ channels }}
