---
layout: default
title: Memory
nav_order: 3
---

# 🧠 Memory

Octo maintains two complementary memory systems that work together to give
every agent a durable, searchable history of past work and decisions.

## Overview

| System | Mechanism | Durability |
|--------|-----------|------------|
| **Manual** | MEMORY.md + daily `memory/YYYY-MM-DD.md` files | Committed to git |
| **Autonomous** | Dreaming — background synthesis from session transcripts | Runtime only (`.dreams/`) |

The two systems complement each other: manual memory captures high-signal decisions
written by the agent; dreaming surfaces patterns and context that might otherwise be
lost between sessions.

## Manual Memory

Each agent has two types of persistent memory files, both committed to git:

### MEMORY.md — Long-term store

A single `MEMORY.md` file per agent holds curated long-term facts: user preferences,
recurring decisions, stable context that should always be accessible.
The agent writes to this file when something is worth remembering permanently.

### Daily files — `memory/YYYY-MM-DD.md`

At the end of each session (or whenever the agent judges it useful) a daily note is
written to `memory/YYYY-MM-DD.md` capturing what happened that day: tasks completed,
things in flight, context worth preserving across sessions.

### `memory_search` tool

The `memory_search` tool provides semantic search across all memory files and session
transcripts. It is the primary way agents recall prior work without having to read
every file manually.

## Dreaming

The `memory-core` plugin runs a background **dreaming** process during idle time.
When no active session is running, the plugin replays recent session transcripts and
synthesises insights — filling gaps the agent did not have time to write down manually.

### How it works

1. On idle, `memory-core` reads the session event log.
2. It identifies sessions not yet processed.
3. It runs an LLM synthesis pass and writes structured records to `.dreams/events.jsonl`.
4. On next session start the agent can query this backfill for context.

### `.dreams/events.jsonl`

Each line is a JSON record representing one synthesised memory event.
This file lives under the agent directory at runtime but is **gitignored** — it is
ephemeral runtime state, not a committed artifact.

### Backfill

If the dreaming process is started after a period of inactivity, it will backfill
all unprocessed sessions automatically before resuming normal idle-time synthesis.

## HEARTBEAT.md

Each agent's `HEARTBEAT.md` defines a daily discipline: on session start the agent
reads today's and yesterday's memory files, checks for outstanding tasks, and
surfaces anything that needs attention.

This **heartbeat discipline** complements dreaming: dreaming synthesises autonomously
in the background, while the heartbeat enforces a conscious recall step at the start
of each human-facing session. Together they ensure context is never silently lost.

## Configuration

Memory-core is configured under `plugins.entries.memory-core.config` in
`config/openclaw.json`. The following knobs are available:

| Key | Description |
|-----|-------------|
| `model` | Override the default LLM used for dreaming synthesis |
| `schedule` | Cron-like schedule string controlling when dreaming runs |
| `scope` | Which agents participate in dreaming (default: all) |

### Current configuration

No overrides are set — memory-core is running with all defaults.

## What Stays in Git

| Path | Committed? | Notes |
|------|------------|-------|
| `agents/*/MEMORY.md` | ✅ Yes | Long-term curated facts |
| `agents/*/memory/YYYY-MM-DD.md` | ✅ Yes | Daily session notes |
| `agents/*/.dreams/` | ❌ No | Runtime state; gitignored |

## Per-Agent Memory Summary

| Agent | Memory Files | Earliest | Latest | Dreams Active |
|-------|-------------|----------|--------|---------------|
| `coding` | 4 | 2026-05-04 | 2026-07-15 | — |
| `family` | 0 | — | — | — |
| `finance` | 69 | 2026-05-06 | 2026-07-16 | — |
| `hass-hooks` | 0 | — | — | — |
| `mail` | 0 | — | — | — |
| `main` | 94 | 2026-03-01 | 2026-07-16 | — |
| `notify` | 0 | — | — | — |
| `root` | 20 | 2026-03-13 | 2026-07-10 | — |
