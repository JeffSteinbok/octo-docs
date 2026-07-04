---
layout: default
title: CLI Tools
nav_order: 6
---

# CLI Tools

CLI tools are lightweight scripts that agents can run via the `exec` tool. They live in `~/safebin/` — a directory of symlinks to approved scripts.

## How It Works

1. **`~/safebin/` directory** — contains symlinks to vetted CLI scripts
2. **Per-agent exec security** — `main` uses `security: allowlist` so it can *only* run binaries listed in its `safeBins`; `root` uses `security: full` for unrestricted access
3. **No external dependencies** — CLIs use only Python stdlib to keep the footprint minimal

## Available CLIs

**1 CLI** currently published.

| CLI | Summary | Example |
|-----|---------|---------|
| [`waitlistme`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/clis/waitlistme) | Join a Waitlist.me queue from the command line |  |
