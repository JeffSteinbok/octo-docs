---
layout: default
title: GitHub
parent: Plugins
nav_order: 3
nav_exclude: true
---

# 🐙 GitHub

Manage GitHub issues. Create, read, update, close, comment on, and list issues.

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>token</code></td><td>string</td><td>Optional</td><td>GitHub personal access token or fine-grained token.</td></tr>
  </tbody>
</table>

## Example config

Set credentials in `plugins.entries["github"].config`:

```json
{
  "plugins": {
    "entries": {
      "github": {
        "enabled": true,
        "config": {
          "token": "ghp_your_personal_access_token"
        }
      }
    }
  }
}
```
