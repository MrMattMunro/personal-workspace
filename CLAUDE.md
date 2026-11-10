# CLAUDE.md

Guidance for Claude Code when working in this repository.

---

## What This Is

A **personal planning workspace** — a structured place to think, plan, and track work across the parts of your life that matter (career, finances, health, projects, whatever you choose). You work with Claude Code across sessions: start each session with `/prime` to load your context, then use the workflow commands to plan and execute changes.

**This file is auto-loaded every session — keep it lean.** Detail belongs in `context/`, `reference/`, or the per-command files, not here.

**First time here?** Run `/setup` to configure the workspace.

---

## How Claude Should Work With Me

<Set this to how you like Claude to work. A starting point:>

- Be direct and concise. Lead with the answer, then the reasoning.
- In plan mode, don't finalise a plan until I say it's ready — let me iterate.
- Confirm before anything hard to reverse or outward-facing.
- **Docs you write get read back as fact by later sessions — label inferences AS inferences.** A conclusion you drew looks identical to something I reported once it's written down. Write "looks like X, unconfirmed", not "X".

---

## Workspace Structure

| Directory | Purpose |
| --------- | ------- |
| `context/` | Background on you and your situation. The core four (`personal-info`, `business-info`, `current-data`, `strategy`) are loaded by `/prime`. Add more topic files here and load them on demand from their own commands. |
| `plans/` | Dated implementation plans. Created by `/create-plan`, refined by `/check-plan`, executed by `/implement`. |
| `outputs/` | Deliverables — the actual things you produce (documents, analyses, assets). |
| `reference/` | Reusable reference docs and notes you'll come back to. |
| `scripts/` | Automation and any local MCP servers. |
| `resources/` | Shared data files. |
| `.claude/commands/` | The slash commands below. |
| `.claude/skills/` | Reusable skills (`skill-creator` to build your own, `mcp-integration` for wiring MCP servers). |
| `.claude/memory/` | Long-term memory index (`MEMORY.md`). |

---

## Commands

- `/setup` — First-run guided setup. Fills your context files, optionally enables search and portable memory, points git at your own repo.
- `/prime` — Load core context at the start of a session.
- `/create-plan [request]` — Plan a change before making it; output lands in `plans/`.
- `/check-plan [path]` — Audit a plan interactively for gaps and open questions.
- `/implement [path]` — Execute a plan.
- `/wrap-up [scope]` — Capture non-obvious lessons into context docs, then commit + push the session's work. `no commits` skips the commit stage; `everything` also commits other dirty files.

Each command file under `.claude/commands/` carries its full instructions.

---

## Notes

- **`context/current-data.md` is the source of truth for any metric.** If a figure lives in more than one doc, update it there and grep the old value out of the others.
- Your filled-in workspace is personal — keep your own copy in a **private** repo (see `/setup` step 6).
- Add your own `/prime-<topic>` commands as you grow areas (e.g. a career prime that loads career-specific context). Copy `prime.md` as a starting point.

---

## Maintaining This File

This file is auto-loaded every session, so its length is a tax on all of them. Add a line only for new functionality, a structure change, or a new command, and default to brevity.
