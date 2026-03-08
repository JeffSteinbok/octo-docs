---
output: agents-channels.md
title: Agents & Channels
nav_order: 2
data_keys:
  - agents
  - channels
---

Generate a documentation page covering OpenClaw **agents** and **channels**.

### Agents

Start with an H2 heading `## Agents` and this intro paragraph:

> Agents are LLM-powered personas, each with their own identity, permissions,
> and context. They decide which plugins to invoke based on user requests.

Then render a markdown table with these columns: **Agent**, **Role**, **Status**.

- **Agent**: the agent's emoji followed by its name
- **Role**: the agent's description (use the override below if one exists for that agent id)
- **Status**: `✅ Active` if `active` is true, otherwise `💤 Inactive`

#### Agent Role Overrides

Use these role descriptions instead of the raw data:

- **main**: Primary personal assistant — full access to all plugins and tools
- **family-agent**: Family group chat agent with limited permissions
- **group-agent**: Generic group chat agent — responds only when mentioned
- **mail**: Email processing agent with read-only access
- **root**: Privileged agent with exec/process access — invoked explicitly by main

### Channels

Then add an H2 heading `## Channels` and this intro paragraph:

> Channels are the messaging platforms through which users interact with agents.

Render a markdown table with columns: **Platform**, **Status**.

- **Platform**: the channel type, title-cased
- **Status**: `✅ Enabled` if enabled, otherwise `❌ Disabled`
