# Personal Workspace

> 📋 **This is a template repository.** It ships with no personal content — every file is an empty starting point. Click **"Use this template"** above (or clone it) to create your own copy, then run `/setup`. Keep *your* copy private.

A clean, structured workspace for managing your life with [Claude Code](https://claude.com/claude-code) — career, finances, health, personal projects, whatever matters to you. It gives Claude a consistent place to load your context, plan work, and keep track of things across sessions.

Clone it, run one setup command, and make it your own.

---

## What you get

- **A context system** — a few markdown files describing your situation and goals, loaded at the start of each session so Claude starts grounded instead of cold.
- **A planning workflow** — slash commands to plan a change, sanity-check the plan, execute it, and capture what you learned.
- **A guided setup** — `/setup` walks you through filling everything in.
- **Optional semantic search** over your own notes.
- **Nothing personal baked in** — every content file is an empty template waiting for you.

---

## Prerequisites

- [Claude Code](https://docs.claude.com/en/docs/claude-code) installed.
- *(Optional)* Python 3.10+ if you want the search tool — `/setup` will check and guide you.

---

## Getting started

1. **Make your own private copy.** Don't work in a public fork — your filled-in context is personal. Either:
   - Click **"Use this template"** on GitHub (set it **Private**), then clone your copy, or
   - Clone this repo and repoint it at a new private repo of your own (`/setup` helps with this in its last step).

2. **Open the folder in Claude Code** and run:
   ```
   /setup
   ```
   It'll walk you through filling in your context, optionally turning on search and portable memory, and pointing git at your repo.

3. **From then on**, start each session with `/prime` to load your context.

---

## The commands

| Command | What it does |
| ------- | ------------ |
| `/setup` | First-run guided configuration. Run once after cloning. |
| `/prime` | Load your core context at the start of a session. |
| `/create-plan [what you want]` | Draft a plan for a change, saved to `plans/`. |
| `/check-plan [path]` | Walk through a plan's gaps and open questions interactively. |
| `/implement [path]` | Execute a plan step by step. |
| `/wrap-up [scope]` | Capture lessons into your context docs, then commit + push. |

---

## How it's laid out

```
context/     Who you are and what you're working toward (loaded by /prime)
plans/       Dated plans created by /create-plan
outputs/     The things you produce
reference/   Reusable notes you'll come back to
scripts/     Automation + optional local MCP servers
resources/   Shared data files
.claude/     Commands, skills, and long-term memory
CLAUDE.md    Always-loaded workspace guide (keep it lean)
```

The four files `/prime` reads — `context/personal-info.md`, `business-info.md`, `current-data.md`, `strategy.md` — are the heart of it. `current-data.md` is the single source of truth for any number you track.

---

## Making it yours

- Edit any file freely — nothing is sacred.
- Add your own `/prime-<topic>` commands as you grow an area (copy `.claude/commands/prime.md` as a starting point).
- Use the bundled `skill-creator` skill to build new skills, and `mcp-integration` to wire up external tools.

---

_Adapted from a personal Claude Code workspace, stripped of all personal content. Shared as a starting point — have at it._
