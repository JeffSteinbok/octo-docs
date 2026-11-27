---
layout: default
title: Decision Models
parent: Models
nav_order: 1
---

# Decision Models

A decision model answers a narrow, structured question, such as whether an item needs attention or which category it belongs in. Octo uses Jev from TypeSafe AI for judgments like these. An automation can use the answer directly to decide whether to continue, and reserve a full language model (LLM) turn for writing a message when one is needed. [TypeSafe AI in OpenClaw](https://docs.openclaw.ai/plugins/typesafe)

## The pattern

- **Code gathers the facts.** The automation prepares a small input with the context needed for the decision.
- **Rules handle the clear cases.** If a known rule settles the question, the automation can act without asking the model.
- **The model answers one typed question.** For cases that need judgment, the automation asks for a yes-or-no answer or a choice from a defined set.
- **The LLM writes the message.** If the decision calls for a response, the agent writes the explanation, summary, or notification.
- **Failures are explicit.** The automation handles model unavailability as a separate outcome and follows a fallback chosen for that workflow.

## Where it's used

An enforcing gate can affect the workflow. A log-only gate records what it would decide while the workflow follows its existing behavior.

| Gate | Question | Status |
|---|---|---|
| Hass Guard | Can this Home Assistant action proceed without confirmation? | Enforcing, with some checks in log-only mode |
| Hass Alert Gate | Is this event worth a notification? | Log-only |
| Session topic labels | Which topic best describes this session? | Log-only |
| Weekly agent review | How should this issue be labeled or grouped with similar issues? | Log-only |
| Evening-briefing events | Should this event appear as a commitment or as an informational item? | Log-only |
| Heartbeat Gate | Does anything need immediate attention? | Log-only |
| Mail Notify Gate | Is this email worth a notification? | Enforcing |
| USPS Mail Gate | How should this incoming mail be prioritized and routed? | Log-only |
| Approval Gate | Does the reply approve the proposed action? | Log-only |
| Family Request Gate | How should the assistant handle this request? | Log-only |
| Unhandled mail | Does this otherwise unmatched email warrant a notification? | Enforcing |
| Octo inbox | Does this inbox message need attention? | Log-only |
| Lobster changelog | Is this changelog entry relevant to Octo? | Log-only |

## From a script

Start with one existing automation that repeatedly makes a small decision. Select a decision model for the OpenClaw agent that owns the workflow and define the type of answer the automation expects. A plugin can call OpenClaw's decision runtime directly. A standalone script can use a plugin to expose that runtime through the Gateway. [OpenClaw decision models](https://docs.openclaw.ai/concepts/decision-models) · [Calling a decision model from a plugin](https://docs.openclaw.ai/concepts/decision-models#call-from-a-plugin)

## Rolling a gate out

Start in log-only mode and compare the answers with what you would want the automation to do. Review both missed actions and unnecessary ones. When the gate is ready to act, keep reviewing its results so you can spot changes in behavior.

## What to know

Decide what happens if the model is unavailable before you let the gate act. If you choose a hosted provider, review what the automation sends and limit it to the facts the provider needs to answer the question.
