---
name: generate-docs
description: >
  Generates high-level public documentation for the OpenClaw Hub GitHub Pages site
  by reading the private openclaw configuration repo. Extracts skill descriptions,
  service overviews, agent roles, and channel types while stripping all secrets,
  account IDs, IP addresses, and personal details.
version: "1.0"
requires:
  bins: [python3]
  packages: [pyyaml]
metadata:
  openclaw:
    emoji: "📝"
    requires:
      env: []
---

# generate-docs

Reads the private `openclaw` configuration repo and generates sanitized, high-level
markdown documentation suitable for the public GitHub Pages site.

## Usage

```bash
python generate-docs.py [--config-repo <path>] [--output-dir <path>]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--config-repo` | `../openclaw` | Path to the private openclaw config repo |
| `--output-dir` | `../../docs` | Path to the Jekyll docs output directory |

### What gets documented

- Skill names, descriptions, and capabilities
- Service names and what they do
- Agent roles (not their personal context)
- Channel types (Telegram, Discord — not specific IDs)
- Architecture overview and how components connect

### What is never shared

- Account IDs, tokens, or credentials
- IP addresses or port numbers
- Email addresses or personal contact info
- Camera entity IDs or device names
- Family member details
- Calendar URLs or feeds
- Telegram/Discord user IDs
