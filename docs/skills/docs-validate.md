---
layout: default
title: Docs Validate
nav_order: 2
nav_exclude: true
---

# 🧠 Docs Validate

Run `tools/docs/scripts/validate_docs.py` to check the docs manifest against live config.

## When to use

- After editing `config/doc-manifest.json`
- After adding/removing/enabling/disabling a plugin in openclaw.json
- As a pre-commit check before pushing docs changes

## Steps

Exits 0 (clean / warnings only) or 1 (errors found).

## What it checks

1. **Schema (ERROR)** — unknown keys, missing required fields (`origin`, `name`, `summary`), invalid `docsMode`, `docsMode=external` without `docsUrl`
2. **Manifest ↔ config (ERROR)** — every manifest plugin exists in `openclaw.json plugins.entries`
3. **Public but disabled (WARN)** — manifest `public:true` plugins that are `enabled:false` in config
4. **Enabled but undocumented (WARN)** — enabled non-provider/non-channel plugins missing from manifest

## Options
