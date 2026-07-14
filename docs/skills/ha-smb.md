---
layout: default
title: HA SMB
nav_order: 3
nav_exclude: true
---

# 🏠 HA SMB

Read and write files on the HA config share (host configured via `HA_SMB_HOST`). Credentials load automatically from the workspace `.env` file.

## Share Layout

| SMB Share | Contents |
|-----------|----------|
| `config`  | HA config root — automations.yaml, scripts.yaml, configuration.yaml, blueprints/, custom_components/, etc. |

## Scripts

All scripts live at `skills/ha-smb/scripts/` relative to the workspace root. Run them directly with `bash`.

### List files

### Read a file

Outputs the local destination path on success.

### Write a file back

## Typical Workflow

1. Read the file to `/tmp/`
2. Edit the local copy
3. Write it back with `ha-smb-write.sh`
4. Reload HA via the REST API if needed:

`HASS_TOKEN` and `HASS_SERVER` are already set as environment variables on this host.

## Notes

- Use forward slashes in paths — scripts convert them to backslashes for smbclient automatically.
- The `config` share is the only relevant share for HA config files. Other shares: `addons`, `addon_configs`, `ssl`, `share`, `backup`, `media`.
- Always reload automations/scripts after writing changes back.
