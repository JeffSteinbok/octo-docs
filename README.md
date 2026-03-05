# 🐙 Octo Docs

Public documentation site for the [OpenClaw](https://github.com/JeffSteinbok/openclaw-hub) system — a modular AI assistant framework that connects language models to real-world services.

## What's Here

- **Jekyll site** — Markdown pages published via GitHub Pages
- **`skills/generate-docs/`** — A Python skill that reads the private OpenClaw config repo and generates sanitized, high-level documentation (no secrets, no IDs, no personal details)

## Generating Docs

```bash
python skills/generate-docs/generate-docs.py --config-repo ../openclaw
```

This reads skills, services, agents, and channels from the private config and writes the Jekyll pages to the repo root.

## Live Site

👉 [jeffsteinbok.github.io/octo-docs](https://jeffsteinbok.github.io/octo-docs/)
