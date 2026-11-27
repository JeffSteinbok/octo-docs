---
layout: default
title: Approval Gate
nav_order: 1
nav_exclude: true
---

# ✅ Approval Gate

Logs a decision-model approve, deny or unrelated check when root, main or coding upgrades OpenClaw or adds ilc:plan-approved. Log-only: never blocks or approves anything.

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>agents</code></td><td>string[]</td><td>Optional</td><td>Agents whose approval-gated actions are judged. Defaults to [&quot;root&quot;, &quot;main&quot;, &quot;coding&quot;].</td></tr>
    <tr><td><code>decisionAgent</code></td><td>string</td><td>Optional</td><td>Agent whose decisionModel answers (coding has none). Defaults to &quot;root&quot;.</td></tr>
    <tr><td><code>logFile</code></td><td>string</td><td>Optional</td><td>JSONL decision log. Defaults to ~/.openclaw/logs/approval-gate.jsonl.</td></tr>
  </tbody>
</table>

## Example config

```json
"approval-gate": { "enabled": true, "hooks": { "allowConversationAccess": true }, "config": {} }
```

`hooks.allowConversationAccess` is required for `before_agent_reply` and `agent_end`. `root` has `decisionModel: typesafe/jev-latest`.
