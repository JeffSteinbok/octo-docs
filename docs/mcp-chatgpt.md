---
layout: default
title: ChatGPT Connector
parent: MCP & OctoDot
grand_parent: External Integrations
nav_order: 2
---

# ChatGPT connector

## Adding the server

1. ChatGPT → Plugins → **+** → **Add custom MCP server**.
2. URL: `https://<funnel-host>/mcp`.
3. Authentication: **OAuth**. Leave client ID and secret blank; ChatGPT registers itself with **CIMD** (preferred) or
   **DCR**.
4. Sign in on the WorkOS page with the invited account.
5. In a chat with OctoDot, select Octo and ask it to call the `ping` tool. It answers `pong` and the server time.

The first sign-in by a new account is refused (`403`) until its WorkOS user ID is on octo-mcp's allowlist; see
[WorkOS setup](mcp-workos#allowing-a-user). After adding the ID, reinstall the connector so ChatGPT retries.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "Couldn't discover OAuth settings"; DCR and CIMD shown as **Unavailable** | ChatGPT never reached the server's metadata. We saw this with the server on Funnel port 8443: ChatGPT doesn't connect to it | Serve on port 443 (`https://<funnel-host>/mcp`). Check the octo-mcp log for requests from ChatGPT (`ua=openai-mcp/…` or `aiohttp`) |
| Can't add the server with "No auth" | ChatGPT requires auth here | Use OAuth |
| Dot says the connector's actions "aren't available" | The connector is stuck on an earlier failed sign-in (for example a `403` before the user was allowlisted) | Reinstall the connector, then start a new chat |
| Dot can call `ping` but can't answer questions about the house | Only `ping` exists so far | `ask_octo` is planned |
| Every call fails with `401` | Token audience or issuer doesn't match (resource indicator changed, or wrong AuthKit domain) | Compare the resource indicator, `OCTO_MCP_RESOURCE` and `OCTO_MCP_AUTHKIT_ISSUER` |

The octo-mcp log shows each request with its user agent and every refusal with its reason:

```bash
tail -f ~/Library/Logs/openclaw-octo-mcp.log
```
