# Prime

> General session init. Loads your core personal/work context so Claude starts each session grounded. Run this (or a more specific prime you create) at the start of a session.

## Read

- `context/personal-info.md`
- `context/business-info.md`
- `context/current-data.md`
- `context/strategy.md`

**Do not** auto-read the rest of `context/`. Any topic or project files you add later should be loaded on demand by their own commands, not here — this keeps every session's starting context lean.

## Summary

Reply in ≤4 lines. **Do not recap the loaded files** — you wrote them. Just confirm what loaded, state the current top priority from `context/strategy.md`, and say you're ready. Don't restate the workspace structure or command list (that's already in `CLAUDE.md`, which is always in context).
