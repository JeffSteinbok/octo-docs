---
layout: default
title: CLI Tools
nav_order: 7
---

# CLI Tools

CLI tools are lightweight scripts that agents can execute via the `exec` tool. They live in `~/safebin/` and are governed by the exec allowlist.

## How It Works

Octo uses a **safebin** model for shell execution:

1. **`~/safebin/` directory** — contains symlinks to approved CLI scripts
2. **Exec allowlist mode** — the gateway's `tools.exec.mode` is set to `allowlist`, meaning *only* binaries listed in `safeBins` can run; everything else is denied
3. **`safeBinTrustedDirs`** — directories the gateway trusts for resolving safebin binaries
4. **`pathPrepend`** — ensures `~/safebin/` is on PATH during exec runs

This gives agents access to specific, vetted tools without opening a full shell.

## Available CLIs

**1 CLI** currently published.

| CLI | Summary | Example |
|-----|---------|---------|
| [`waitlistme`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/clis/waitlistme) | Join a Waitlist.me queue from the command line |  |
