# Check Plan

Audit an existing implementation plan for unresolved questions, gaps, ambiguities, and potential improvements, then walk through each finding interactively — one at a time — so you can resolve them before `/implement`.

## Variables

plan_path: $ARGUMENTS (optional — path to a plan file. If omitted, use the most recently modified file in `plans/`.)

---

## Instructions

- **IMPORTANT:** Walk findings one at a time via `AskUserQuestion`, never batched. Interactive iteration beats a bulk Q&A dump.
- After each answer, **edit the plan file in place** so the resolution is captured. Don't accumulate edits to apply later.
- Do not call `/implement` or change any non-plan files. This command only audits and refines the plan.

---

## Phase 1: Locate the Plan

1. If `plan_path` was passed as an argument, use it directly.
2. Otherwise, list `plans/*.md` sorted by modification time (newest first) and pick the most recent. If multiple plans were modified in the same session, prefer one whose Status is `Draft` or `Ready for /implement` over `Implemented`.
3. State the chosen plan path to the user in one sentence before reading it, so they can redirect if the wrong file was picked.

---

## Phase 2: Read and Audit

Read the plan file in full. Then audit for the categories below. Be specific — every finding must point to a section or line in the plan, not a vague concern.

### Categories to check

1. **Open Questions still present** — anything in an "Open Questions" section that lacks a recorded answer.
2. **Placeholder text** — `<descriptive title>`, `<placeholder>`, `TBD`, `???`, etc. left over from the template.
3. **Ambiguities** — steps that say "consider", "maybe", "either / or" without a chosen path; mismatched numbers between sections (e.g. summary says 5 files, table has 7).
4. **Missing details for execution** — file paths that don't exist yet but aren't called out as new; code snippets that reference undefined variables; step actions that say "do X" without specifying how.
5. **Contradictions / drift** — earlier section says one thing, later section says another. E.g. a design decision says "keep the old file as a stub" but a step says "delete the old file".
6. **Validation gaps** — Success Criteria that aren't covered by any Validation Checklist item, or vice versa.
7. **Risk / scope creep** — steps that quietly expand scope beyond the request (e.g. a plan to "add one command" that secretly restructures three existing ones in step 8).
8. **Missing CLAUDE.md / context updates** — workspace-affecting changes that don't include a doc update step.
9. **Cross-reference rot** — links to files/sections that won't exist after the changes land, or references that may be stale.
10. **Reasonable improvements** — non-blocking suggestions that would make the plan stronger (e.g. "Step 7 could be parallelised with Step 8" or "this step would benefit from a quick test").

### Audit output

Build an internal list of findings, each with:
- **Title** (short — the question/issue in one phrase)
- **Category** (from the list above)
- **Severity:** `blocker` (must resolve before /implement) / `improvement` (nice-to-have) / `cosmetic` (typos, formatting)
- **Anchor:** section or line range in the plan
- **Why it matters** (one sentence)
- **Resolution options** (2-4 concrete choices, with a recommended default)

If there are zero blockers and zero improvements worth raising, say so plainly and stop — don't fabricate findings to fill a quota.

---

## Phase 3: Walk Findings Interactively

Order findings by severity: all `blocker` first, then `improvement`, then `cosmetic`. Within each group, present in plan-order (top of plan → bottom).

For each finding:

1. **Use `AskUserQuestion`** with:
   - `question:` the finding's title rephrased as a clear question
   - `header:` ≤12 chars (e.g. "Scope", "File path", "Naming")
   - `options:` 2-4 concrete choices. The recommended default goes first with `(Recommended)` in the label.
   - Each option's `description:` explains tradeoffs honestly — don't oversell the recommendation.

2. **Apply the user's answer to the plan file immediately** using `Edit`. Update relevant sections (Open Questions, Step actions, Design Decisions, Files to Modify, etc.) to reflect the chosen path. If the user picks "Other", capture their free-text response verbatim in the plan.

3. **Brief acknowledgement** (one sentence) — what was decided and which section(s) of the plan were updated — then move to the next finding.

If a finding's resolution **introduces a new finding**, append it to the queue and address after the current pass — don't recurse mid-question.

---

## Phase 4: Final Pass

After all findings are walked:

1. **Resolved Design Decisions section** — make sure the plan now has one, consolidating every interactive answer. If the plan already had this section, append the new resolutions; otherwise add it. Lead each entry with the decision, not the question.

2. **Update the plan's Status:**
   - If all blockers resolved → `Status: Ready for /implement`
   - If user deferred any blockers → leave as `Draft` and list deferred items in a "Deferred" note at the top.

3. **Report to the user:**

```
## Plan Check Complete

**Plan:** plans/YYYY-MM-DD-{name}.md
**Status:** {Ready for /implement | Draft (N deferred)}

### Resolutions captured
- {Finding 1} → {chosen option}
- {Finding 2} → {chosen option}
...

### Deferred (if any)
- {Finding} — {reason user gave}

### Recommended next step
Run `/implement plans/YYYY-MM-DD-{name}.md` to execute.
```

---

## Quality Standards

- **Specificity over generality.** A finding that says "Step 4 is vague" is useless. "Step 4 says 'update the budget doc' but three docs track budget figures and the plan doesn't say which is authoritative — is it `current-data.md` or the output file?" is useful.
- **Honest options.** Don't pad with throwaway choices. If there are genuinely only 2 sensible paths, present 2.
- **One question per turn.** Never call `AskUserQuestion` with multiple questions in the questions array — serialised iteration, not batched.
- **Edit-as-you-go.** Don't accumulate decisions and apply them at the end. Each answer → immediate Edit → move on. Lets the user redirect mid-pass without losing earlier work.
- **No phantom findings.** If the plan is solid, say so and exit. Padding the queue with weak questions trains the user to ignore the command.
