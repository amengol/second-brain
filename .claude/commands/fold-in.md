---
description: "Fold this vault session's substance into the right places — today's journal + any project Activity Logs touched"
---

# fold-in

Route the substantive content of *this conversation* back into the vault, so a
"sporadic" session — one where I didn't explicitly journal or `/brain-flush` —
still leaves a trail in the right files. On-demand, idempotent-ish, additive.

## Mission

Survey what was actually discussed/decided this session. For each thing worth
keeping, write it to the **one right place**:
- Today's daily note → for what I worked on, what moved forward, what got
  stuck, and any new inbox items.
- A project's Activity Log → for substantive work on / decisions about a
  specific project (`200 Projects/<name>/`).

Do not write to multiple places out of confusion; pick the best home.

## Hard rules

- **No fabrication.** Only fold in things genuinely discussed or decided in
  this session. If nothing substantive happened, write nothing and say so.
- **Additive only.** Never overwrite existing journal content or hub notes.
  Append bullets at the end of each target section.
- **Don't touch the hub.** `<Project> Project Hub.md` is human-authored.
  Project entries go to the **Activity Log** via the shared helper.
- **Don't create today's daily note.** Templater owns it. If today's note is
  missing, fall back to `100 Inbox/Session Captures <today>.md` for the
  journal-shaped content (the existing flush helper logic handles this file).

## Step 1 — Survey

Scan this conversation and group what's worth folding in:

1. **Journal-worthy** (goes to today's daily note's Progress Log):
   - **Worked on**: activities I spent time on this session (even if nothing finished).
   - **Moved forward**: what actually progressed — shipped, decided, unblocked, next-step taken.
   - **Stuck / blocked**: anything parked, waiting, or hit a wall.
2. **Inbox items** (goes to "Inbox Items Captured Today"): tasks/ideas raised but not
   acted on — things to process in the weekly review.
3. **Project-touched** (per project, goes to that project's Activity Log):
   For each project in `200 Projects/` discussed substantively this session,
   determine `moved` (2-5 bullets), and if the session changed it, the new
   `next_action`. Do not invent next_action if it wasn't actually decided.

Skip casual mentions. If a project was named in passing but nothing substantive
happened, do not write a log entry for it.

## Step 2 — Write the journal

Today's daily note: `800 Journal/<YYYY-MM-DD>.md` (use today's date).

If the note **exists**: append bullets to the corresponding `###` sub-sections
under `## Progress Log` (and "Inbox Items Captured Today" if applicable),
**below any existing bullets**, preserving everything that's there. Only touch
sub-sections that have new content; do not edit any other section.

If the note **does not exist**: do not create it. Instead, append the
journal-shaped content to `100 Inbox/Session Captures <today>.md` (the helper
will create that file if missing — same path the auto flush uses).

## Step 3 — Write project Activity Logs

For each project touched, build a JSON payload and pipe it to the shared
helper. The helper appends a dated, newest-first entry and refreshes the
`type: project` frontmatter that the Projects Dashboard reads.

```bash
python3 ~/.brain/brain_flush.py <<'JSON'
{
  "project": "<exact folder name in 200 Projects/>",
  "moved": ["...", "..."],
  "next_action": "<only if it actually changed this session — else omit>",
  "status": "<only if changed>",
  "repo": "<from project context — else omit>",
  "repo_state": "<only if known — else omit>"
}
JSON
```

Run one helper call per project. Omit any fields whose value wasn't actually
established in this session — better to leave the existing frontmatter than
overwrite it with a guess.

## Step 4 — Report

End with a terse summary, no fluff:
- Each file that was updated, one line each (path + what was added).
- "Nothing folded in" if the session was substantively empty.
- Any judgment calls worth flagging (e.g. "treated X as journal not project
  because the discussion was strategic across projects, not specific").
