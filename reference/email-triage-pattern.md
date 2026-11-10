# Email triage pattern

A pattern for using Claude to triage your inbox — surface the handful of messages that need your eyes, collapse the rest to a count. Provider-agnostic: the *judgment* here is the reusable part; the *fetch* step depends on your email host.

This isn't wired up by default. If you want it, build the fetch step for your provider and add a `/email` command that runs it and applies the triage below.

---

## The fetch step (provider-specific)

You need a **read-only** way to pull recent unread messages with: sender, subject, date, a short preview, and ideally whether the message carries a `List-Unsubscribe` header (the standard marketing/newsletter marker). Options by provider:

- **Gmail** — the Gmail API (`users.messages.list` with `q="is:unread newer_than:7d"`), or the Gmail connector in Claude if you have it enabled.
- **Microsoft 365 / Outlook** — the Microsoft Graph API (`/me/messages` with a `$filter` on `isRead eq false` and `receivedDateTime`).
- **Fastmail or another JMAP host** — a JMAP `Email/query` with filter `{notKeyword: "$seen", after: <date>}`.

Keep it strictly read-only — nothing marked read, moved, or deleted. Have it print a plain list; Claude does the sorting.

---

## The triage (the reusable judgment)

The fetch's bulk/non-bulk split (via `List-Unsubscribe`) is crude — most "non-bulk" is still transactional noise. Apply a **content** sort instead:

- 🔴 **Needs action / time-sensitive** — real people; bills or payments due; account/security alerts (flag possible phishing; never endorse acting on a link); appointments; anything with a deadline or that asks something of you.
- 🟡 **Worth knowing** — subscription/service changes, infrastructure warnings (domains, hosting), anything touching a live priority.
- ⚪ **Noise** — receipts, shipping/delivery updates, newsletters, marketing, calendar-notification emails. **Collapse to a single count — don't list these** unless asked.

### Always surface, whatever the bucket

Pull your own standing priorities from `context/strategy.md` and list them here, e.g.:
- Anything tied to your #1 priority
- Anything medical / financial / legal with a real deadline
- A named set of important senders

---

## Reply format

- Open with one count line: *"N unread in last D days — A need action, B FYI, C noise."*
- Then the 🔴 and 🟡 items only, one line each: sender · subject · the single thing that matters.
- Don't recap the noise or dump the raw list. Keep it scannable.
- Close by offering to open any item in full, or draft a reply.
