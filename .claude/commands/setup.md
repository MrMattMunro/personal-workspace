# Setup

First-run setup for a freshly cloned workspace. Walk the user through configuring their workspace step by step: fill in their context files, optionally enable the search tool, optionally wire up portable memory, personalise `CLAUDE.md`, and point git at their own repo. Run this once, right after cloning.

This is a **guided, interactive stepper** — one decision at a time via `AskUserQuestion`, applying each result before moving to the next step. Never dump all the questions at once. The user can skip any step.

---

## Before you start

Open with one short paragraph: this workspace is a personal planning environment built around a few context files and a handful of slash commands. Setup will take a few minutes and nothing here is locked in — every file can be edited later. Then begin the steps.

Detect the operating system (check the environment info) so OS-specific steps (memory junction, Python command) use the right syntax.

---

## Step 1 — What you'll use it for

Ask what they mainly want the workspace to help with (multi-select is fine): e.g. **Career / work**, **Finances**, **Health**, **Personal projects**, **General planning & journaling**. Use their answer to shape the emphasis and examples in the context files you write next — don't create per-domain commands yet, just tailor the content.

## Step 2 — Fill in the context files

Walk through the four core context files in `context/`, filling each from a short conversation rather than leaving the placeholders:

1. `personal-info.md` — ask their name, roughly where they are / their situation, and what they want from the workspace. Write it back in their words, concise.
2. `business-info.md` — ask about work and the bigger-picture context around it. Skip or trim if "work" wasn't one of their focus areas.
3. `strategy.md` — ask for their top 2-4 priorities, in priority order (the first becomes what `/prime` surfaces). For each, capture the goal and one or two concrete next actions.
4. `current-data.md` — ask for any metrics they want to track and current values. It's fine to leave this light; remind them it's the single source of truth for numbers.

Ask these as a small number of open questions (not a rigid form), and **write each file as you go** so progress is visible. Keep everything in their voice. Don't invent facts — if they skip something, leave a short placeholder.

## Step 3 — Search tool (optional)

Explain the tradeoff, then ask whether to enable it:

> The **workspace-search** tool lets Claude semantically search everything in `plans/`, `outputs/`, `reference/` and `context/`. It's genuinely useful once you have a lot of notes, but it needs Python plus a one-time package install (`chromadb`), and it builds a local index on first use. You can enable it now or any time later by re-running `/setup`.

**If they enable it:**
1. Check Python is available (`python --version` or `python3 --version`). If not, tell them to install Python 3.10+ and offer to continue setup without search.
2. Install dependencies: `python -m pip install -r scripts/workspace-search/requirements.txt` (use `python3` on macOS/Linux if that's the interpreter).
3. Write `.mcp.json` to register the server:
   ```json
   {
     "mcpServers": {
       "workspace-search": {
         "command": "python",
         "args": ["scripts/workspace-search/server.py"]
       }
     }
   }
   ```
   (use `python3` as the command if that's what the system uses).
4. Tell them the server loads when Claude Code next starts, and the first `reindex_workspace(force=True)` call builds the index. MCP servers don't hot-load — they'll need to restart Claude Code to pick it up.

**If they decline:** leave `.mcp.json` as `{"mcpServers": {}}` and move on.

## Step 4 — Portable memory (optional, advanced)

Explain, then ask:

> Claude Code keeps long-term memory in a per-project folder outside this repo by default, so it won't travel when you move machines or push the repo. If you'd like memory to live *inside* the repo (in `.claude/memory/`, so it's versioned and portable), setup can link the two.

**Only on Windows**, and only if they say yes: create a directory junction from Claude Code's memory path for this project to `<repo>/.claude/memory`. Work out Claude Code's memory path from the environment (it derives from the project directory), back up or clear the existing folder if it has real content, and create the junction with `mklink /J`. Confirm afterward.

**On macOS/Linux**, offer the equivalent symlink (`ln -s`) only if they ask; otherwise recommend leaving memory at its default location. If they decline on any OS, do nothing — the in-repo `.claude/memory/MEMORY.md` still works fine as a starting index they can edit by hand.

## Step 5 — Personalise CLAUDE.md

Offer to drop their name into `CLAUDE.md` (the "How Claude Should Work With Me" line) and adjust anything that doesn't fit how they want Claude to behave. Light touch — this file is auto-loaded every session, so keep it lean.

## Step 6 — Point git at your own repo

Remind them this clone still points at the template's origin. Offer to help repoint it:
- Show the current remote (`git remote -v`).
- If they have their own (ideally **private**) repo URL, set it: `git remote set-url origin <their-url>`.
- If not, suggest creating one and offer the commands. Don't push anything on their behalf without them asking.

Note that their personal workspace should almost certainly be a **private** repo — the template is public, but their filled-in context is not.

## Step 7 — Done

Summarise what was configured in a short list, and tell them the normal flow from here:
- `/prime` at the start of each session to load context
- `/create-plan` → `/check-plan` → `/implement` to plan and execute changes
- `/wrap-up` at the end to capture lessons and commit
- re-run `/setup` any time to enable things they skipped

Keep the closing to a few lines.
