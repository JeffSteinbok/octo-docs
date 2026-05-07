---
layout: default
title: Skills
nav_order: 4
---

# Skills

Skills are markdown-defined guidance modules that agents load for domain-specific rules, workflows, and operating context.

Unlike plugins, skills do not execute code. They give agents shared instructions for how to use tools and interpret a problem domain.

Octo currently publishes **1 skill** in the public bundle.

| | Skill | Used by | Description |
|---|-------|---------|-------------|
| 🧠 | [Ha Smb](skills/ha-smb) | `coding` | Access, read, and write files on the Home Assistant server via SMB. Use when you need to read or modify HA config files (automations.yaml, scripts.yaml, blueprints, configuration.yaml, etc.) directly on the HA server. Credentials are stored in the workspace .env file. |

## How Skills Differ from Plugins

- **Skills** are bundled markdown knowledge for agents to read and follow.
- **Plugins** are executable integrations that expose callable tools and APIs.
- Skills can reference plugins, but they do not execute on their own.
