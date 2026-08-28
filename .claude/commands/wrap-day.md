---
description: End-of-day wrap — accountability check on morning priorities + propose reflective content for today's journal. Write only on approval.
---

# wrap-day

Close the day honestly. Looks across what actually happened today — Progress Log entries, Activity Log writes, git activity, and this conversation — and proposes:

- An **accountability check** against the morning's stated priorities.
- **Reflective bullets** for the three end-of-day questions (win / learned / would-do-differently).

Always propose first; never write to the journal without explicit approval. Reflections are personal and you are reading from evidence, not feeling.

## Mission

For today's daily note (`800 Journal/<YYYY-MM-DD>.md`):

1. Compare the morning's `My top priorities for today` against what actually moved.
2. Propose content for the three Reflections sub-sections, evidence-grounded.
3. Show both in chat. **Wait for approval — don't write yet.**
4. On approval, write into `## Reflections (End of Day)`: insert a new `### Accountability — Priorities vs Actual` sub-section at the top, and fill the three existing questions.

## Hard rules

- **No fabrication.** Every reflection bullet must trace to something in today's Progress Log, Activity Log entries, git, or this conversation. If you don't have evidence for a "win," say "no clear win surfaced — what would you say?" Don't invent.
- **Never let me off the hook.** If a priority wasn't touched, say so plainly. "Not touched. No evidence in journal, activity logs, or git." Don't soften. Per `SOUL.md`.
- **Propose-first, write-on-approval.** Show in chat first. Only write to the daily note when the owner says "looks good" / "write it" / equivalent. The owner may paste back edited content — write that verbatim.
- **Don't touch other sections of the daily note.** Only modify `## Reflections (End of Day)` and its sub-sections. Leave Morning Setup, Brain Dump, Progress Log, and Inbox Items Captured Today untouched.
- **If today's daily note doesn't exist:** check `000 Meta/Vault Setup.md` → `Daily notes:`.
  - `templater` or `core-daily-notes` → **stop.** Tell the owner their daily-note plugin didn't fire, and don't create the file yourself — creating it by hand produces a note without the template, which is worse than no note.
  - `assistant-creates` → create it from `000 Meta/Templates/Daily Note.md`, filling the date fields yourself (the template's `<% tp.* %>` expressions won't be evaluated), then continue.
  - No setup file, or no such field → stop, and suggest `/onboard` to settle it.
- **Re-run protection.** If `### Accountability — Priorities vs Actual` already exists in today's note, do not duplicate. Surface the existing block, propose updates if anything new happened since, and only write if the owner explicitly says to refresh.

## Step 1 — Gather

Read in this order:

1. Today's daily note: `800 Journal/<YYYY-MM-DD>.md`. Extract:
   - Morning priorities (the numbered list under `### My top priorities for today`)
   - Progress Log bullets (worked on / moved forward / stuck)
   - Inbox Items Captured Today
   - Brain Dump (context only — rough notes)
2. All Activity Logs under `200 Projects/*/<Project> Activity Log.md` whose newest entry is dated today.
3. Git log for the vault: `git log --since="midnight" --oneline`.
4. (Optional) Git logs from linked project repos if the conversation references them.

If the conversation history contains explicit context about today's work that isn't in the journal yet, treat it as additional evidence — but flag in your proposal that it's not yet captured in writing.

## Step 2 — Build the accountability block

For each morning priority, produce one line:

```
- **Priority N:** <verbatim priority text> → **Status: Done | Partial | Not touched.** <one-line evidence, or "no evidence in today's records">
```

Then one summary line: `*Overall:* <one-line read on the day's execution>`.

Be honest:
- If priorities were vague ("Make the brain more autonomous"), call it out — vague priorities can't be evaluated.
- If work got done on something *not* on the list, call that out too — silent priority swaps are a real pattern worth seeing.
- "Partial" means evidence exists but the priority isn't fully cleared. Say what's still open.

## Step 3 — Build the reflection content

Propose 1–3 bullets each for:

- **What was the win today?** — a real win (decision made, thing shipped, important conversation, breakthrough). If there genuinely isn't one, say so and ask the owner.
- **What did I learn?** — something concrete: skill, system, person, self. If nothing genuine surfaced, say so.
- **What would I do differently?** — a candid retrospective bullet. Pattern noticed, time wasted, scope crept, distraction taken. Per `SOUL.md` disposition — useful, not flattering.

Keep bullets short and concrete. Cite the source inline when helpful (e.g., "from the <project> activity log entry," "per the budget-framing conversation in chat") so the owner can verify.

## Step 4 — Present and wait

Output to chat in this shape:

```
## Daily wrap proposal — <today's date>

### Accountability — Priorities vs Actual
- **Priority 1:** ... → Status: ... — ...
- **Priority 2:** ... → Status: ... — ...
- **Priority 3:** ... → Status: ... — ...
*Overall:* ...

### Proposed reflections

**What was the win today?**
- ...

**What did I learn?**
- ...

**What would I do differently?**
- ...
```

Then ask:

> *Want me to write this to the journal? Edits welcome — paste a revised version and I'll write that instead.*

**Do not write to the file yet.** Wait for explicit approval.

## Step 5 — Write on approval

When approved (or owner provides an edited version):

1. Open `800 Journal/<YYYY-MM-DD>.md` using the Edit tool.
2. Insert a new sub-section `### Accountability — Priorities vs Actual` **immediately after** the `## Reflections (End of Day)` heading and **before** `### What was the win today?`. Include the bullets and the *Overall* line.
3. Under each existing reflection sub-section (`### What was the win today?`, `### What did I learn?`, `### What would I do differently?`), append the proposed bullets **below** the question heading, preserving any content already there.
4. Confirm in chat: file path + what was written.

If the owner edited the proposal, write the edited version verbatim — do not re-process.

## Step 6 — Report

One-line summary:

- `wrap-day: wrote to 800 Journal/<YYYY-MM-DD>.md — accountability + 3 reflection sections.`
- Or `wrap-day: owner declined to write; proposal stays in chat only.`

Done.
