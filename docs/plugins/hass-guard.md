---
layout: default
title: Hass Guard
nav_order: 3
nav_exclude: true
---

# 🛡️ Hass Guard

Limits the agents behind Hassonic and the Octo MCP (`hassonic` and `external`) to an allowlist of Home Assistant actions, and blocks any action their decision model doesn't rate safe.

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>agents</code></td><td>string[]</td><td>Optional</td><td>Agent IDs to guard. Defaults to [&quot;hassonic&quot;].</td></tr>
    <tr><td><code>alertTarget</code></td><td>string</td><td>Optional</td><td>Where to post blocked calls, as &lt;channel&gt;:&lt;target&gt;, e.g. &quot;discord:channel:&lt;id&gt;&quot;. Unset means no alerts.</td></tr>
  </tbody>
</table>

## Example config

```json
"plugins": { "entries": { "hass-guard": { "enabled": true, "config": { "agents": ["hassonic", "external"], "alertTarget": "discord:channel:<id>" } } } }
```

`agents` lists the agent IDs to guard. `alertTarget` is `<channel>:<target>` as `openclaw message send` takes them; leave it out for no alerts. If `agents` is missing or empty, only `hassonic` is guarded. The safety check uses each guarded agent's own `decisionModel`.
