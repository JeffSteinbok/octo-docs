---
layout: default
title: Family Request Gate
nav_order: 3
nav_exclude: true
---

# 👪 Family Request Gate

Logs a decision-model handle, ask-Jeff or refuse verdict for each request a person sends the family or group agent, next to what the agent did. Log-only.

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>agents</code></td><td>string[]</td><td>Optional</td><td>Agents whose requests are judged. Defaults to [&quot;family&quot;, &quot;group&quot;].</td></tr>
    <tr><td><code>decisionAgent</code></td><td>string</td><td>Optional</td><td>Agent whose decisionModel answers (family and group have none). Defaults to &quot;main&quot;.</td></tr>
    <tr><td><code>owner</code></td><td>string</td><td>Optional</td><td>The owner&#x27;s name in session.identityLinks. Defaults to &quot;jeff&quot;.</td></tr>
    <tr><td><code>logFile</code></td><td>string</td><td>Optional</td><td>JSONL decision log. Defaults to ~/.openclaw/logs/family-request-gate.jsonl.</td></tr>
  </tbody>
</table>

## Example config

```json
"family-request-gate": { "enabled": true, "hooks": { "allowConversationAccess": true }, "config": {} }
```

`hooks.allowConversationAccess` is required for `before_agent_reply` and `agent_end`. `main` has `decisionModel: typesafe/jev-latest`.
