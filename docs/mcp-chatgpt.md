---
layout: default
title: ChatGPT Connector
parent: 'Octo MCP: Octo for other agents'
grand_parent: External Integrations
nav_order: 2
---

# ChatGPT connector

How to add the [Octo MCP](mcp) to ChatGPT as a custom MCP server, so OctoDot (or any ChatGPT chat) can use Octo's
tools. You need the WorkOS side set up first; see [WorkOS setup](mcp-workos).

## Adding the server

1. ChatGPT → Plugins → **+** → **Add custom MCP server**.
2. URL: `https://<funnel-host>/mcp`.
3. Authentication: **OAuth**. Leave client ID and secret blank; ChatGPT registers itself with **CIMD** (preferred) or
   **DCR**.
4. Sign in on the WorkOS page with the invited account.
5. In a chat with OctoDot, select Octo and ask "what's the house status?". It answers without asking you to confirm,
   because `house_status` is read-only.

## Confirmations

ChatGPT asks you to confirm any tool that isn't marked read-only. That's deliberate for `control_house` (it changes
the house) and `send_message` (it reaches people). `house_status`, `calendar` and `ping` are read-only and run without
a prompt. See [why the tools are split this way](mcp#why-this-split).

The first sign-in by a new account is refused (`403`) until its WorkOS user ID is on the bridge's allowlist; see
[WorkOS setup](mcp-workos#allowing-a-user). After adding the ID, reinstall the connector so ChatGPT retries.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "Couldn't discover OAuth settings"; DCR and CIMD shown as **Unavailable** | ChatGPT never reached the server's metadata. We saw this with the server on Funnel port 8443: ChatGPT doesn't connect to it | Serve on port 443 (`https://<funnel-host>/mcp`). Check the bridge log for requests from ChatGPT (`ua=openai-mcp/…` or `aiohttp`) |
| Can't add the server with "No auth" | ChatGPT requires auth here | Use OAuth |
| Dot says the connector's actions "aren't available" | The connector is stuck on an earlier failed sign-in (for example a `403` before the user was allowlisted) | Reinstall the connector, then start a new chat |
| Dot only sees `ping`, or an old tool list | ChatGPT caches the tool list; only `ping` is offered while the bridge isn't paired with the Gateway | Refresh (or reinstall) the connector; the bridge log lists the tools it loaded at startup (`tools: house_status, …`) |
| Every house or calendar question fails | The bridge can't reach the Gateway, or its device was removed | `openclaw devices list` should show the bridge's device; re-pair with `dist/pair.js` (see [mcp-bridge install](services/mcp-bridge#install)) |
| Every call fails with `401` | Token audience or issuer doesn't match (resource indicator changed, or wrong AuthKit domain) | Compare the resource indicator, `MCP_BRIDGE_RESOURCE` and `MCP_BRIDGE_ISSUER` |

The bridge log on the Mac mini shows each request with its user agent and every refusal with its reason:

```bash
tail -f ~/Library/Logs/openclaw-mcp-bridge.log
```
