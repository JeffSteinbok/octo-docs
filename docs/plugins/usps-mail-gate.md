---
layout: default
title: USPS Mail Gate
nav_order: 9
nav_exclude: true
---

# USPS Mail Gate

Logs a decision-model importance and recipient for each mailpiece in the USPS Informed Delivery digest, next to what usps-mail's rules decided. Log-only.

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>agents</code></td><td>string[]</td><td>Optional</td><td>Agents whose USPS handoffs are judged. Defaults to [&quot;main&quot;].</td></tr>
    <tr><td><code>threshold</code></td><td>number</td><td>Optional</td><td>P(urgent) + P(high) at or above this counts as &#x27;text the recipient&#x27;. Default 0.5.</td></tr>
    <tr><td><code>uspsConfigFile</code></td><td>string</td><td>Optional</td><td>usps-mail&#x27;s config.json (routing, former_residents, home_street). Defaults to ~/.openclaw/agents/mail/workspace/usps-mail/config.json.</td></tr>
    <tr><td><code>logFile</code></td><td>string</td><td>Optional</td><td>JSONL decision log. Defaults to ~/.openclaw/logs/usps-mail-gate.jsonl.</td></tr>
  </tbody>
</table>

## Example config

```json
"usps-mail-gate": { "enabled": true, "hooks": { "allowConversationAccess": true }, "config": {} }
```

`hooks.allowConversationAccess` is required for `before_agent_reply`. The gated agent needs a `decisionModel` (`main` has `typesafe/jev-latest`).
