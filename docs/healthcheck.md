---
layout: default
title: Health Check
parent: Engineering Harness
nav_order: 2
---

# 🩺 Health Check

`scripts/healthcheck.py` is a regression check for changes to the running system. Large changes to Octo are made as a series of small, named **steps**; the health check snapshots the system before a step, probes it again afterwards, and reports everything that changed without being declared. A step that breaks something is caught before the next one lands, while it is still easy to undo. It is part of the [Engineering Harness](harness).

```bash
scripts/healthcheck.py baseline --step <step>     # before the change

## ... make the change ...
scripts/healthcheck.py verify --step <step>       # after: GO or NO-GO
scripts/healthcheck.py wait-ready --step <step>   # after any Gateway restart
scripts/healthcheck.py probes                     # list the probes
```

`verify` exits 0 for GO, 1 for NO-GO, and 2 if the tool itself fails. Add `--strict` to treat warnings as NO-GO.

## What it checks

28 probes, all read-only except the remote-access smoke test, which sends requests that are expected to be rejected:

| Area | Checks |
|---|---|
| Gateway | `/healthz`, `/startupz`, `/readyz` (agent databases, channels, plugin reload, event loop), `openclaw health`, CLI and Gateway versions match, stability bundles and memory pressure, listening ports |
| Channels | Each enabled channel configured, running, connected and ready; the iMessage bridge process |
| Hooks | `main` can never be run by a hook; the [remote-access smoke test](external-integrations#verifying-changes); webhook-proxy and GitHub hook logs |
| Plugins | Enabled plugins loaded; degraded plugins or secret owners |
| Agents | Agent list and models, database files present and sane, session counts (if an agent database is refused, its session count drops to zero) |
| Cron | Scheduler on; job errors, especially agent-database admission failures; overdue jobs; failed runs since the baseline |
| Services | LaunchAgents running, plist hashes, program arguments, env key names; the Glances API; the OneDrive app (vault sync); service log errors since the baseline |
| Config | `openclaw.json` hash and a redacted copy; env files as key names and value lengths only; service configs |
| Tailscale Funnel | Tailnet up; Funnel routes, and drift from the committed `config/tailscale/funnel.json` |
| Devices | Paired devices, admin count, pending requests, nodes |
| Logs | New Gateway log lines since the baseline, matched against known failure signatures |

## Before and after

`baseline` records an inventory of the system. `verify` takes a new one and sorts every difference into a class:

| Class | Meaning | Result |
|---|---|---|
| telemetry | Values that move on their own: timestamps, process IDs, database sizes, log offsets, service runtime state | ignored |
| expected | Declared in the step's expected-changes file | pass |
| counter | A counter that should never go up went up: cron errors, service restarts, failed deliveries, admin devices | FAIL |
| soft | A change worth a warning, such as a laptop node going to sleep | WARN |
| undeclared | Anything else that changed, appeared or disappeared | FAIL |

Each step declares what it is supposed to change in `config/healthcheck/steps/<step>.json`, including whether a Gateway or service restart is expected. Known findings that predate the step live in `config/healthcheck/accepted.json`.

## WhatsApp owner approvals

Use the `owner-allow-whatsapp` step when adding Jeff’s channel-scoped WhatsApp
sender to `commands.ownerAllowFrom`. Match the sender in the direct WhatsApp
binding to `main` against `channels.whatsapp.allowFrom` and preserve existing
owner entries. The channel allowlist controls who can send messages.
`commands.ownerAllowFrom` grants owner authority for approvals.

Run `baseline` before editing and `verify` afterward. The only expected
configuration projection change is `commands.ownerAllowFrom`. OpenClaw applies
command changes through Gateway hot reload. After verification, confirm that an
approval from Jeff’s WhatsApp sender (DM or an allowlisted group) is recognized as an owner approval.

## Main file reads

Use the `main-fs-guard` step to deploy the Main Filesystem Guard. Take a baseline before installation. Plugin installation triggers a Gateway hot reload, so use `scripts/healthcheck.py wait-ready --step main-fs-guard --timeout 180 --no-verify` before running full verification. Check the declared workspace, outside and denied reads. Use `~/.openclaw/logs/main-fs-guard.jsonl` to identify which read-only roots `main` still uses before moving to `tools.fs.workspaceOnly`.

## After a restart

`wait-ready` polls `/healthz`, then `/startupz`, then `/readyz`, for up to 8 minutes by default (`--timeout` changes this), because an agent database can take minutes to be admitted after a restart. If an agent database is refused, it stops waiting and prints the recovery steps: stop the Gateway (`openclaw gateway stop --force`), back up `~/.openclaw/agents/<id>/agent`, run `openclaw doctor --fix --yes`, then `wait-ready` again. Once the Gateway is ready, it runs the Gateway, channel, agent, cron, LaunchAgent and log checks.

## Reports and secrets

Reports go to `~/.openclaw/healthcheck/steps/<step>/`, readable only by the owner (mode 600). The connection watcher uses the timing and lock information in these reports and private active-run markers to identify alerts that overlap a deployment. They never contain secret values: env files are recorded as key names and value lengths, config secrets are redacted, and log samples pass through a redactor.

## Why it exists

On 2026-10-24 a routine Gateway restart left the main agent's database refused. For about 80 minutes iMessage showed typing indicators but Octo never replied. `/readyz`, the Gateway log and the cron state all showed the failure, but nothing was reading them. Replaying that day's log against a baseline makes `verify` fail on exactly those signals.


## Channel outage alerts

The five-minute `readiness-check` cron reads `/readyz` and the Gateway’s default
account status for WhatsApp, iMessage, Telegram, and Discord. It keeps reporting
other readiness failures through the cron’s Discord delivery. For a channel
that stays down for 20 minutes, the script sends Jeff one alert via the first
working route in this order, iMessage, Discord DM, Telegram, WhatsApp. It also
posts to #octo-status when Discord is healthy. A logout alert includes the
relink command. A timestamped logout can qualify on the first run.

The cron batches alerts by recipient, sends a reminder after 24 hours, and
sends a recovery note after 30 minutes of consecutive healthy observations.
A failed or missing observation resets that recovery timer. New down notices
for the same channel and audience are at least six hours apart. Healthy
observations before the initial alert reset the 20-minute outage timer.

The cron keeps delivery state and the latest send errors in
`~/.openclaw/state/readiness-check.json`. It retries failed sends after an
hour and counts timed-out sends as delivered because the transport may have
accepted them. Losing the state file can cause a duplicate alert per audience.
The heartbeat gate reads the same file for channel-health context. The readiness
cron owns alert delivery.

Use `python3 scripts/readiness_check.py --dry-run` to read live status and see
which sends are due without sending messages or updating state.
