---
layout: default
title: Connection Watcher
parent: Engineering Harness
---

# Connection watcher

The root hourly `connection-watch` command checks Gateway pairings and connections, MCP bridge access, webhook proxy authentication, Funnel routes, and tailnet membership. A healthy run emits no text. The command sends one summary per run through the Gateway’s main owner iMessage route. Cron delivery is disabled because the command needs the Gateway receipt to confirm each send. Logs without verified MCP client attribution do not produce client or IP findings. The MCP bridge logs tool refusals and records validated Tailscale origin IPs for signed-in calls. An unfamiliar signed-in IP can alert even when the OAuth client ID is unavailable.

The watcher checks for more than 20 MCP 401 responses or webhook auth rejections in any rolling hour. It reads new log data from a saved byte offset and follows renamed or copy-truncated logs through retained numbered archives, including gzip archives. If the checkpoint tail or an intervening generation is missing or unreadable, it reports the gap and processes the readable history. A content fingerprint identifies a retained archive after gzip compression. Each detected gap gets its own checkpointed sequence number, so retries deduplicate and a later gap can alert. Archive identities and modification metadata distinguish shifted archives from overwritten archives. The first upgraded scan uses the prior checkpoint time to identify newer archives and reports uncertainty if a zero-offset legacy checkpoint cannot distinguish an old archive from an overwritten one. The legacy cutoff stays fixed for each log until its cursor upgrades, including when a read fails or an operator edits the baseline. Device inventory and route changes are checked each run. Owner iMessages combine findings from the same scan only when the private-socket Funnel source, client, and hourly window match. The alert lists each finding with its own count, sources, and next step. Findings with incomplete attribution appear separately. Unknown-client alerts say when the IP is unavailable. Short fingerprints identify findings without including raw log text, device IDs, OAuth client IDs, or tokens. Confirmed findings are suppressed for the lifetime of the checkpoint, including each burst category. Unconfirmed batches stay pending and retry on the next run with the same Gateway idempotency key. If an acknowledgement is lost and the Gateway’s dedupe window expires, a retry can deliver a duplicate.

The remote-access smoke script registers each intentional webhook and MCP rejection with a fresh one-time marker in `~/.openclaw/state/connection-watch-smoke/`. Each registration is bound to the service, exact route, and direct loopback. The service adds those details to the rejection log only for a marked request received directly on loopback. The watcher requires a matching recent registration and accepts it once. Public probes check routing, discovery, and signed webhook behavior. Ordinary rejections, forwarded markers, and replays count toward alerts. Keep the registration directory private to the OpenClaw account.

Verdict lines report facts that the watcher can verify. The allowlist verdict states what the bridge `clientTools` file says as of its modification time. An unreadable file is reported in the alert. Home-network attribution uses the bridge’s private-socket signed-in `ip=… via=funnel` field. The watcher also reports an overlapping health check or deploy. These facts do not change whether an alert is sent.

Configure household networks in the private `~/.openclaw/state/connection-watch/home-prefixes.json` file. Use a JSON array of CIDR strings, for example `["2001:db8:55::/64"]`. A missing or invalid file leaves home-network attribution unavailable.

Alerts give the count and Pacific time range, up to three caller origins and user-agent families, relevant health-check or live-change steps, and an inspection command or other next step. A burst counts the busiest rolling hour observed in that scan. The bridge and webhook proxy provide origin categories and validated addresses where available. Alerts use a short allowlisted user-agent family, from the fixed set `curl`, `browser`, `node`, `openai-mcp`, and `other`. Older log records can have unknown origins or user agents. The watcher reads local health-check run markers and reports, and can only attribute a lock to steps recorded while it was held. A local burst during a deployment can be test traffic, but the alert preserves mixed and public origins for investigation.

## Initialize and update

Run the commands as the OpenClaw user. Set `WATCHER` to the installed script or the path in your checkout.

```sh
python3 "$WATCHER" --initialize --bridge-client-log
python3 "$WATCHER" --dry-run --bridge-client-log
python3 "$WATCHER" --accept KIND VALUE
```

Use `--bridge-client-log` only when the running bridge appends its verified `client=` field (0.3.1 or later), and use the same setting in the hourly cron. A legacy user-agent can mimic that field, so omit the flag on older builds. Initialization snapshots live inventory and offsets, and seeds Gateway client identities and addresses observed in the preceding hour of available log history. It requires review of pending pairings before creating a baseline. The private file at `~/.openclaw/state/connection-watch/watch.json` contains the baseline, log offsets, recent rejection timestamps, pending alert batches, and confirmed anomaly fingerprints. Keep it private. Checkpoint saves sync the new file and its parent directory.

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

## Update the existing job

Acquire the live-change lock and run `python3 scripts/healthcheck.py baseline --step connection-watch-incidents`. Keep private backups of the installed script and household-prefix file if present. Configure the household CIDRs in `home-prefixes.json`.

Replace the installed script atomically at the existing cron path. The next hourly run uses the new file. Verify the cron ID and settings are unchanged. Dry-run the installed script against a private replay checkpoint, then run `python3 scripts/healthcheck.py verify --step connection-watch-incidents`. Restore the backups if verification fails, then release the lock. The sanitized replay is covered by `python3 -m unittest scripts.tests.test_connection_watch.ConnectionWatchTest.test_sanitized_replay_merges_four_calls_and_adds_factual_verdicts`.
