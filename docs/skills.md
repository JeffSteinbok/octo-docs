---
layout: default
title: Skills
nav_order: 5
---

# Skills

Skills are markdown-defined guidance modules that agents load for domain-specific rules, workflows, and operating context.

Unlike plugins, skills do not execute code. They give agents shared instructions for how to use tools and interpret a problem domain.

Octo currently publishes **3 skills** in the public bundle.

Skills are grouped by whether their source is open source or private to Octo. Host-specific commands are omitted from the individual pages — they run on the Octo host and reference private paths.

## 📦 Open Source

Skills whose source lives in a public OpenClaw repo — reusable across installs.

| | Skill | Used by | Description | Source |
|---|-------|---------|-------------|--------|
| 📊 | [Usage Report](skills/usage-report) | `root` | Generate the weekly LLM API usage and cost report, render to PDF, post to Discord, and commit. | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/skills/usage-report) |

## 🔒 Private (octo)

Octo-specific skills. Source is private, but the docs are published below.

| | Skill | Used by | Description | Source |
|---|-------|---------|-------------|--------|
| 🔍 | [Agent Review](skills/agent-review) | `root` | Weekly self-improvement analysis — scan session transcripts, tool failures, cron errors, and memory for patterns; file GitHub issues for recurring findings; deliver prioritized suggestions to Jeff via Discord DM. | Private |
| 🏠 | [HA SMB](skills/ha-smb) | `coding` | Access, read, and write files on the Home Assistant server via SMB. Use when you need to read or modify HA config files (automations.yaml, scripts.yaml, blueprints, configuration.yaml, etc.) directly on the HA server. Credentials are stored in the workspace .env file. | Private |


## How Skills Differ from Plugins

- **Skills** are bundled markdown knowledge for agents to read and follow.
- **Plugins** are executable integrations that expose callable tools and APIs.
- Skills can reference plugins, but they do not execute on their own.
