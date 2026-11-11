---
layout: default
title: Hass Alert Gate
nav_order: 3
nav_exclude: true
---

# Hass Alert Gate

Decides whether a Home Assistant camera event is worth telling Jeff about before the hass-hooks agent runs. Skips the full agent turn for events that would end in NO_REPLY.

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>agents</code></td><td>string[]</td><td>Optional</td><td>Agent IDs whose hook runs are gated. Defaults to [&quot;hass-hooks&quot;].</td></tr>
    <tr><td><code>mode</code></td><td>string</td><td>Optional</td><td>log (default): record decisions, change nothing. enforce: skip the agent turn when the event isn&#x27;t worth an alert. Allowed: `log`, `enforce`.</td></tr>
    <tr><td><code>threshold</code></td><td>number</td><td>Optional</td><td>In enforce mode, skip the turn when P(alert) is below this. Default 0.3.</td></tr>
    <tr><td><code>presenceEntities</code></td><td>string[]</td><td>Optional</td><td>Home Assistant person.* entities whose state goes into the decision.</td></tr>
    <tr><td><code>visitors</code></td><td>object[]</td><td>Optional</td><td>Expected regular visitors, e.g. a weekly chef.</td></tr>
    <tr><td><code>visitors[].name</code></td><td>string</td><td>Required</td><td></td></tr>
    <tr><td><code>visitors[].when</code></td><td>string</td><td>Required</td><td></td></tr>
    <tr><td><code>visitors[].note</code></td><td>string</td><td>Optional</td><td></td></tr>
    <tr><td><code>question</code></td><td>object</td><td>Optional</td><td>The question the decision model answers. Any field left out uses the built-in wording (see README).</td></tr>
    <tr><td><code>question.instructions</code></td><td>string</td><td>Optional</td><td>What the model is asked.</td></tr>
    <tr><td><code>question.criteria</code></td><td>object</td><td>Optional</td><td></td></tr>
    <tr><td><code>question.criteria.true</code></td><td>string</td><td>Optional</td><td>When the answer is yes (text the owner).</td></tr>
    <tr><td><code>question.criteria.false</code></td><td>string</td><td>Optional</td><td>When the answer is no.</td></tr>
    <tr><td><code>logFile</code></td><td>string</td><td>Optional</td><td>JSONL decision log. Defaults to ~/.openclaw/logs/hass-alert-gate.jsonl.</td></tr>
  </tbody>
</table>

## Example config

```json
"hass-alert-gate": {
  "enabled": true,
  "hooks": { "allowConversationAccess": true },
  "config": {
    "mode": "log",
    "threshold": 0.3,
    "presenceEntities": ["person.owner", "person.partner"],
    "visitors": [{ "name": "Cleaner", "when": "Tuesdays, around noon", "note": "arrives at the front door with supplies" }]
  }
}
```

`hooks.allowConversationAccess` is required: `before_agent_reply` reads the run's input. Each gated agent needs a `decisionModel` (`agents.entries.hass-hooks.decisionModel`).
