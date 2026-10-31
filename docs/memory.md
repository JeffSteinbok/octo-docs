---
layout: default
title: Memory
nav_order: 3
---

# 🧠 Memory

An agent starts every session without any recollection of earlier conversations. What carries over is what
is written down: each agent keeps Markdown memory files in its workspace, reads them when it needs context,
and searches them with the `memory_search` tool. A nightly **dreaming** sweep, run by OpenClaw's `memory-core`
plugin, reviews recent notes and conversations and promotes what proved important into long-term memory.

## Memory Files

| File | What it holds | Who writes it |
|------|---------------|---------------|
| `MEMORY.md` | Curated long-term facts: preferences, decisions and context that should always be at hand | The agent, and the nightly dreaming sweep |
| `memory/YYYY-MM-DD.md` | Daily notes: what happened, what's in flight, context worth keeping | The agent, during the day |
| `DREAMS.md` | The Dream Diary: a short, readable entry for each dreaming sweep | The dreaming sweep |
| `HEARTBEAT.md` | A checklist the agent works through on each heartbeat (see below) | The owner or the agent |

Agents write these files themselves when something is worth remembering. Standing rules ("always do X")
go in the agent's instructions instead, so they apply from the first turn of every session.

### Searching memory

The `memory_search` tool finds relevant passages in an agent's memory files even when the wording differs
from the original, using a mix of keyword and semantic (embedding) search. It is how agents recall earlier
work without reading every file. See OpenClaw's [memory search docs](https://docs.openclaw.ai/concepts/memory-search).

## Dreaming

Dreaming is the `memory-core` plugin's background memory consolidation. It runs as a scheduled job (by default
daily at 3:00 AM; it appears as `Memory Dreaming Promotion` on [Scheduled Tasks](scheduled-tasks)). Each sweep:

1. Reads recent daily notes and, for interactive sessions, conversation transcripts.
2. Picks out themes and facts that keep coming up.
3. Scores the candidates and promotes the strongest into `MEMORY.md`, keeping a reference to where each came from.
4. Writes a short Dream Diary entry in `DREAMS.md` describing what it did.

Only `MEMORY.md` is changed for long-term memory, and the previous version is saved first, so each change can
be reviewed. Dreaming's working state is kept in OpenClaw's own database, not in the memory files.
See OpenClaw's [dreaming docs](https://docs.openclaw.ai/concepts/dreaming) for the details.

## Heartbeat

A heartbeat is a regular scheduled turn in which an agent wakes up without being messaged and works through
its `HEARTBEAT.md` checklist: following up on pending tasks and surfacing anything that needs attention.
For `main` this is the `heartbeat-main` job on [Scheduled Tasks](scheduled-tasks). An agent whose
`HEARTBEAT.md` is empty (or only comments) skips its heartbeat, so it costs nothing.

## Configuration

Dreaming is configured under `plugins.entries.memory-core.config.dreaming` in OpenClaw's config:

| Key | Default | Description |
|-----|---------|-------------|
| `enabled` | `true` | Turns dreaming on or off |
| `frequency` | `0 3 * * *` | Cron schedule for the sweep |
| `model` | The agent's default model | Model used to write the diary and decide promotions |

### Current configuration

Octo sets no overrides, so dreaming runs with the defaults above.

## What Is Kept in Git

The agent workspaces live in this repo, and the daily [Config Backup](plugins/config-backup) job commits
changes to them, so memory files are versioned along with everything else:

| Path | Committed? |
|------|------------|
| `agents/*/MEMORY.md` | Yes |
| `agents/*/memory/YYYY-MM-DD.md` | Yes |
| `agents/*/DREAMS.md` | Yes |

## Memory by Agent

| Agent | Daily notes | Earliest | Latest | Dream Diary |
|-------|-------------|----------|--------|-------------|
| `coding` | 6 | 2026-05-04 | 2026-08-06 | Yes |
| `external` | 0 | — | — | Yes |
| `family` | 0 | — | — | Yes |
| `finance` | 175 | 2026-05-06 | 2026-10-30 | Yes |
| `group` | 0 | — | — | Yes |
| `hass-hooks` | 0 | — | — | — |
| `hassonic` | 0 | — | — | Yes |
| `mail` | 0 | — | — | Yes |
| `main` | 166 | 2026-03-01 | 2026-10-28 | Yes |
| `root` | 25 | 2026-03-13 | 2026-08-26 | Yes |
