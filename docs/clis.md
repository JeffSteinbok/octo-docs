---
layout: default
title: CLI Tools
nav_order: 6
---

# CLI Tools

CLI tools are small command-line programs that an agent can run with its `exec` (shell) tool, for jobs that don't need a full plugin.

## How It Works

1. **Approved programs in one place.** On the Mac mini, approved commands live in `~/safebin/`. Most are short wrapper scripts that call the real tool in its repo.
2. **A per-agent allowlist.** The `main` agent's `exec` runs in `allowlist` mode: it can run only the commands named in its `safeBins` list, each with limits on the arguments it accepts. `root` runs in `full` mode for admin work. See [Agents & Channels](agents-channels) for each agent's permissions.

## Available CLIs

Only CLIs with public source are listed here; Octo publishes **1**.

| CLI | Summary | Example |
|-----|---------|---------|
| [`waitlistme`](https://github.com/JeffSteinbok/openclaw-hub/tree/main/clis/waitlistme) | Join a Waitlist.me queue, or check its status, from the command line |  |
