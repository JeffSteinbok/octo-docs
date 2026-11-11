---
layout: default
title: Heartbeat Gate
nav_order: 5
nav_exclude: true
---

# Heartbeat Gate

Decides whether a heartbeat has anything urgent enough to message Jeff about, from hard facts rather than a full LLM turn.

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>agents</code></td><td>string[]</td><td>Optional</td><td>Agents whose heartbeat turns are gated. Defaults to [&quot;main&quot;].</td></tr>
    <tr><td><code>mode</code></td><td>string</td><td>Optional</td><td>log (default): record decisions only. enforce: skip the heartbeat turn when nothing is urgent. Allowed: `log`, `enforce`.</td></tr>
    <tr><td><code>threshold</code></td><td>number</td><td>Optional</td><td>In enforce mode, skip the turn when P(urgent) is below this. Default 0.3.</td></tr>
    <tr><td><code>logFile</code></td><td>string</td><td>Optional</td><td>JSONL decision log. Defaults to ~/.openclaw/logs/heartbeat-gate.jsonl.</td></tr>
    <tr><td><code>calendarDir</code></td><td>string</td><td>Optional</td><td>Folder with main&#x27;s calendar files (calendar-work.md, calendar-jeff.md, calendar-tripit.md). Defaults to ~/.openclaw/agents/main/workspace/memory.</td></tr>
    <tr><td><code>pluginHealthFile</code></td><td>string</td><td>Optional</td><td>Latest plugin health check result. Defaults to ~/.openclaw/state/plugin-health.json.</td></tr>
  </tbody>
</table>

## Example config

```json
"heartbeat-gate": { "enabled": true, "hooks": { "allowConversationAccess": true }, "config": { "mode": "log", "threshold": 0.3 } }
```

`hooks.allowConversationAccess` is required for `before_agent_reply` and `agent_end`. The gated agent (`main`) needs a `decisionModel`. `calendarDir` (default `~/.openclaw/agents/main/workspace/memory`) and `pluginHealthFile` (default `~/.openclaw/state/plugin-health.json`) override where the facts are read from.
