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
| [Hass Alert Gate](https://github.com/JeffSteinbok/octo/tree/main/plugins/hass-alert-gate) | Is this camera event worth a text to Jeff right now? (`hass-hooks`) | Enforced from 2026-10-30, but silent from 2026-11-03: after OpenClaw 2026.10.10 webhook runs carry trigger `event`, which `before_agent_reply` skips, so hass-hooks handled every event itself. 0.2.0 gates on `before_agent_run`; back to log-only for a week before enforcing again ([plan](https://github.com/JeffSteinbok/octo/blob/main/specs/plan-decision-models-enforce.md)). In its first log-only week it agreed with hass-hooks on 25 of 26 events; the one difference was a rabbit it rightly dropped |
| Cost-report labels (`agents/root/scripts/enrich_sessions.py`) | Which of 17 topics is this session about? Asked only for sessions the keyword rules can't place, which today all become "chat" | Log-only since 2026-10-26 |
| Weekly agent review (`scripts/agent_review_gate.py`) | For each issue it filed: which kind (bug, enhancement, infrastructure)? And for the most similar-titled issues: same problem? | Log-only since 2026-10-26, Sundays after the review |
| Evening-briefing events (`agents/main/scripts/briefing_events_gate.py`) | Is this personal or family event Jeff's own, or FYI about another household member? Checked against the name rule ("names a family member → FYI"), which misfires on "Dinner with …" | Log-only since 2026-10-26, 21:55 Sun–Thu |
| [Heartbeat Gate](https://github.com/JeffSteinbok/octo/tree/main/plugins/heartbeat-gate) | Is anything urgent enough to message Jeff now? Facts: failing scheduled jobs, failing plugin health checks, chat channel status (alerts owned by the readiness cron), his events in the next 3 hours, the time, quiet hours. No heartbeat action due → no model call | Log-only since 2026-10-26, every 2-hour heartbeat |
| [Mail Notify Gate](https://github.com/JeffSteinbok/octo/tree/main/plugins/mail-notify-gate) | Is this email worth a text to Jeff now? Asked for each email a mail rule hands to `main`, with the rule's own instruction as context | Enforcing since 2026-11-25 (log-only since 2026-10-31) |
| [USPS Mail Gate](https://github.com/JeffSteinbok/octo/tree/main/plugins/usps-mail-gate) | For each mailpiece in the morning Informed Delivery digest: how important is it (junk to urgent), and who is it for (Jeff, Nicole, Walter or the household)? Facts are the vision model's sender, addressee and description, plus each household member's names and the former residents. Ads and mail for former residents skip the model; government mail is always high. Compared with what `usps-mail`'s 24 rules and name-matching routing would text | Written, not installed yet (log-only). A dry run on 63 real mailpieces agreed on who gets texted for 61 |
| [Approval Gate](https://github.com/JeffSteinbok/octo/tree/main/plugins/approval-gate) | A second check on Jeff's explicit approvals: when `root`, `main` or `coding` is about to upgrade OpenClaw (`update.run`, `openclaw update`) or add `ilc:plan-approved`, is his latest message an approval for that action (`approve`, `deny`, `unrelated`)? Facts are the action, what the assistant asked just before and his message. A message from another agent or the system, none seen, or a requester OpenClaw didn't resolve as the owner is `unrelated` without the model. Compared with the agent's own judgement, which was to go ahead. It never approves anything by itself | Written, not installed yet (log-only). A dry run on the 7 real upgrade runs since 2026-08-31: 5 approve at 0.93 or higher, the "Restart" → `update.run` run `unrelated`, and one borderline approve at 0.53 (a yes to a restart) |
| [Family Request Gate](https://github.com/JeffSteinbok/octo/tree/main/plugins/family-request-gate) | For each request a person sends the `family` or `group` agent: should it `handle` it, `ask_jeff` (send Jeff's main agent an approval request) or `refuse`? Replaces "anything that feels sensitive" in their `AGENTS.md`. Facts are the owner's first name, what the agent can do, the sender's role (owner, family member, unknown; from `session.identityLinks`, never the text), direct or group chat, and the request with emails, phone numbers, long digit runs and link paths masked (names, addresses and short codes aren't), cut to 500 characters. Approval outcomes from `main` and unmentioned chat in the family Discord channel are skipped. Calendar access stays in the calendar tools' ACLs, so every calendar request is `handle`. Compared with what the agent did: an approval request, a tool, or a text-only reply | Written, not installed yet (log-only). A dry run on the 11 real requests in the family and group transcripts matched what the agent did on 10 (the miss: a bare "request again" follow-up); 16 synthetic ones put injection and an unknown sender asking for Jeff's address at `refuse` |
| Unhandled mail (`unhandled-mail` gate in `config/m365-webhook-config.json`, a [carapace-mail-runtime decision gate](https://github.com/JeffSteinbok/carapace-mail-runtime#decision-gates)) | For Outlook mail that no other rule handles (Jeff's Fastmail address only forwards to Outlook, so `fastmail-sse` watches Octo's mailbox only): is it genuine (not phishing, a scam or instructions aimed at an assistant)? And is it worth a text to Jeff now? On a pass, the tool-less [`mail-reader`](https://github.com/JeffSteinbok/octo/tree/main/agents/mail-reader) agent texts Jeff a two- or three-line summary; if the decision model is unavailable, nothing is sent (`on_unavailable: block`). Verdicts go to `~/.openclaw/logs/mail-gates.jsonl` | Enforcing since 2026-11-22 at notify 0.5 (log-only 2026-11-05 to 11-21: 723 emails, 16 would have texted). Until 2026-11-21 it also ran in `fastmail-sse` on Jeff's Fastmail address, which logged most emails twice (once there, once after forwarding to Outlook) |
| Octo inbox (`octo-inbox` gate on `octo-notify-all` in `config/fastmail-sse-config.json`, a carapace-mail-runtime decision gate) | For non-GitHub mail to Octo's own mailbox (openclaw@), which `octo-notify-all` texts Jeff about every time: does Jeff need to see this? Facts are the sender, subject, SPF/DKIM/DMARC results, local time and the first 500 characters of the body. Copies of Octo's own mail arrive with no authentication results; mail claiming that sender with DKIM or DMARC `fail` counts as a possible spoof worth a text. Tracking-number pickup moved to its own ungated rule, so enforcing can't drop it. The text waits for the verdict (about 0.5 s, at most 5 s for a slow model). Verdicts go to `~/.openclaw/logs/mail-gates.jsonl`; the review asks about the emails it would have skipped | Written, not deployed yet (log-only, `on_unavailable: pass`). A dry run on 22 real emails from the last two months: 4 to text (three Apple account alerts and a reply from Nicole), 18 to skip (16 copies of Octo's own outgoing mail, two Apple marketing and onboarding emails); today all 22 text. Two spoofed test emails both text |
| Lobster changelog (`scripts/lobster_changelog_gate.py`) | For each new entry on [Lobster's changelog](https://lobster.shahine.com/changelog/): is it worth adopting in Octo (something to copy or check), or only about Lobster's own machine (a version it runs, a smoke test that passed, a retired patch)? Code fetches the page and diffs it against the weekly scan's snapshot (`agents/main/memory/lobster-changelog-last.md`) ten minutes before the scan. If the snapshot is missing or its matches are too few or too sparse to trust, nothing is scored and one `skipped` line is logged; an entry already scored isn't asked again. the facts are the entry's date, section and text (untrusted, capped at 800 characters) plus Octo's OpenClaw version and channels. Compared with today, where the scan posts every new entry to #upgrades; `post` at 0.5 or higher. Once enforcing, the scan would summarize only the `post` entries, and `unavailable` keeps today's post-everything path | Written, not scheduled yet (log-only). A dry run on the 44 entries the Oct 19 scan covered: 33 post, 11 skip (version bumps, passed smoke checks, retired patches, the docs site's Astro upgrade); every entry the scan's own "worth adopting?" list called out scored 0.77 or higher. On the 19 entries added retroactively by Oct 26: 18 post, 1 skip |

The remaining candidate, the GitHub notify gate, is tracked in [issue #436](https://github.com/JeffSteinbok/octo/issues/436). The family approval cards aren't in the Approval Gate: after an approval `main` can take any action, so there's no single tool call to check, and the card buttons already carry the request ID and only accept Jeff.

---

## From a script

Plugins call the decision model with `api.runtime.decisions.evaluate`. Many gates are scripts instead (the cost-report labels, review labels, briefing events and Lobster changelog above, and most of the candidates in #436), and scripts can't. Two pieces close that gap:

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
2. **Weekly check.** When a gate goes log-only, `decision_review.py start <date>` holds the first review about a week out. After that, every Monday, `scripts/decision_review.py report` matches each verdict with what the agent actually did and texts Jeff the events where they disagree, numbered: at most 6, two per gate, gates closest to enforcing first. A gate that has logged before but nothing for 3 days (9 for the Sunday-only agent review) gets a ⚠️ line instead of "0 events". He replies "1 yes, 2 no", and the main agent records it with `decision-review label`. `scripts/decision_review_reminder.py` prints a nudge when the day's review has no answers yet; a one-shot cron job (`decision-review-reminder`, 2026-11-23 1pm) texts it to him.
3. **Tune.** The labels show two kinds of mistake. A **missed alert** (the gate would drop something Jeff wanted) is the costly one. **Noise** (it would alert on something he didn't care about) is cheaper. `decision-review status` suggests the highest threshold that keeps every alert he wanted.
4. **Enforce.** Once a week of labels shows no missed alerts, the gate's `mode` switches to `enforce`. It keeps logging, so the weekly check keeps catching drift.

The current behavior isn't treated as ground truth: before the alert gate, `hass-hooks` alerted on 18 of 185 camera events, inconsistently. The labels are.

---

## What to know

- **Data.** Selecting a decision model sends each question's facts to TypeSafe's hosted endpoint. For the alert gate that's the camera name, the vision model's title and summary, the time and who is home, not the images. A local [Kev](https://github.com/jaredpalmer/kev) server is the alternative.
- **Rubric versions.** Each gate passes a `rubricVersion`. Change it when a rubric's meaning changes, so old and new results can be told apart.
- **Pass a signal.** `decisions.evaluate` rejects a call without an `AbortSignal` in its options ("Invalid decision contract"). Hooks that don't supply one (like `before_agent_reply`) and Gateway methods use `AbortSignal.timeout(...)`.
- **Log what the agent actually did, in its words.** A review question like "nothing failing; agent alerted; model right?" can't be answered. Gates that compare against an agent's reply log the reply itself (heartbeat-gate's `reply`), and the review quotes it.
- **Scores stay internal.** Agents are told whether a check ran and what it decided, never the probability.
