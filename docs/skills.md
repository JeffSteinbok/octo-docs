---
layout: default
title: Skills
nav_order: 5
---

# Skills

Skills are instruction files (`SKILL.md`, written in Markdown) that teach an agent how to do a particular job: which tools to use, in what order, and what rules to follow. An agent loads a skill only when a task calls for it.

Unlike [plugins](plugins), skills don't add tools to an agent; they tell it how to use the tools it already has. Some come with scripts that the agent runs with its shell tool.

Octo publishes **3 skills**, grouped by where the source lives. Each skill's page is the skill file itself, written as instructions to the agent. Commands that only run on the Octo host are left out.

## 📦 Open Source

Skills whose source is in a public repo, so other OpenClaw installs can use them too.

| | Skill | Used by | Description | Source |
|---|-------|---------|-------------|--------|
| 🔍 | [Agent Review](skills/agent-review) | `root` | Weekly review of session transcripts, tool failures, scheduled-job errors and memory files. Files a GitHub issue for each recurring problem it is confident about and sends a prioritized summary. | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/skills/agent-review) |
| 📊 | [Usage Report](skills/usage-report) | `root` | Weekly report of model API usage and cost, broken down by agent, scheduled job and model. Rendered to PDF and posted to Discord. | [GitHub ↗](https://github.com/JeffSteinbok/openclaw-hub/tree/main/skills/usage-report) |

## 🔒 Private (octo)

Octo-specific skills. The source is private, but each skill's page is published here.

| | Skill | Used by | Description | Source |
|---|-------|---------|-------------|--------|
| 🏠 | [HA SMB](skills/ha-smb) | `coding` | Read and edit Home Assistant's config files (automations, scripts, blueprints) over its SMB file share. | Private |
