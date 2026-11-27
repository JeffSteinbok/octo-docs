---
layout: default
title: MCP Bridge
parent: Services
nav_order: 4
---

# MCP Bridge

> **Source:** [openclaw-hub/services/mcp-bridge](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/mcp-bridge)

The OAuth-protected MCP server behind the Octo MCP, which lets other agents, such as OctoDot in ChatGPT, use Octo through a few tools defined in `config/mcp-bridge/tools.json`. Every request needs a WorkOS AuthKit access token for the owner's account, checked before the request body is read. On the Mac mini it runs from the LaunchAgent `com.octo.openclaw.mcp-bridge` (backed up in `config/macos/launchd/`).

## Features

- Streamable HTTP MCP, stateless, at `https://<funnel-host>/mcp`
- OAuth 2.1 resource server: protected resource metadata (RFC 9728), and AuthKit's authorization server metadata proxied for clients that look for it on this origin
- Access tokens checked for JWKS signature, issuer, audience (the MCP URL), expiry, and a one-person allowlist
- Fails closed: refuses to start without an issuer, resource URL and valid tool definitions; never serves `/mcp` unauthenticated
- Tools defined in config, split by risk: direct, condensed reads (`house_status`, `calendar`); `control_house` (changes the house, confirmed in ChatGPT); `send_message` (iMessage or Discord to named destinations, confirmed in ChatGPT); `set_reminder` (one-shot message to Jeff); `ping`
- MCP server instructions tell the client what Octo can and can't do
- Paired with the OpenClaw Gateway as its own device (`operator.read` + `operator.write`, no admin); the shared Gateway token is used once to pair and never stored
- Host header allowlist, POST only, 1 MiB body limit

## Tools

From `config/mcp-bridge/tools.json`. Reads call OpenClaw tools directly under the deliberately limited `external` agent and come back condensed; house changes go to that agent and through Hass Guard; messages go straight out through the Gateway to named destinations.

| Tool | Kind | Action | What happens |
|---|---|---|---|
| `house_status` | read-only | `invoke` | `hass_state_list` for lights, covers, climate and media players, condensed (`home-assistant-status`); network-gear status lights are ignored |
| `calendar` | read-only | `invoke` + `dateRange` | `ics_calendar_fetch` (Personal, Family, TripIt) and `outlook_work_calendar_fetch`, merged and sorted (`calendar-events`) in Pacific time |
| `control_house` | changes things | `ask` | The request, quoted as data, to the `external` agent; Hass Guard checks every action |
| `send_message` | sends things | `send` | Direct Gateway `send` to a named destination from the private destinations file; no AI involved |
| `set_reminder` | schedules a message | `reminder` | One-time text to Jeff, defaulting to iMessage |
| `ping` | read-only | built in | Reachability |

Bridge 0.3.3 persists pending reminders in the private paired-device directory
and resumes them after restart. It delivers through the existing Gateway device
with its current scopes. An unconfirmed delivery is logged and the private
`.sending` record is retained for inspection. The bridge skips automatic replay
of an unconfirmed send to avoid duplicate reminders.

Grant changes in `tools.json` can be reloaded on bridge 0.3.2 and later. See the
Octo MCP page for reload instructions. Tool definition changes
require a restart and may also require a change to the `external` agent's tool list.

## Funnel routes

ChatGPT doesn't connect to non-443 ports, so these paths on the shared 443 hostname go through separate Unix listeners under `~/.openclaw/mcp-proxy`. Tailscale strips each mount prefix, so each listener restores only its own prefix. The LaunchAgent configures the socket directory, which the bridge creates with owner-only permissions and rejects macOS ACLs on that directory. The local TCP listener on port 18793 serves local requests and never attributes forwarded addresses.

| Path | Purpose |
|---|---|
| `/mcp` | MCP endpoint |
| `/.well-known/oauth-protected-resource` (and `…/mcp`) | Protected resource metadata |
| `/.well-known/oauth-authorization-server` | AuthKit metadata, proxied |

A complete Funnel restore requires the bridge to be running with all three sockets ready. From the
Octo checkout, run `sudo bash config/tailscale/restore-funnel.sh "$HOME/.openclaw/mcp-proxy"` under
the live-change lock. The calling shell expands the bridge account’s path before `sudo`. The script
checks the directory and sockets before resetting Funnel. Install or change individual Unix targets
as root with `sudo tailscale funnel --bg --set-path <mount> unix:<absolute-socket-path>`.

## Environment Variables

The LaunchAgent sets `MCP_BRIDGE_TOOLS`; the service reads the rest from a private env file, `~/.openclaw/secrets/mcp-bridge/mcp-bridge.env`:

| Variable | Required | Description |
|---|---|---|
| `MCP_BRIDGE_TOOLS` | yes | Tool definitions file (`~/git/octo/config/mcp-bridge/tools.json`) |
| `MCP_BRIDGE_RESOURCE` | yes | Public MCP URL (`https://<funnel-host>/mcp`); must equal the WorkOS resource indicator |
| `MCP_BRIDGE_ISSUER` | yes | AuthKit domain, exactly as in tokens' `iss` |
| `MCP_BRIDGE_ALLOWED_SUBJECTS` | no | WorkOS user IDs allowed in; empty means nobody gets in |

Defaults cover the rest (device directory `~/.openclaw/secrets/mcp-bridge`, Gateway WebSocket on IPv4 loopback, port 18789, port 18793); the [mcp-bridge README](https://github.com/JeffSteinbok/openclaw-hub/tree/main/services/mcp-bridge) lists every setting. The device directory (mode 700/600, never in a repo) holds the device identity and token and `destinations.json`, the message destinations' handles and channel IDs.

## Install

```bash
cd ~/git/openclaw-hub/services/mcp-bridge
npm ci && npm run build && npm test
cp ~/git/octo/config/macos/launchd/com.octo.openclaw.mcp-bridge.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.octo.openclaw.mcp-bridge.plist
```

Pair with the Gateway once (the shared token is used for this command only):

```bash
OPENCLAW_GATEWAY_TOKEN=… node dist/pair.js
openclaw devices list    # role operator, scopes operator.read + operator.write
```

The Funnel routes are added by `config/tailscale/apply-step-441.sh`, which the owner runs by hand because it needs the Tailscale operator account (see [Changing Funnel](../external-integrations#changing-funnel)).

The current tool definitions require bridge 0.3.3 or later. Install and verify
the bridge against the previous config with the `mcp-bridge-reminder-build`
health check step before pushing the reminder config to main. Then apply the
config and restart under `mcp-bridge-reminders`.

```bash
launchctl kickstart -k gui/$(id -u)/com.octo.openclaw.mcp-bridge
```

## Logs

```bash
tail -f ~/Library/Logs/openclaw-mcp-bridge.log
```

At startup the log lists the tools and destination names it loaded. Request lines include the path and the verified OAuth `client_id`, with `client=-` when the ID is unavailable.
Successful OAuth authentication on the private Unix listeners records a validated Tailscale-forwarded client IP and labels it Funnel or tailnet. TCP calls and calls without validated forwarding metadata have an unknown origin. The socket boundary trusts the bridge account and the privileged local Tailscale daemon. The log omits <redacted-bearer-token>,
Tailscale user identities, and raw user-agent strings. Signed-in calls and authentication or tool rejections use a bounded user-agent family for watcher summaries. Keep these logs private. Refusals log the reason.
Find user IDs for the allowlist in the WorkOS dashboard. Each `send_message` logs only the destination name.
