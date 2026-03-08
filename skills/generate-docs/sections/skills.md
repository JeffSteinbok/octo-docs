---
output: skills.md
title: Skills
nav_order: 3
data_keys:
  - skills
---

Generate a documentation section for OpenClaw **skills**.

Skills are standalone command-line tools that live in agent workspaces.
Each skill has a `SKILL.md` manifest describing its purpose, dependencies,
and usage. Agents invoke skills to perform specific tasks.

Use the `skills` array from the provided data. If the array is empty,
output only: "_No skills are currently configured._"

For each skill, generate:
1. An H2 heading with the skill's emoji and name (e.g., `## 🔧 skill-name`)
2. A link to the source on GitHub if `source_url` is present: `📦 [Source on GitHub](url)`
3. The skill description (one to two sentences)
4. A **Dependencies** line listing `bins` and `packages` if non-empty
5. A horizontal rule (`---`) divider

Keep descriptions concise and factual.
