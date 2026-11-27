---
layout: default
title: Connection Watcher
parent: Engineering Harness
---

# Connection watcher

The root hourly `connection-watch` command checks Gateway pairings and connections, MCP bridge access, webhook proxy authentication, Funnel routes, and tailnet membership. A healthy run emits no text. The command sends one summary per run through the Gateway’s main owner iMessage route. Cron delivery is disabled because the command needs the Gateway receipt to confirm each send. Logs without verified MCP client attribution do not produce client or IP findings. The deployed bridge currently omits signed-in IPs and tool-refusal events. The watcher recognizes those events when a bridge log supplies them.

The watcher checks for more than 20 MCP 401 responses or webhook auth rejections in any rolling hour. It reads new log data from a saved byte offset and follows renamed or copy-truncated logs if the old file survives as `.1` or `.0`. Device inventory and route changes are checked each run. Alerts use short fingerprints to identify findings without including raw log text, device IDs, or addresses. Confirmed findings are suppressed for the lifetime of the checkpoint, including each burst category. Unconfirmed batches stay pending and retry on the next run with the same Gateway idempotency key. If an acknowledgement is lost and the Gateway’s dedupe window expires, a retry can deliver a duplicate.

## Initialize and update

Run the commands as the OpenClaw user. Set `WATCHER` to the installed script or the path in your checkout.

```sh
python3 "$WATCHER" --initialize --bridge-client-log
python3 "$WATCHER" --dry-run --bridge-client-log
python3 "$WATCHER" --accept KIND VALUE
```

Use `--bridge-client-log` only when the running bridge appends its verified `client=` field (0.3.1 or later), and use the same setting in the hourly cron. A legacy user-agent can mimic that field, so omit the flag on older builds. Initialization snapshots live inventory and offsets, and seeds Gateway client identities and addresses observed in the preceding hour of available log history. It requires review of pending pairings before creating a baseline. The private file at `~/.openclaw/state/connection-watch/watch.json` contains the baseline, log offsets, recent rejection timestamps, pending alert batches, and confirmed anomaly fingerprints. Keep it private.

After verifying a change, use the exact value from its source. The accepted kinds are listed by `--help` or an invalid `--accept` invocation. Pairing kinds use the device or node ID (or request ID if absent), `gateway-client` uses `client:mode`, IP kinds use the canonical address, and `tailnet-device` uses the Tailscale stable peer ID. Funnel values use the route prefix and compact key-sorted JSON from Funnel status, for example `'TCP 443 {"HTTPS":true}'`. Accepting a changed route replaces the old value for the same key. Use `--remove-funnel-route VALUE` for an approved route removal.

For a synthetic alert, run `--dry-run --fixture FILE` with JSON containing `source` (`gateway`, `bridge`, or `webhook`) and a single `line` using the corresponding log format. The command prints the alert and leaves the checkpoint untouched.


## Register the hourly cron

Acquire the live-change lock with `mkdir ~/.openclaw/healthcheck/live-change.lock`. Run `python3 scripts/healthcheck.py baseline --step connection-watch` before applying changes. Install the script at a stable absolute path and initialize its baseline before registering. Read the owner iMessage address from the main `partner-calendar-fetch` failure alert and use it as `OWNER_IMESSAGE`. Set `JOB_ARGV` to a JSON array containing the absolute Python executable and watcher script paths, followed by `--owner-imessage`, the owner address, and `--bridge-client-log` for a bridge with verified client logging. Use a `WATCHER_PATH` that includes the OpenClaw CLI, Node, and Tailscale binaries.

```sh
openclaw cron add --name connection-watch --agent root --every 1h \
  --command-argv "$JOB_ARGV" --command-env "PATH=$WATCHER_PATH" --timeout-seconds 120 \
  --no-deliver --json
openclaw cron edit "$JOB_ID" --no-failure-alert --json
openclaw cron run --wait --json "$JOB_ID"
```

Set `JOB_ID` from the registration result before running the edit and manual run. Check the run history for successful execution and confirm the job count increased by one. Cron registration takes effect in the running Gateway.

To test iMessage during rollout, use a synthetic unfamiliar MCP client fixture. Run the dry-run command first and confirm the alert begins with `TEST`. Then invoke the same installed script manually once with `--send-test --fixture /absolute/path/to/test.json --owner-imessage "$OWNER_IMESSAGE"`. The script records the one permitted test attempt before sending and records whether the Gateway confirmed it. The hourly cron has no test action. Run `python3 scripts/healthcheck.py verify --step connection-watch` after the manual run and test. Release the live-change lock after verification.
