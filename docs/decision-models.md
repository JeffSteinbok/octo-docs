---
layout: default
title: Decision Models
parent: Models
nav_order: 1
---

# Decision Models

Octo uses a **decision model** for the small yes/no and pick-one calls that a full LLM turn used to make: "is this safe to do without asking?", "is this camera event worth a text?". The model is Jev from [TypeSafe AI](https://docs.openclaw.ai/plugins/typesafe), selected per agent with `decisionModel: "typesafe/jev-latest"` (see OpenClaw's [decision models](https://docs.openclaw.ai/concepts/decision-models) page).

A decision model doesn't write text. It gets a typed question and some structured facts and returns an answer with a probability. Plugins call it through `api.runtime.decisions.evaluate`.

---

## The pattern

1. **Code gathers the facts.** The plugin pulls the fields that matter out of the request (the action and entity, the camera and what the vision model saw, the time, who is home).
2. **Clear cases skip the model.** Rules handle what doesn't need judgment: plain light switches always run, a doorbell press always alerts, "no activity" is always dropped.
3. **The model answers one typed question** for everything else, with a short rubric of what counts as true and false.
4. **The LLM only runs when there's something to say.** The decision decides whether the agent turn happens or the action runs. Writing the message stays with the agent.
5. **Failures are explicit.** If the decision model is unavailable, each gate says what happens: Hass Guard blocks (fail closed), the alert gate lets the agent decide as before.

---

## Where it's used

| Gate | Question | Status |
|---|---|---|
| [Hass Guard](plugins/hass-guard) | Is this Home Assistant action routine and safe to do without asking? (Hassonic and the Octo MCP's `external` agent) | Enforcing at 85%. Plain light and switch on/off skips the model |
| [Hass Alert Gate](plugins/hass-alert-gate) | Is this camera event worth a text to Jeff right now? (`hass-hooks`) | Log-only since 2026-10-26 |
| Cost-report labels (`agents/root/scripts/enrich_sessions.py`) | Which of 17 topics is this session about? Asked only for sessions the keyword rules can't place, which today all become "chat" | Log-only since 2026-10-26 |

The remaining candidates are tracked in [issue #436](https://github.com/JeffSteinbok/octo/issues/436): the heartbeat alert, GitHub and inbox notify gates, USPS mail importance, family request handling, weekly review labels, changelog scoring and evening-briefing events.

---

## From a script

Plugins call the decision model with `api.runtime.decisions.evaluate`. Most of the remaining gates are scripts (cost-report labels, calendar events, review labels), and scripts can't. Two pieces close that gap:

- **[Decisions Bridge](https://github.com/JeffSteinbok/openclaw-hub/tree/main/plugins/decisions-bridge)** (openclaw-hub) registers the `decisions-bridge.evaluate` Gateway method, so anything that can run `openclaw gateway call` can ask an agent's decision model a typed question. Only agents listed in its config can be named, and when the model is unavailable it returns `status: "unavailable"` rather than failing.
- **`scripts/decide.py`** (octo) wraps that call for Python and writes the log line the weekly check reads:

```python
from decide import decide, choice, log_verdict

answers = decide("root", "octo.session-labels", {"firstMessage": text},
                 {"label": {"type": "choice", "instructions": "What kind of session is this?",
                            "criteria": {"coding": "Writing or fixing code", "chat": "Conversation"}}})
label, p = choice(answers, "label")      # (None, None) when unavailable: keep today's answer
log_verdict("session-labels", what=title, decision=label or "unavailable", actual=heuristic_label, p=p)
```

A log line with `actual` (what the script would do today) is compared directly in the weekly check; the review asks Jeff whether the model's answer is right.

---

## Rolling a gate out

A new gate never starts by acting on its answers.

1. **Log-only.** The gate records its verdict for every event (one JSON line in `~/.openclaw/logs/<gate>.jsonl`) and steps aside. Behavior doesn't change.
2. **Weekly check.** When a gate goes log-only, `decision_review.py start <date>` holds the first review about a week out. After that, every Monday, `scripts/decision_review.py report` matches each verdict with what the agent actually did and texts Jeff the events where they disagree, numbered. He replies "1 yes, 2 no", and the main agent records it with `decision-review label`.
3. **Tune.** The labels show two kinds of mistake. A **missed alert** (the gate would drop something Jeff wanted) is the costly one. **Noise** (it would alert on something he didn't care about) is cheaper. `decision-review status` suggests the highest threshold that keeps every alert he wanted.
4. **Enforce.** Once a week of labels shows no missed alerts, the gate's `mode` switches to `enforce`. It keeps logging, so the weekly check keeps catching drift.

The current behavior isn't treated as ground truth: before the alert gate, `hass-hooks` alerted on 18 of 185 camera events, inconsistently. The labels are.

---

## What to know

- **Data.** Selecting a decision model sends each question's facts to TypeSafe's hosted endpoint. For the alert gate that's the camera name, the vision model's title and summary, the time and who is home, not the images. A local [Kev](https://github.com/jaredpalmer/kev) server is the alternative.
- **Rubric versions.** Each gate passes a `rubricVersion`. Change it when a rubric's meaning changes, so old and new results can be told apart.
- **Pass a signal.** `decisions.evaluate` rejects a call without an `AbortSignal` in its options ("Invalid decision contract"). Hooks that don't supply one (like `before_agent_reply`) and Gateway methods use `AbortSignal.timeout(...)`.
- **Scores stay internal.** Agents are told whether a check ran and what it decided, never the probability.
