# Wrap Up

Review the current session's work, capture any non-obvious lessons into the appropriate context docs, then commit and push the session's work. Keep captures terse — three lines max per lesson.

**Default is SKIP, not save.** Context docs bloat fast when wrap-ups treat "interesting" as the bar. The bar is "this will trip a future session that hasn't seen this conversation." Most sessions capture 0-2 lessons. A wrap-up reporting 5+ saves is a red flag — re-read each and cut anything routine, mechanical, or derivable from the files themselves. A wrap-up reporting zero lessons is a fine outcome.

## Variables

$ARGUMENTS (optional). Carries up to two things — a **commit mode** and a **lesson scope** — which can combine.

**Commit mode** (controls Phase 5; parse this out of the argument FIRST):

- **`no commits`** (also `no commit`, `nocommit`, `skip commit`, `skip commits`, `no push`) → **SKIP MODE**: do Phases 1-4, then skip the commit & push stage entirely.
- **`everything`** (also `commit everything`, `wrap up everything`) → **EVERYTHING MODE**: commit + push this session's work AND any pre-existing / concurrent dirty files noticed in the repo.
- **neither keyword present** → **DEFAULT MODE**: automatically commit + push only THIS session's work; leave any other dirty files alone.

**Lesson scope** — whatever text is left after removing a commit-mode keyword narrows lesson focus (e.g. `health`, `finance`, a project name). If nothing remains, infer scope from the session's actual work.

---

## Instructions

### Phase 1: Identify what happened in this session

Look at the conversation for:
- Plans implemented (status changed Draft / Ready → Implemented)
- Files created or substantially modified
- Problems hit and fixed inline
- Approaches that didn't work the obvious way
- Surprising tool / library / service behaviour

If the session is large or ambiguous, ask ONE focused question about the slice to wrap up. Otherwise proceed.

---

### Phase 2: Extract reusable lessons

A lesson is worth capturing ONLY if it's:
- **Non-obvious** from reading the current file state
- **Likely to bite again** in a future session
- **A correction to an assumption** ("I thought X, but Y") OR **confirmation of a surprising approach** ("the obvious A/B failed; C worked")

Skip:
- Routine mechanics — derivable from the files themselves
- File paths, folder structure, file names — those are in the workspace
- Things already covered in `CLAUDE.md` or any `context/*.md`
- Anything that's just "I did the work as planned"

---

### Phase 3: Decide WHERE each lesson goes

| Lesson scope | Target |
|---|---|
| A workspace / Claude Code workflow lesson | `CLAUDE.md` |
| A fact or state about one of your ongoing areas (health, finance, a project) | the relevant `context/*.md` |
| A user-specific habit or preference ("I prefer X") | auto-memory via the memory system (a `feedback_*.md`) |
| A reusable gotcha about a tool/library you use | the relevant `context/*.md`, or a new `reference/` doc if it's substantial |

**Update in place, don't accumulate.** Before adding a new bullet, Grep the target file for related content. If a similar lesson exists, tighten it rather than appending a parallel one. Parallel near-duplicates are how docs bloat.

**Append to existing sections** rather than creating new top-level files. Grep for the closest existing heading and insert there. Create a new section only if the lesson genuinely belongs in a new category.

---

### Phase 4: Apply edits

For each lesson:
1. Read the target file (or just `Grep` for the nearest heading)
2. Use `Edit` to append a concise bullet or short paragraph in the right section
3. Format: **bold lead phrase** on what surprised you, then a sentence on why, then a sentence on how to apply / avoid. Three lines max.

---

### Phase 5: Commit & push (automatic — driven by the commit mode)

**If the commit mode is SKIP → do nothing in this phase.** Note in the Phase 6 report that commits were skipped by request, and list what's left dirty.

Otherwise commit + push **automatically** — you opted into this by invoking `/wrap-up`. What differs between the two auto modes is only *which files* get staged. The Git Safety Protocol below applies in full either way.

**Detection:**

1. Identify dirty repos: the workspace repo, plus any external project the session touched (check the environment's working directories and the file paths Edit / Write touched).
2. For each candidate, run `git status --porcelain` from inside that directory (`git -C <dir> status`). Skip repos with a clean tree.
3. For each dirty repo, classify files into:
   - **Session-attributable** — touched via Edit / Write during THIS conversation, including the Phase 4 lesson edits.
   - **Pre-existing / other-session** — dirty at session start, or modified by something other than this session.

**What to stage, per dirty repo:**

- **DEFAULT MODE** — stage ONLY the session-attributable files (by explicit filename). Leave the rest dirty and report them under "Still dirty".
- **EVERYTHING MODE** — stage BOTH groups (still by explicit filename). The commit message must honestly describe both — never bury other-session changes under a session-only headline.

**Executing the commit (Git Safety Protocol — follow verbatim):**

- Stage **by explicit filename**, never `git add -A` / `git add .` / `git add -u` — that's how secrets, large binaries, and a concurrent session's half-finished work leak in.
- **Re-run `git status` / `git log` immediately before staging** — HEAD may have moved since detection. Stage against current state.
- One commit per repo per session (don't slice into several).
- Use a HEREDOC (`git commit -F -` with `cat <<'EOF'`) for the message so multi-line formatting survives.
- Message should lead with `<area>: <short headline>`, then 2-4 short paragraphs on what changed and why.
- Never `--no-verify`, never `--no-gpg-sign`, never `--amend` unless the user explicitly asks.
- If a pre-commit hook fails, fix the underlying issue and create a NEW commit (don't amend).

**Pushing:**

After a successful commit, push to the tracked branch (`git push origin <branch>`). No extra confirmation needed UNLESS (pause and ask):

- The target branch is `main` / `master` AND the push would be a force push — never do this without explicit instruction.
- The local branch is ahead of origin by an unusually large number of commits (>10).
- A push is rejected (non-fast-forward) because something pushed first — fetch, integrate, and retry rather than force.

**Skip Phase 5 entirely when:** commit mode is SKIP, or there are no dirty repos (say so and move on).

---

### Phase 6: Report

```
## Wrap-Up Complete

### Lessons captured
- <one-line summary> → `CLAUDE.md` (Section)
- <one-line summary> → `context/health.md` (Section)

### Files edited
- `context/...`

### Skipped (not worth saving)
- <one-line reason> — already documented / routine

### Commits pushed
- `<repo>` `<old>..<new>` — `<short msg>`

### Still dirty
- `<repo>/<file>` — <why left unstaged>
```

If nothing was worth saving, say so plainly: "Session was routine — no non-obvious lessons to capture."

State the commit mode in one line when it wasn't the default. In SKIP mode, omit "Commits pushed" and list everything under "Still dirty". If everything committed cleanly, omit "Still dirty".
