---
layout: default
title: Ha Smb
nav_order: 2
nav_exclude: true
---

# 🧠 Ha Smb

Read and write files on the HA config share (host configured via `HA_SMB_HOST`). Credentials load automatically from the workspace `.env` file.

## Share Layout

| SMB Share | Contents |
|-----------|----------|
| `config`  | HA config root — automations.yaml, scripts.yaml, configuration.yaml, blueprints/, custom_components/, etc. |

## Scripts

All scripts live at `skills/ha-smb/scripts/` relative to the workspace root. Run them directly with `bash`.

### List files

```bash
bash skills/ha-smb/scripts/ha-smb-ls.sh [remote-dir]

## Examples:
bash skills/ha-smb/scripts/ha-smb-ls.sh
bash skills/ha-smb/scripts/ha-smb-ls.sh blueprints/automation/valentinfrlch
```

### Read a file

```bash
bash skills/ha-smb/scripts/ha-smb-read.sh <remote-path> [local-dest]

## Examples:
bash skills/ha-smb/scripts/ha-smb-read.sh automations.yaml /tmp/automations.yaml
bash skills/ha-smb/scripts/ha-smb-read.sh blueprints/automation/valentinfrlch/event_summary.yaml /tmp/event_summary.yaml
```

Outputs the local destination path on success.

### Write a file back

```bash
bash skills/ha-smb/scripts/ha-smb-write.sh <local-file> <remote-path>

## Example:
bash skills/ha-smb/scripts/ha-smb-write.sh /tmp/automations.yaml automations.yaml
```

## Typical Workflow

1. Read the file to `/tmp/`
2. Edit the local copy
3. Write it back with `ha-smb-write.sh`
4. Reload HA via the REST API if needed:
   ```bash
   curl -s -X POST -H "Authorization: Bearer $HASS_TOKEN" "$HASS_SERVER/api/services/homeassistant/reload_core_config"
   # Or for automations specifically:
   curl -s -X POST -H "Authorization: Bearer $HASS_TOKEN" "$HASS_SERVER/api/services/automation/reload"
   ```

`HASS_TOKEN` and `HASS_SERVER` are already set as environment variables on this host.

## Notes

- Use forward slashes in paths — scripts convert them to backslashes for smbclient automatically.
- The `config` share is the only relevant share for HA config files. Other shares: `addons`, `addon_configs`, `ssl`, `share`, `backup`, `media`.
- Always reload automations/scripts after writing changes back.
