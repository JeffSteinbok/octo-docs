---
layout: default
title: Self-Improvement
nav_order: 11
---

# 🔁 Self-Improvement

Octo has a small but growing set of mechanisms for detecting its own drift, inconsistencies, and quality problems — and filing issues to fix them automatically.

---

## Docs Validation

A validation script runs weekly and checks the docs manifest against the live OpenClaw config. It catches:

- **Schema errors** — unknown fields, missing required metadata, invalid `docsMode`, external plugins without a docs URL
- **Manifest/config drift** — plugins documented but no longer installed, or vice versa
- **Public but disabled** — plugins marked public in docs but disabled in config
- **Enabled but undocumented** — enabled plugins with no docs entry

For each finding the script files a GitHub issue in [`JeffSteinbok/octo`](https://github.com/JeffSteinbok/octo) tagged `docs-validate`, with deduplication so the same issue isn't filed twice. Errors get the `bug` label; warnings get `documentation`.

**Script:** [`tools/docs/scripts/validate_docs.py`](https://github.com/JeffSteinbok/octo/blob/main/tools/docs/scripts/validate_docs.py)

---

## Agent Review

A weekly agent review scans session trajectories and memory files for recurring tool failures, missing context patterns, and quality regressions. It produces a summary report and files `agent-review`-labelled issues for actionable findings.

**Skill:** [`agent-review`](/skills/agent-review)

---

## Planned: Full Fix Lifecycle

The goal is a closed loop from detection to merged fix:

1. **Detect** — validation scripts, agent review, or manual observation
2. **File** — issue auto-filed with labels
3. **Triage** — Octo reads the issue, writes a fix plan, pings Jeff for review
4. **Approve** — Jeff adds `plan-approved` label
5. **Fix** — Copilot assigned, opens PR
6. **Review** — Octo reviews PR, comments, pings Jeff
7. **Merge** — done

See [octo#208](https://github.com/JeffSteinbok/octo/issues/208) for the full lifecycle design.
