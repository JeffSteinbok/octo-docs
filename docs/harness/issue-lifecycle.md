---
layout: default
title: Issue Lifecycle
parent: Engineering Harness
nav_order: 1
---

# Issue Lifecycle — State Machine

This document describes the automated lifecycle for issues filed in `JeffSteinbok/octo` — from detection through triage, planning, Copilot fix, PR review, and merge.

---

## State Machine

```mermaid
stateDiagram-v2
    [*] --> Opened : issue opened

    Opened --> PlanPending : Octo picks up issue\nadds plan-pending label

    PlanPending --> PlanReady : Octo writes plan\ncomments on issue\nadds plan-ready label

    PlanReady --> PlanApproved : Jeff adds\nplan-approved label

    PlanReady --> NeedsInput : Jeff adds\nneeds-input label\n(plan needs changes)

    NeedsInput --> PlanPending : Jeff updates issue\nor clarifies

    PlanApproved --> CopilotAssigned : Octo assigns @copilot\nadds copilot-assigned label

    CopilotAssigned --> PRReview : Copilot opens PR\nOcto adds pr-review label

    PRReview --> Merged : Jeff merges PR

    PRReview --> CopilotAssigned : PR needs rework\nOcto requests changes

    Merged --> [*]
    Opened --> [*] : closed as wontfix\nor duplicate
```

---

## Labels

| Label | Meaning |
|---|---|
| `plan-pending` | Octo is reading the issue and writing a plan |
| `plan-ready` | Plan written and commented — awaiting Jeff's review |
| `plan-approved` | Jeff approved the plan — Copilot can be assigned |
| `needs-input` | Plan needs changes or clarification before proceeding |
| `copilot-assigned` | Copilot is working on the fix |
| `pr-review` | PR is open — Octo has reviewed and pinged Jeff |

Only one lifecycle label should be active at a time. Octo manages transitions automatically; the only label Jeff needs to add manually is `plan-approved` (or `needs-input` to push back).

---

## What Octo does at each step

### Issue opened
1. Adds `plan-pending`
2. Reads the issue body
3. Writes a plan comment — what changes, which files, approach, risks
4. Replaces `plan-pending` with `plan-ready`
5. Pings Jeff in `#root`

### `plan-approved` label added
1. Removes `plan-ready`
2. Assigns `@copilot` to the issue
3. Adds `copilot-assigned`
4. Pings Jeff in `#root`

### PR opened by Copilot
1. Reads the diff
2. Reviews for correctness, completeness, style
3. Posts a review comment on the PR
4. Adds `pr-review` to the issue
5. Pings Jeff in `#root`

---

## Skill

The coding agent's `issue-lifecycle` skill implements this flow. It is invoked by the `github-issues` webhook hook mapping whenever a relevant issue or PR event fires.

See [`agents/coding/skills/issue-lifecycle/SKILL.md`](../agents/coding/skills/issue-lifecycle/SKILL.md).
