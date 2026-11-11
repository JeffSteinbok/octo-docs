---
layout: default
title: Mail Notify Gate
nav_order: 6
nav_exclude: true
---

# Mail Notify Gate

Decides whether an email handed off by a mail rule is worth texting Jeff about, before the main agent runs.

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>agents</code></td><td>string[]</td><td>Optional</td><td>Agents whose mail handoffs are gated. Defaults to [&quot;main&quot;].</td></tr>
    <tr><td><code>mode</code></td><td>string</td><td>Optional</td><td>log (default): record decisions only. enforce: skip the mail run when the email isn&#x27;t worth a text. Allowed: `log`, `enforce`.</td></tr>
    <tr><td><code>threshold</code></td><td>number</td><td>Optional</td><td>P(notify) at or above this counts as notify. Default 0.5.</td></tr>
    <tr><td><code>logFile</code></td><td>string</td><td>Optional</td><td>JSONL decision log. Defaults to ~/.openclaw/logs/mail-notify-gate.jsonl.</td></tr>
  </tbody>
</table>

## Example config

```json
"mail-notify-gate": { "enabled": true, "hooks": { "allowConversationAccess": true }, "config": { "mode": "log" } }
```

`hooks.allowConversationAccess` is required for `before_agent_reply` and `agent_end`. The gated agent needs a `decisionModel` (`main` has `typesafe/jev-latest`).
