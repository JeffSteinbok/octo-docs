# Docs — octo-docs

This repository hosts the **public documentation site** for Octo, deployed via
Jekyll to GitHub Pages at [octo.steinbok.net](https://octo.steinbok.net).

## How it works

All documentation pages are **generated in the private `octo` repo** and delivered
here as a pre-built artifact of final Markdown files with Jekyll front matter.

```
octo (private)
   │  extractors → JSON bundle → render Markdown → validate → upload artifact
   │  dispatch "docs-site-ready" event
   ▼
octo-docs (this repo)
   │  download artifact
   │  copy .md files into docs/
   │  TruffleHog secret scan
   │  Jekyll build & deploy to GitHub Pages
   ▼
octo.steinbok.net
```

## Hand-written pages

These files live directly in `docs/` and are **not** overwritten by the pipeline:

- `docs/index.md` — homepage
- `docs/404.md` — 404 page
- `docs/mail-runtime.md` — mail runtime documentation
- `docs/CNAME` — custom domain
- `docs/_config.yml`, `docs/Gemfile` — Jekyll configuration
- `docs/_includes/`, `docs/_sass/`, `docs/assets/` — theme and styling

## Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `docs-main-pipeline.yml` | `repository_dispatch`, `push`, manual | Download artifact → copy docs → secret scan → deploy |
| `secret-scan.yml` | Called by pipeline | TruffleHog scan for leaked secrets |
| `jekyll-gh-pages.yml` | Called by pipeline | Build Jekyll site and deploy to GitHub Pages |

## Manual re-deploy

Trigger the **Docs Main Pipeline** workflow from the Actions tab. Optionally provide
an artifact name and run ID; if left blank it downloads the latest successful artifact
from the `octo` repo.
