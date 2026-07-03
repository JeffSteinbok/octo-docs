# Docs (receive & deploy)

Documentation **rendering now happens upstream** in the private `octo` repo.
This repository no longer renders anything — it just receives the pre-rendered
Jekyll Markdown pages and deploys them to GitHub Pages.

---

## Architecture

```
Private repo (octo)
   │  1. extracts + sanitizes runtime facts
   │  2. renders final Jekyll Markdown pages
   │  3. uploads them as the `docs-site` artifact
   │  4. sends a repository_dispatch event: docs-site-ready
   ▼
octo-docs (this repo)
   │  ├─ downloads the `docs-site` artifact
   │  ├─ copies the rendered pages into docs/
   │  ├─ runs a TruffleHog secret scan
   │  └─ commits to main
   ▼
GitHub Pages (Jekyll build + deploy)
```

All the previous rendering code (bundle loading, page specs, prompt building,
LLM generation, output formatting) was removed and lives in
`octo:tools/docs/render/` instead.

---

## Workflows

| Workflow | Role |
|----------|------|
| `.github/workflows/docs-main-pipeline.yml` | Orchestrator. Listens for the `docs-site-ready` dispatch (plus `push` / `workflow_dispatch`) and runs secret-scan → receive → deploy. |
| `.github/workflows/generate-docs.yml` | Downloads the `docs-site` artifact from `octo` and copies the pages into `docs/`, then commits to main. |
| `.github/workflows/secret-scan.yml` | TruffleHog scan; opens an issue and fails the run if verified secrets are found. |
| `.github/workflows/jekyll-gh-pages.yml` | Builds `docs/` with Jekyll and deploys to GitHub Pages. |

---

## Triggering a rebuild manually

```bash
gh api repos/JeffSteinbok/octo-docs/dispatches \
  --method POST \
  -f event_type=docs-site-ready \
  -F client_payload[artifact_name]=docs-site \
  -F client_payload[octo_run_id]=$OCTO_RUN_ID
```

Or run **Docs Main Pipeline** from the Actions tab, optionally supplying an
artifact name / run ID.

---

## Jekyll site

The site content lives under `docs/` (theme config in `docs/_config.yml`,
`docs/_includes/`, `docs/_sass/`). Only the generated content pages are
overwritten by the receive step; theme files are left untouched.
