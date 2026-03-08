# 🐙 Octo Docs

Public documentation site for the [OpenClaw](https://github.com/JeffSteinbok/openclaw-hub) system — a modular AI assistant framework that connects language models to real-world services.

## What's Here

- **Jekyll site** — Markdown pages published via GitHub Pages (`docs/`)
- **Doc generation pipeline** — LLM-powered page generator (`tools/docs/`) triggered automatically when the private OpenClaw repo is updated

## How It Works

1. A push to [openclaw](https://github.com/JeffSteinbok/openclaw) builds a docs bundle and dispatches a `bundle-ready` event
2. The `generate-docs.yml` workflow downloads the bundle, generates pages via GitHub Models (gpt-4o), and opens a PR

## Live Site

👉 [jeffsteinbok.github.io/octo-docs](https://jeffsteinbok.github.io/octo-docs/)
