---
layout: default
title: Self-Improvement
nav_order: 11
has_children: true
---

# 🔁 Self-Improvement

Octo has a small but growing set of mechanisms for detecting its own drift, inconsistencies, and quality problems — and filing issues to fix them automatically.

---

## Docs Validation

**Script:** `tools/docs/scripts/validate_docs.py`

Validates `config/doc-manifest.json` against the live `openclaw.json` config. Runs four checks:

| Severity | Check | Description |
|----------|-------|-------------|
| ERROR | Schema | Unknown keys, missing required fields (`origin`, `name`, `summary`), invalid `docsMode`, `external` plugin without `docsUrl` |
| ERROR | Manifest ↔ Config | Every plugin in the manifest must exist in `openclaw.json plugins.entries` |
| WARN | Public but disabled | Manifest `public: true` plugins that are `enabled: false` in config |
| WARN | Enabled but undocumented | Enabled non-provider plugins missing from the manifest entirely |

### Running it

```bash
cd ~/git/octo
python3 tools/docs/scripts/validate_docs.py          # run + file issues
python3 tools/docs/scripts/validate_docs.py --dry-run  # preview only
python3 tools/docs/scripts/validate_docs.py --no-issues  # check only, no GitHub
```

### Issue filing

For each finding, the script:
1. Fetches open issues tagged `docs-validate` to avoid duplicates
2. Files a new `JeffSteinbok/octo` issue if none already exists
3. Labels errors as `bug` + `docs-validate`, warnings as `documentation` + `docs-validate`

---

## Agent Review

**Skill:** [`agent-review`](/skills/agent-review)
**Script:** `agents/root/scripts/agent_review.py`
**Cron:** Weekly, Monday mornings

Scans session trajectories and memory files for recurring tool failures, missing context patterns, and quality issues. Produces a summary report and files `agent-review`-labelled issues for actionable items.

> ⚠️ Known bug: trajectory field names are mismatched ([#210](https://github.com/JeffSteinbok/octo/issues/210)) — cron stats are currently always 0. Fix in progress.

---

## Issue Lifecycle

Every issue filed in `JeffSteinbok/octo` flows through an automated state machine — from triage through planning, Copilot fix, PR review, and merge. Octo drives each transition; the only manual step is Jeff adding `plan-approved`.

See **[Issue Lifecycle](./self-improvement/issue-lifecycle)** for the full state machine with Mermaid diagram.
