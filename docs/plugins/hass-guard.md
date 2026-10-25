---
layout: default
title: Hass Guard
nav_order: 3
nav_exclude: true
---

# Hass Guard

Limits configured agents (default: hassonic) to an allowlist of Home Assistant actions and safety-checks each one.

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
"plugins": { "entries": { "hass-guard": { "enabled": true, "config": { "agents": ["hassonic"], "alertTarget": "discord:channel:<id>" } } } }
```

`agents` lists the agent IDs to guard. `alertTarget` is `<channel>:<target>` as `openclaw message send` takes them; leave it out for no alerts. If it is missing or empty, only `hassonic` is guarded. The safety check uses each guarded agent's own `decisionModel`.

## CLI Usage

This plugin can also run as a standalone command-line tool via `@openclaw/cli-shared`.

### Setup

```bash
cd plugins/hass-guard
npm install && npm run build
```

### Commands

```bash

## Show help
node dist/bin/hass-guard.js --help

## JSON output
node dist/bin/hass-guard.js <command> [args...] --json
```

### Environment Variables (CLI mode)

| Variable | Description |
|----------|-------------|
| `HASS_GUARD_AGENTS` | Agent IDs to guard. Defaults to ["hassonic"]. |
| `HASS_GUARD_ALERT_TARGET` | Where to post blocked calls, as <channel>:<target>, e.g. "discord:channel:<id>". Unset means no alerts. |
