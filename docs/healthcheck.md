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

## After a restart

`wait-ready` polls `/healthz`, then `/startupz`, then `/readyz`, for up to 8 minutes by default (`--timeout` changes this), because an agent database can take minutes to be admitted after a restart. If an agent database is refused, it prints the recovery procedure (`openclaw doctor --fix`) instead of waiting. Once the Gateway is ready, it runs the Gateway, channel, agent and cron checks.

## Reports and secrets

Reports go to `~/.openclaw/healthcheck/steps/<step>/`, readable only by the owner (mode 600). They never contain secret values: env files are recorded as key names and value lengths, config secrets are redacted, and log samples pass through a redactor.

## Why it exists

On 2026-10-24 a routine Gateway restart left the main agent's database refused. For about 80 minutes iMessage showed typing indicators but Octo never replied. `/readyz`, the Gateway log and the cron state all showed the failure, but nothing was reading them. Replaying that day's log against a baseline makes `verify` fail on exactly those signals.
