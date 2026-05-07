---
layout: default
title: Octo Satellite
parent: Plugins
nav_order: 9
nav_exclude: true
---

# 🛰️ Octo Satellite

OpenClaw toolset providing structured access to the [Octo Satellite](https://github.com/JeffSteinbok/octo-satellite) service. Exposes Amazon order management and Monarch Money financial tools.

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>token</code></td><td>string</td><td>Optional</td><td>Satellite API &lt;redacted-bearer-token&gt;.</td></tr>
    <tr><td><code>baseUrl</code></td><td>string</td><td>Optional</td><td>Satellite base URL (default: http://localhost:9000).</td></tr>
  </tbody>
</table>

## Example config

| Key | Description | Default |
|-----|-------------|---------|
| `token` | Satellite API <redacted-bearer-token> | `$OCTO_SATELLITE_TOKEN` env var |
| `baseUrl` | Satellite proxy URL | `http://localhost:9000` |
