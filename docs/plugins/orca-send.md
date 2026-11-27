---
layout: default
title: Orca Send
nav_order: 9
nav_exclude: true
---

# 🐋 Orca Send

Lets the main agent send status and questions to an allowlisted Orca bot through a structured tool.

## Configuration Schema

<table class="config-schema-table">
  <thead>
    <tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>agents</code></td><td>string[]</td><td>Optional</td><td>Agents that get the tools. Defaults to [&quot;main&quot;].</td></tr>
    <tr><td><code>allowedRecipients</code></td><td>string[]</td><td>Optional</td><td>Recipients orca_send may message: bot:&lt;name&gt;, bot:&lt;id&gt; or run:run_&lt;id&gt;. Defaults to [&quot;bot:&lt;orca-bot-id&gt;&quot;].</td></tr>
    <tr><td><code>allowedTypes</code></td><td>string[]</td><td>Optional</td><td>Message types orca_send may use. Default [&quot;status&quot;]. question and handoff are opt-in. Orca-Octo answers questions in a dedicated OpenClaw session.</td></tr>
    <tr><td><code>fromHandle</code></td><td>string</td><td>Optional</td><td>Sender label Orca records as from_handle. Defaults to openclaw:main. Must not name a Run, Dispatch, terminal or bot.</td></tr>
    <tr><td><code>orcaBin</code></td><td>string</td><td>Optional</td><td>Absolute path to the orca CLI. Defaults to /Users/octo/Applications/Orca.app/Contents/Resources/bin/orca.</td></tr>
    <tr><td><code>timeoutMs</code></td><td>number</td><td>Optional</td><td>Timeout for each CLI call. Default 30000.</td></tr>
  </tbody>
</table>

## Example config

```json
{
  "plugins": {
    "entries": {
      "orca-send": {
        "enabled": true,
        "config": {
          "allowedRecipients": ["bot:<orca-octo-bot-id>"],
          "allowedTypes": ["status", "question"]
        }
      }
    }
  },
  "agents": {
    "entries": {
      "main": { "tools": { "alsoAllow": ["orca_send"] } }
    }
  }
}
```

## Command-Line Use

Building the plugin also produces a standalone command-line version, with one command per tool. Add `--json` to any command for JSON output.

```bash
cd plugins/orca-send
npm install && npm run build
node dist/bin/orca-send.js --help
```

### Environment Variables (command line)

On the command line, each config field is read from an environment variable instead:

| Variable | Description |
|----------|-------------|
| `ORCA_SEND_AGENTS` | Agents that get the tools. Defaults to ["main"]. |
| `ORCA_SEND_ALLOWED_RECIPIENTS` | Recipients orca_send may message: bot:<name>, bot:<id> or run:run_<id>. Defaults to ["bot:<orca-bot-id>"]. |
| `ORCA_SEND_ALLOWED_TYPES` | Message types orca_send may use. Default ["status"]. question and handoff are opt-in. Orca-Octo answers questions in a dedicated OpenClaw session. |
| `ORCA_SEND_FROM_HANDLE` | Sender label Orca records as from_handle. Defaults to openclaw:main. Must not name a Run, Dispatch, terminal or bot. |
| `ORCA_SEND_ORCA_BIN` | Absolute path to the orca CLI. Defaults to /Users/octo/Applications/Orca.app/Contents/Resources/bin/orca. |
| `ORCA_SEND_TIMEOUT_MS` | Timeout for each CLI call. Default 30000. |
