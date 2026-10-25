---
layout: default
title: Health Check
parent: Engineering Harness
nav_order: 2
---

# 🩺 Health Check

`scripts/healthcheck.py` is a regression check to run between implementation steps, so a change that breaks something
is caught before the next one lands and can be unwound. It snapshots the system before a step, runs read-only probes
after it, and reports everything that changed but wasn't declared.

```bash
scripts/healthcheck.py baseline --step <step>     # before the change

## ... make the change ...
scripts/healthcheck.py verify --step <step>       # after: GO / NO-GO (exit 0 / 1)
scripts/healthcheck.py wait-ready --step <step>   # after any Gateway restart
scripts/healthcheck.py probes                     # list the probes
```

## What it checks

About 40 read-only checks in roughly 13 seconds:

| Area | Checks |
|---|---|
| Gateway | `/healthz`, `/startupz`, `/readyz` (agent databases, channels, plugin reload, event loop), `openclaw health`, CLI and Gateway versions, stability bundles, listening ports |
| Channels | Each enabled channel configured, running, connected and ready; the iMessage bridge process |
| Hooks | `main` can never be run by a hook; the [remote-access smoke test](external-integrations#verifying-changes); proxy and GitHub hook logs |
| Plugins | Enabled plugins loaded; degraded plugins or secret owners |
| Agents | Agent list and models, database files present and sane, session counts (a refused database makes them collapse to zero) |
| Cron | Scheduler on; job errors, especially agent-database admission failures; overdue jobs; failed runs since the baseline |
| Services | LaunchAgents running, plist hashes, program arguments, env key names; service log errors since the baseline |
| Config | `openclaw.json` hash and a redacted projection; env files as key names and value lengths only; service configs |
| Funnel | Routes, and drift from the committed `config/tailscale/funnel.json` |
| Devices | Paired devices, admin count, pending requests, nodes |
| Logs | New Gateway log lines since the baseline, matched against known failure signatures |

## Before and after

`baseline` records an inventory of the system. `verify` takes a new one and classifies every difference:

| Class | Meaning | Result |
|---|---|---|
| telemetry | Values that move on their own: timestamps, pids, database sizes, log offsets, service runtime state | ignored |
| expected | Declared in the step's expected-changes file | pass |
| counter | A counter that must not grow grew: cron errors, service restarts, failed deliveries, admin devices | FAIL |
| soft | A change worth a warning, such as a laptop node going to sleep | WARN |
| undeclared | Anything else that changed, appeared or vanished | FAIL |

Each step declares what it is supposed to change in `config/healthcheck/steps/<step>.json`, including whether a
Gateway or service restart is expected. Known pre-existing findings live in `config/healthcheck/accepted.json`.

## After a restart

`wait-ready` polls `/healthz`, then `/startupz`, then `/readyz`, allowing up to 8 minutes, because an agent database
can take minutes to be admitted after a restart. If an agent database is refused, it prints the recovery procedure
(`openclaw doctor --fix`) instead of waiting. When the Gateway is ready it runs the Gateway, channel, agent and cron
checks.

## Reports and secrets

Reports go to `~/.openclaw/healthcheck/steps/<step>/` (mode 600). They never contain secret values: env files are
recorded as key names and value lengths, config secrets are redacted, and log samples pass through a redactor.

## Why it exists

On 2026-10-24 a routine Gateway restart left the main agent's database refused. iMessage showed typing indicators and
never replied for about 80 minutes, while `/readyz`, the Gateway log and the cron state all reported the failure and
nothing read them. Replaying that day's log against a baseline makes `verify` fail on exactly those signals.
