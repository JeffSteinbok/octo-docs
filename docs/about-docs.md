---
layout: default
title: About These Docs
nav_order: 12
---

# How Octo's Docs System Works

This page explains how [octo.steinbok.net](https://octo.steinbok.net) is built, from the source in the `octo` repo to the published site, and how to build something similar for your own OpenClaw instance.

---

## Overview

Most of Octo's public documentation is generated from the repo itself (plugin manifests, agent files, config, skills, cron jobs, service READMEs) rather than written by hand. A few pages, including this one, are hand-written Markdown files in the `octo` repo's `docs/` folder that the same pipeline publishes.

The pipeline runs when a push to `main` changes something the site is built from (the docs, the docs tools, plugin, service and lib folders, agent instructions and skills, top-level notes, the doc manifest), every Monday morning, and by hand. The weekly run picks up config and cron changes and memory counts, which change daily and don't start a build by themselves. Each run:

1. **Extract** — Python scripts read the repo and write structured JSON (the *bundle*)
2. **Redact** — secrets and private addresses are stripped from the bundle
3. **Render** — deterministic renderers turn the bundle into Jekyll Markdown pages
4. **Validate** — the rendered pages are scanned to make sure nothing private leaked
5. **Publish** — the rendered site is handed to the separate `octo-docs` repo, which commits it and deploys it with GitHub Pages

There is **no LLM in the pipeline**. Every step is deterministic, version-controlled and tested.

---

## Two repos

The system is split across two repos on purpose:

| Repo | Purpose |
|------|---------|
| [`JeffSteinbok/octo`](https://github.com/JeffSteinbok/octo) | Source of truth: plugins, config, agents, and the pipeline code |
| [`JeffSteinbok/octo-docs`](https://github.com/JeffSteinbok/octo-docs) | Hosts the published Jekyll site at octo.steinbok.net |

`octo` generates the docs; `octo-docs` publishes them. This means:

- `octo` can stay private while `octo-docs` is public
- The rendered output can be audited before it goes live
- The docs repo never contains raw source code

The handoff uses a GitHub Actions `repository_dispatch` event. `octo` uploads the rendered site as a `docs-site` artifact and sends a `docs-site-ready` event to `octo-docs`, which downloads the artifact, commits the pages and deploys the site.

---

## Visibility: `config/doc-manifest.json`

`config/doc-manifest.json` is the single source of truth for what appears in the public docs. It has a section per kind of thing: `plugins`, `services`, `skills`, `jobs`, `clis`, `hooks` and `pages`.

```json
{
  "plugins": {
    "config-backup": {
      "public": true,
      "origin": "octo",
      "docsMode": "local",
      "name": "Config Backup",
      "summary": "Backs up OpenClaw config to Git with SHA-256 change detection"
    },
    "fastmail": {
      "public": true,
      "origin": "openclaw-hub",
      "docsMode": "external",
      "name": "FastMail tools",
      "summary": "Send email and manage calendar events in Fastmail",
      "docsUrl": "https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/fastmail",
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
  "hooks":    { ... },
  "pages":    { ... }
}
```

**Rules:**

- Anything not listed is private by default, even if it is in the repo
- An entry needs `"public": true` to appear in the docs
- The manifest also holds display metadata: `name`, `summary`, `emoji`, `sourceUrl`, `docsUrl`, `docsMode`, `author`
- A public plugin entry must have `origin`, `name`, `summary` and `docsMode`. An unknown key fails the build, so typos are caught instead of silently ignored

### Where plugins come from

`origin` says where a plugin's code lives, and the Plugins page groups plugins by it:

| `origin` | Where the code lives |
|----------|---------------------|
| `octo` | This repo, under `plugins/<id>/` |
| `openclaw-hub`, `carapace-*` | Jeff's public open-source repos, such as [openclaw-hub](https://github.com/JeffSteinbok/openclaw-hub) |
| `builtin` | OpenClaw itself (for example Browser or Google) |
| `external` | Someone else's repo |

`docsMode` says where the plugin's documentation lives:

- `local` — the pipeline renders a full page for the plugin, with every tool documented
- `external` — the plugin is listed with a link to `docsUrl` (or `sourceUrl`); `docsMode: external` requires one of them

### External plugins

For a plugin installed from outside Jeff's repos, put the author and links in `doc-manifest.json`, not in the plugin's own `openclaw.plugin.json`. The pipeline reads `author` and `sourceUrl` from the manifest:

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

## Pipeline stages

`tools/docs/publish/emit_bundle.py` runs all five stages in order. The bundle is written to `out/docs-bundle/` and the rendered site to `out/docs-site/`.

### 1. Extract (`tools/docs/extract/`)

Each extractor is a standalone, read-only Python script that writes JSON into `out/docs-bundle/`. The orchestrator also copies `config/doc-manifest.json` into the bundle and writes a `manifest.json` listing every file.

| Extractor | Reads | Writes |
|-----------|-------|--------|
| `api_inventory.py` | Each plugin's `openclaw.plugin.json` and tool schemas | `api-index.json` |
| `agent_summary.py` | `agents/*/` identity files | `agents.json`, `agents/<id>.json` |
| `plugin_summary.py` | `plugins/*/openclaw.plugin.json` and plugin tools | `plugins/<id>.json` |
| `changelog_summary.py` | `CHANGELOG.md` | `release/changes.json` |
| `config_summary.py` | `config/openclaw.json` | `config.json` |
| `skill_summary.py` | `agents/*/skills/*/SKILL.md` | `skills.json`, `skills/<name>.json` |
| `job_summary.py` | `config/cron_jobs_export.json` | `jobs.json` |
| `service_summary.py` | `services/*/README.md` | `services.json`, `services/<id>.json` |
| `libs_summary.py` | Shared libraries under `libs/ts/` | `libs.json`, `libs/<id>.json` |
| `usps_runtime_summary.py` | The shared USPS action-module README | `libs/mail_action_usps-action.json` |
| `note_summary.py` | Setup notes in the repo root's Markdown files | `notes.json` |
| `cli_summary.py` | The `clis` manifest section and CLI READMEs in openclaw-hub | `clis.json` |
| `memory_summary.py` | Agent memory folders and memory config | `memory.json` |
| `visibility_registry.py` | `config/doc-manifest.json` | (a helper the other extractors use) |

### 2. Redact (`tools/docs/sanitize/redact.py`)

After extraction, the redactor rewrites every JSON file in the bundle and replaces:

- GitHub, Slack and `sk-` style API tokens, and bearer tokens
- Credential-looking hex strings next to words like `token` or `secret`
- URLs on internal domains (`.local`, `.internal`, `.corp`, `.intranet`, `.private`)
- Private IP addresses and URLs that use them
- Links to private GitHub repos

### 3. Render (`tools/docs/render/render_site.py`)

The renderer reads the page specs in `tools/docs/page_specs/` and writes Jekyll Markdown pages to `out/docs-site/`. A page spec looks like this:

```yaml
id: plugins-overview
output_path: docs/plugins.md       # written to out/docs-site/plugins.md
strategy: bundle-plugins           # which renderer to use
sources:
  - path: doc-manifest.json
  - path: plugins/*.json
front_matter:
  layout: default
  title: Plugins
  nav_order: 4
```

`strategy` picks a rendering function. Every strategy is plain Python, with no templating engine and no LLM:

| Strategy | What it generates |
|----------|-------------------|
| `bundle-plugins` | Plugin inventory page and per-plugin pages |
| `bundle-services` | Services overview |
| `bundle-service-detail` | One service's page |
| `bundle-skills` | Skills overview and per-skill pages |
| `bundle-scheduled-tasks` | Scheduled Tasks page |
| `bundle-agents-channels` | Agents & Channels page |
| `bundle-models` | Models page |
| `bundle-memory` | Memory page |
| `bundle-clis` | CLI Tools page |
| `bundle-hooks` | Hooks overview and per-hook pages |
| `bundle-release` | Release notes |
| `static-markdown` | A hand-written page, published from the Markdown file named in the spec's `source:` |

Hand-written pages live in the `octo` repo's `docs/` folder (this page is `docs/DOCS-PIPELINE.md`). When the renderer publishes one, it rewrites links to other hand-written pages so they work on the site, and turns links to repo files that aren't published into plain text.

### 4. Validate (`tools/docs/sanitize/validate_public.py`)

After rendering, every `.md` and `.json` file in the site is scanned for token shapes, internal hostnames (including Tailscale `.ts.net` names), private IP addresses and private repo links. Known JSON files are also checked for their required keys. Any match fails the build before anything is uploaded.

### 5. Publish

In the `octo` repo, the `docs-bundle.yml` workflow (**Build Docs Bundle**) runs:

```
push to main
    │
    ▼
npm ci && npm run build --workspaces --if-present   # build the TypeScript plugins
    │
    ▼
emit_bundle.py                                      # extract → redact → render → validate
    │
    ▼
validate_public.py out/docs-site                    # validate again, as a separate CI step
    │
    ▼
upload-artifact (docs-site)
    │
    ▼
repository_dispatch → octo-docs (docs-site-ready)
```

In `octo-docs`, the **Docs Main Pipeline** workflow (`docs-main-pipeline.yml`) receives the event and:

1. Runs a secret scan
2. Runs `generate-docs.yml` (**Receive Rendered Docs**), which downloads the artifact from the `octo` run and copies it into `docs/`. Each generated subfolder (such as `plugins/` or `services/`) is replaced in full, so retired pages are deleted. Top-level pages are copied over without deleting anything, and a short list of pages maintained by hand in `octo-docs`, such as the home page, is never overwritten. It then commits the result to `main`
3. Deploys the site with GitHub Pages (`jekyll-gh-pages.yml`)

---

## Running the pipeline locally

```bash

## Install Python dependencies
pip install -r tools/docs/requirements.txt

## Build the TypeScript plugins first (needed for tool extraction)
npm ci && npm run build --workspaces --if-present

## Run the full pipeline: extract, redact, render, validate
python tools/docs/publish/emit_bundle.py

## The site is in out/docs-site/
```

You can also run single stages:

```bash

## Run one extractor
python tools/docs/extract/plugin_summary.py

## Render from an existing bundle
python tools/docs/render/render_site.py --bundle out/docs-bundle --out out/docs-site

## Validate the rendered site
python tools/docs/sanitize/validate_public.py out/docs-site
```

To check the manifest against the live config as well, run `tools/docs/scripts/validate_docs.py` (see [Docs validation](harness#docs-validation) in the Engineering Harness, which runs it weekly).

---

## Adding content

### A plugin from this repo

1. Build the plugin in `plugins/<id>/` with an `openclaw.plugin.json`
2. Add it to `config/doc-manifest.json` under `plugins` with `"public": true`, `"origin": "octo"` and `"docsMode": "local"`
3. Push to `main`; the pipeline picks it up

### An external plugin

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

3. Don't add `author` or `repository` to the third-party plugin's `openclaw.plugin.json`

### A hand-written page

1. Write the page as Markdown in `docs/`
2. Add a page spec in `tools/docs/page_specs/<id>.yml` with `strategy: static-markdown`, `source:` pointing at the file, and the page's `front_matter`

### A new kind of generated page

1. Add a page spec in `tools/docs/page_specs/<id>.yml`
2. Add a rendering strategy in `tools/docs/render/render_site.py`
3. Add extractors in `tools/docs/extract/` if the bundle doesn't have the data yet
4. Add the matching entries to `config/doc-manifest.json`

---

## Building your own

To build something similar for your own OpenClaw instance:

1. **Copy `tools/docs/`.** All the pipeline code lives there. The extractors assume Octo's repo layout (`agents/`, `plugins/`, `services/`, `config/`), so expect to adapt them to yours.
2. **Create `config/doc-manifest.json`** listing your plugins, services, skills and jobs, each with `"public": true` or `false`.
3. **Set up the build workflow** by copying `.github/workflows/docs-bundle.yml`.
4. **Create a separate docs repo** with a Jekyll site (GitHub Pages works) and a workflow that listens for `repository_dispatch`, downloads the artifact and deploys it.
5. **Add the secrets.** The source repo needs `OCTO_DOCS_TOKEN`, a token that can send the dispatch event to the docs repo. The docs repo needs `OCTO_DOCS_BUNDLE_READ_TOKEN`, a token that can download artifacts from the source repo.

The only Python dependency outside the standard library is PyYAML.

---

## Tests

```bash
cd ~/git/octo
python -m pytest tools/docs/tests/ -q
```

The tests cover the extractors, the renderer, the bundle orchestrator, page writing, the bundle selectors, the visibility registry and `validate_docs.py`. Run them before pushing any pipeline change.
