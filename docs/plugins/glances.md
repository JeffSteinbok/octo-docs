---
layout: default
title: Glances
parent: Plugins
nav_order: 4
---

# Glances

Read CPU, memory, disk, and summary metrics from a Glances server

> **Source:** [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/glances)

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>url</code></td><td>string</td><td>Optional</td><td>Base URL for the Glances web server, e.g. http://127.0.0.1:61208. Default: `http://127.0.0.1:61208`.</td></tr>
  </tbody>
</table>

## Example config

Set Glances under `plugins.entries["glances"].config`:

```json
{
  "plugins": {
    "entries": {
      "glances": {
        "enabled": true,
        "config": {
          "url": "http://127.0.0.1:61208"
        }
      }
    }
  }
}
```

If omitted, the plugin defaults to `http://127.0.0.1:61208`.
