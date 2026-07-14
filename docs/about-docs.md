---
layout: default
title: About These Docs
nav_order: 12
---

# How Octo's Docs System Works

This guide explains how [octo.steinbok.net](https://octo.steinbok.net) is generated end-to-end — from source code to published site — and how to build something equivalent for your own OpenClaw instance.

---

## Overview

Octo's public documentation is generated entirely from structured data, not from hand-authored HTML or markdown pages. The pipeline runs on every push to `main`:

1. **Extract** — Python scripts read plugins, agents, config, skills, cron jobs, and services from the repo and produce structured JSON
2. **Redact** — sensitive fields (hostnames, tokens, private paths) are stripped
3. **Render** — the JSON is fed through deterministic renderers that write final Jekyll Markdown pages
4. **Validate** — the rendered output is checked to make sure nothing private leaked
5. **Publish** — the artifact is dispatched to a separate `octo-docs` repo that hosts the Jekyll site

There is **no LLM in the rendering step**. Everything is deterministic, version-controlled, and testable.

---

## Two-Repo Architecture

The system is split across two repos deliberately:

| Repo | Purpose |
|------|---------|
| [`JeffSteinbok/octo`](https://github.com/JeffSteinbok/octo) | Source of truth: plugins, config, agents, pipeline code |
| [`JeffSteinbok/octo-docs`](https://github.com/JeffSteinbok/octo-docs) | Hosts the published Jekyll site at octo.steinbok.net |

`octo` generates the docs; `octo-docs` publishes them. This means:
- `octo` can be private while `octo-docs` is public
- The rendered output is always auditable before it goes live
- The docs repo never contains raw source code

The handoff happens via a GitHub Actions `repository_dispatch` event: `octo` uploads a `docs-site` artifact and triggers a `docs-site-ready` event in `octo-docs`, which downloads and commits the artifact.

---

## Visibility: `config/doc-manifest.json`

[`config/doc-manifest.json`](../config/doc-manifest.json) is the single source of truth for what appears in the public docs.

```json
{
  "plugins": {
    "fastmail": {
      "public": true,
      "origin": "openclaw-hub",
      "docsMode": "local",
      "name": "Fastmail",
      "summary": "Send email and manage calendar events in Fastmail",
      "sourceUrl": "https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fastmail"
    },
    "my-private-plugin": {
      "public": false
    }
  },
  "services": { ... },
  "skills":   { ... },
  "jobs":     { ... },
  "clis":     { ... },
  "hooks":    { ... }
}
```

**Rules:**
- Anything not listed here is private by default — even if it's in the repo
- `"public": true` is required for the entity to appear in the bundle
- The manifest also stores display metadata: `name`, `summary`, `emoji`, `sourceUrl`, `docsUrl`, `docsMode`

### Plugin types

| Type | Where it lives | How docs are generated |
|------|---------------|----------------------|
| **First-party** | `octo/plugins/<id>/` | Full local page with all tools documented |
| **External** | Outside `octo/` (e.g. `~/git/restaurant-cli`) | Listed in inventory; links to external docs |
| **Built-in** | OpenClaw itself (e.g. Browser, GitHub Copilot, Google) | Listed in inventory; links to official external docs |

### External plugins

When a plugin is installed from outside this repo, add its entry to `doc-manifest.json` — not to the plugin's own `openclaw.plugin.json`. The pipeline reads `author` and `sourceUrl` from the manifest:

```json
"restaurant-cli": {
  "public": true,
  "origin": "external",
  "docsMode": "external",
  "name": "restaurant-cli",
  "emoji": "🍽️",
  "author": "OmarShahine",
  "sourceUrl": "https://github.com/omarshahine/restaurant-cli",
  "summary": "Pluggable reservation booking via Resy, OpenTable, Tock, and other providers",
  "docsUrl": "https://github.com/omarshahine/restaurant-cli"
}
```

---

## Pipeline Stages

### 1. Extract (`tools/docs/extract/`)

Each extractor is a standalone Python script that reads from the repo and writes one or more JSON files to `out/docs-bundle/`.

| Extractor | Input | Output |
|-----------|-------|--------|
| `plugin_summary.py` | `plugins/*/openclaw.plugin.json` + plugin tools | `plugins/<id>.json` |
| `agent_summary.py` | `agents/*/` identity files | `agents.json` |
| `config_summary.py` | `config/openclaw.json` | `config-summary.json` |
| `job_summary.py` | Cron job configs | `jobs/*.json` |
| `service_summary.py` | `services/*/README.md` | `services/*.json` |
| `skill_summary.py` | `agents/*/skills/` | `skills/*.json` |
| `changelog_summary.py` | `CHANGELOG.md` | `changelog.json` |
| `visibility_registry.py` | `config/doc-manifest.json` | (used by other extractors) |

The extractors are all read-only and safe to run at any time:

```bash
cd octo
python tools/docs/extract/plugin_summary.py
```

### 2. Redact (`tools/docs/sanitize/redact.py`)

After extraction, sensitive fields are stripped from the bundle. The redactor removes:
- Private hostnames and IP addresses
- Token values and API key shapes
- Internal paths that reveal the filesystem layout
- Any field tagged as `_private` by an extractor

The bundle in `out/docs-bundle/` after redaction is what's fed to the renderer.

### 3. Render (`tools/docs/render/render_site.py`)

The renderer reads page spec YAML files from `tools/docs/page_specs/` and produces final Jekyll Markdown pages in `out/docs-site/`.

Each page spec declares:

```yaml
id: plugins-overview
output_path: docs/plugins.md     # maps to out/docs-site/plugins.md
strategy: bundle-plugins         # which renderer to use
sources:
  - path: plugins/*.json
front_matter:
  layout: default
  title: Plugins
  nav_order: 12
```

The `strategy` field selects a rendering function. All strategies are deterministic — no templating engine, no LLM:

| Strategy | What it generates |
|----------|-----------------|
| `bundle-plugins` | Plugin inventory page + per-plugin detail pages |
| `bundle-services` | Service overview + per-service pages |
| `bundle-skills` | Skills overview |
| `bundle-jobs` | Scheduled tasks page |
| `bundle-agents` | Agent/channel reference |
| `bundle-clis` | CLI tools reference |
| `bundle-hooks` | Hooks reference |
| `bundle-release` | Latest release notes |

### 4. Validate (`tools/docs/sanitize/validate_public.py`)

After rendering, every output `.md` and `.json` file is checked against a blocklist of patterns (internal hostnames, token shapes, private paths). If anything matches, the build fails before the artifact is uploaded.

### 5. Publish

The CI workflow (`docs-bundle.yml`) orchestrates everything:

```
push to main
    │
    ▼
npm ci && npm run build         # build TypeScript plugins
    │
    ▼
emit_bundle.py                  # extract → redact → render → validate
    │
    ▼
upload-artifact (docs-site)
    │
    ▼
repository_dispatch → octo-docs # trigger publish in the docs repo
```

The `octo-docs` repo listens for `docs-site-ready`, downloads the artifact, and commits the pages.

---

## Running the Pipeline Locally

```bash

## Install Python dependencies
pip install -r tools/docs/requirements.txt

## Build TypeScript plugins first (needed for tool extraction)
npm ci && npm run build

## Run the full pipeline: extract + redact + render + validate
python tools/docs/publish/emit_bundle.py

## Output is at out/docs-site/
```

You can also run individual stages:

```bash

## Extract only
python tools/docs/extract/plugin_summary.py

## Render from an existing bundle
python tools/docs/render/render_site.py --bundle out/docs-bundle --out out/docs-site

## Validate rendered output
python tools/docs/sanitize/validate_public.py out/docs-site
```

---

## Adding Content

### Adding a first-party plugin to the docs

1. Build the plugin (`plugins/<id>/`) with an `openclaw.plugin.json`
2. Add it to `config/doc-manifest.json` under `plugins` with `"public": true`
3. Push to `main` — the CI pipeline picks it up automatically

### Adding an external plugin

1. Install the plugin as usual (`openclaw plugins install ...`)
2. Add an entry to `config/doc-manifest.json`:

```json
"<plugin-id>": {
  "public": true,
  "origin": "external",
  "docsMode": "external",
  "name": "Display Name",
  "emoji": "🔌",
  "author": "AuthorName",
  "sourceUrl": "https://github.com/author/repo",
  "summary": "One-line description",
  "docsUrl": "https://github.com/author/repo"
}
```

3. Do **not** add `author`/`repository` to the third-party plugin's `openclaw.plugin.json`

### Adding a new page type

1. Create a page spec in `tools/docs/page_specs/<id>.yml`
2. Add a rendering strategy in `tools/docs/render/render_site.py`
3. Add extractor(s) in `tools/docs/extract/` if needed
4. Add the corresponding entries to `config/doc-manifest.json`

---

## Building Your Own

If you want to replicate this system for your own OpenClaw instance:

1. **Fork or copy `tools/docs/`** — all the pipeline code is self-contained there
2. **Create `config/doc-manifest.json`** — list your plugins, services, skills, and jobs with `"public": true/false`
3. **Set up the GitHub Actions workflow** — copy `.github/workflows/docs-bundle.yml`
4. **Create a separate docs repo** — set up a Jekyll site (GitHub Pages works), add a workflow that listens for `repository_dispatch` and deploys the artifact
5. **Add the `OCTO_DOCS_TOKEN` secret** — a PAT with `repo` scope on the docs repo so the dispatch can trigger it

The only external dependency is PyYAML (`pip install pyyaml`). Everything else is stdlib Python.

---

## Tests

The pipeline has a full test suite:

```bash
cd octo
python -m pytest tools/docs/tests/ -q
```

Tests cover the extractors, renderer, bundle loader, selectors, and the visibility registry. Run them before pushing any pipeline changes.
