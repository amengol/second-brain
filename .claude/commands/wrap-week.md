---
description: Sunday weekly review — accountability across the week + inbox audit + stale-next_action audit + reflective themes. Writes to 800 Journal/Weekly Reviews/<YYYY-Www>.md on approval.
---

# wrap-week

Close the week honestly. Wider scope than `wrap-day` — looks across all daily notes, Activity Logs, project state, inbox, and git for the ISO week (Mon–Sun). Per `USER.md` cadence: *"Empty inbox, review all projects, update next_actions"* + reflective themes layered on top.

Like `wrap-day`: propose-first / write-on-approval. The weekly review note is a human-authored artifact; you draft, the owner ratifies.

## Mission

For the current ISO week (or the most recently-completed week if today is Sunday/Monday):

1. **Accountability per active project** — what moved, what stalled, did `next_action` change?
2. **Inbox audit** — flag every unprocessed item with a routing suggestion (Project / Area / Archive / Keep).
3. **Stale `next_action` audit** — any active project whose `next_action` hasn't changed in 7+ days.
4. **Themes** — patterns across the week's journals (what was circled back to, what was avoided, energy patterns).
5. **Wins and decisions** of the week.
6. **Memory proposals audit** — surface `000 Meta/MEMORY pending proposals.md`: how many items are **ticked** (`[x]`, awaiting promotion to `MEMORY.md`) and how many are **unticked** (`[ ]`, awaiting the owner's keep/skip decision). Two nudges: remind the owner to review the unticked ones, and offer to promote the ticked ones.
7. **Getaway check** — did any drive-to getaway happen this week (camping, cabin, B&B, hotel, road trip)? If so, it belongs in `200 Projects/Family Getaways/Trip Log.md`. Getaways are event-driven, so no date-based trigger catches them — this is the weekly net under the only fragile part of that project. An unlogged trip is a silently lost data point, and the decision it feeds isn't due until Oct 2028.

Propose in chat. On approval, write `800 Journal/Weekly Reviews/<YYYY-Www>.md`. Do **not** auto-edit hubs, Activity Logs, or inbox files as side effects — surface them; let the owner act.

## Hard rules

- **No fabrication.** Every bullet traces to evidence in journals, Activity Logs, hubs, inbox, git, or this conversation.
- **Don't touch projects, hubs, Activity Logs, or inbox items as side effects.** The weekly review note is the only file this command writes. Everything else is surfaced for owner action.
- **Propose-first, write-on-approval** for the weekly review note itself.
- **Never let me off the hook.** Stalled projects, ignored inbox items, vague priorities, scope creep — name them. Per `SOUL.md`.
- **Re-run protection.** If `800 Journal/Weekly Reviews/<YYYY-Www>.md` already exists, do not overwrite. Read it, surface what's there, and only update if the owner explicitly says to refresh.

## Step 1 — Determine the week

Use ISO week:

- Week starts Monday, ends Sunday.
- Year-week identifier: `YYYY-Www` (e.g., `2026-W21`).
- Default: wrap the ISO week today falls in.
- If today is **Sunday**, wrap the week ending today (Mon → Sun).
- If today is **Monday or Tuesday**, ask the owner: "Wrap last week (Mon → Sun ending yesterday/two days ago) or this week so far?" — both are valid.

Compute the date range explicitly so downstream reads know what to include.

## Step 2 — Gather

Read in this order:

1. **Daily notes for the week's date range** — `800 Journal/<YYYY-MM-DD>.md` for each Mon–Sun date. Missing days = note them; don't panic.
2. **Activity Logs** — every `200 Projects/*/<Project> Activity Log.md`. For each, extract entries whose timestamp falls within the week's range. Also note the file's frontmatter `updated:` to detect staleness.
3. **Projects Dashboard** — `200 Projects/000 Projects Dashboard.md`. Identify all active projects.
4. **Each active project's hub** — `200 Projects/<Project>/<Project> Project Hub.md`. Cross-reference its `next_action` with the Activity Log's frontmatter `next_action` (the Activity Log is the canonical source per the two-tier model — flag any drift).
5. **Inbox** — list every file in `100 Inbox/` except `README.md`. For each, read enough to summarize in one line.
6. **Vault git log for the week** — `git log --since="<Monday>" --until="<Sunday +1 day>" --oneline`.
7. **Memory pending proposals** — `000 Meta/MEMORY pending proposals.md`. Count the `- [x]` (ticked → awaiting promotion) and `- [ ]` (unticked → awaiting review) items. This is the staging inbox; `MEMORY.md` (vault root) is the destination. The morning `memory_reflect.py` script appends candidates here; the owner ticks; this command is where promotion + review get nudged weekly.
8. **Trip Log** — `200 Projects/Family Getaways/Trip Log.md`. Note the most recent logged trip's date. Cross-reference against this week's daily notes: a getaway mentioned in a journal but absent from the log is the thing to surface.

## Step 3 — Build the review draft

Compose a draft of the weekly review with this exact structure:

```markdown
---
type: weekly-review
date: <Sunday's date>
week: <YYYY-Www>
tags: [type/weekly-review]
---

# Weekly Review — <YYYY-Www> (<Mon date> → <Sun date>)

## Wins of the week
- <bullet — concrete win with one-line evidence>
- ...

## Project Accountability
For each active project, one entry:

- **<Project name>**
  - Moved: <1–2 lines of what changed this week, from Activity Log entries>
  - `next_action`: <current value>. Last updated <date>. <Changed this week? Y/N>
  - <Optional: anything stalled or stuck>

## Stale `next_action`s (7+ days unchanged)
- **<Project>** — last updated <date>. Current `next_action`: "..."

*If none: "None — every active project's `next_action` was touched within 7 days."*

## Inbox Audit
For each file in `100 Inbox/` (excluding `README.md`):

- `<filename>` — <one-line summary> → **Suggested:** Project (<which>) / Area (<which>) / Archive / Keep

*If empty: "Inbox is empty. ✅"*

## Memory Proposals Audit
Status of `000 Meta/MEMORY pending proposals.md`:
- **Ticked, awaiting promotion:** <N> — <one-line list, or "none">
- **Unticked, awaiting your review:** <N> — oldest dated <date>

*If both zero: "Pending proposals clear. ✅"*

## Getaways
- <Any drive-to getaway found in this week's journals> → **In [[Trip Log]]? Y/N**

*If none: "No getaways this week."*
*Flights don't count. Off-season trips still get logged — they just don't vote on the gates.*

## Themes
Observational, direct. Patterns across the week's journals — what was circled back to, what was avoided, energy patterns, recurring frictions. Per `SOUL.md`: pattern detection is part of your job.

## Decisions made this week
- <Dated decision — from journal or Activity Log>
- ...

## What I'd do differently next week
- <Candid retrospective bullet>
- ...
```

## Step 4 — Present and wait

Output the entire draft to chat. **Don't write anything yet.**

After the draft, surface the call to action as **separate offers** the owner can accept independently:

1. *"X stale `next_action`s — want to update any now? I can walk through them one at a time."*
2. *"Y inbox items waiting — want to triage them now?"*
3. *"Z ticked memory proposals awaiting promotion + W unticked awaiting your review — want to promote the ticked ones now, and/or walk the unticked ones?"*
4. *"A getaway this week isn't in the Trip Log — want to log it now? Takes ~2 min."* (only if one is missing)
5. *"Want me to write the weekly review to `800 Journal/Weekly Reviews/<YYYY-Www>.md`?"*

## Step 5 — Write on approval

If the owner approves writing the weekly review note:

1. Ensure `800 Journal/Weekly Reviews/` exists. Create it if missing (`mkdir -p`). This is a vault-canonical location.
2. Write `800 Journal/Weekly Reviews/<YYYY-Www>.md` using the draft (incorporating any owner edits verbatim).
3. Confirm in chat: file path written.

If the owner wants to triage inbox items or update stale `next_action`s, handle those **interactively, one at a time**:

- For each inbox item: ask "Move to <suggested target>? Keep? Archive?" — only act on explicit confirmation per item.
- For each stale `next_action`: surface the project + current value + ask for a new value. If owner provides one, update via `python3 ~/.brain/brain_flush.py` (same helper `fold-in` uses) — never edit hubs directly.

If the owner wants to process memory proposals (`000 Meta/MEMORY pending proposals.md`):

- **Promote ticked items:** for each `- [x]` item, write it into the right bucket of `MEMORY.md` (vault root) — *Active decisions* / *Lessons learned* / *Durable facts* — keeping the `**YYYY-MM-DD**` date prefix, then **delete that line from the pending file**. Promotion and removal happen together. Confirm the batch with the owner before writing, then report what landed where.
- **Walk unticked items:** present each `- [ ]` one at a time — owner says keep (→ tick, then promote as above) or skip (leave unticked to age out, or delete if clearly junk on the owner's say-so). Never tick on the owner's behalf.
- `MEMORY.md` stays short — if an item duplicates or supersedes an existing line, update/replace rather than append.

If the owner wants to log a getaway, append one row to `200 Projects/Family Getaways/Trip Log.md` and refresh the scoreboard. Ask for what the journal doesn't already give: **Who** (just us / with friends / group — the dominant variable; never record a Fun score without it), **Comfort 1–5**, and **"would being in a trailer have improved this trip — better / no difference / worse"** (ask about *being in* one, not owning one). Cost is **all-in** — fuel, food, lodging, border. Never write the row without the owner's own numbers.

Don't batch silently. Each action is its own confirm.

## Step 6 — Report

One-line summary covering:

- Whether the weekly review note was written (path).
- How many inbox items were triaged this session (and how many remain).
- How many stale `next_action`s were refreshed (and how many remain).
- How many memory proposals were promoted to `MEMORY.md` (and how many ticked/unticked remain in the pending file).
- Any open follow-ups the owner explicitly deferred.

Done.
