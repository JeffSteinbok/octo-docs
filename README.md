# 🐙 Octo Docs

Public documentation site for the [OpenClaw](https://github.com/JeffSteinbok/openclaw-hub) system — a modular AI assistant framework that connects language models to real-world services.

## What's Here

- **Jekyll site** — Markdown pages published via GitHub Pages
- **`skills/generate-docs/`** — A Python script that reads the private OpenClaw config repo and generates sanitized, high-level documentation (no secrets, no IDs, no personal details)

## How It Works

The `generate-docs.py` script reads data from the openclaw repo (plugins, services, agents, channels, jobs) and fills `{{ placeholder }}` markers in the section template files under `skills/generate-docs/sections/`. The rendered pages are written to `docs/`.

No external AI tools are required — all rendering is done directly by the script.

## Generating Docs

```bash
python skills/generate-docs/generate-docs.py --source ../openclaw
```

This reads plugins, services, agents, channels, and jobs from the private config and writes the Jekyll pages to `docs/`.

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--source` | _(none)_ | Path to a local openclaw repo checkout (CI mode) |
| `--config-dir` | `~/.openclaw` | Path to the .openclaw runtime config directory |
| `--output-dir` | `./docs` | Path to the Jekyll docs output directory |

## Customizing Content

Section templates live in `skills/generate-docs/sections/`. Each template is a Markdown file with YAML frontmatter and `{{ placeholder }}` markers:

| Placeholder | Renders |
|-------------|---------|
| `{{ agents }}` | Table of agents + per-agent descriptions |
| `{{ channels }}` | Table of messaging channels |
| `{{ items }}` | List of plugins or services (depends on `data_source`) |
| `{{ jobs }}` | Scheduled jobs tables |

Override descriptions for specific items using the `overrides:` key in a section's frontmatter.

## Live Site

👉 [jeffsteinbok.github.io/octo-docs](https://jeffsteinbok.github.io/octo-docs/)
