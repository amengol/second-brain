---
description: Load Second Brain context — run this at the start of every session
---

# Prime: Load Second Brain Context

## Objective

Build a full picture of the current vault state: active projects, inbox status, recent journal, and anything blocked or stalled. Then give a concise accountability briefing.

---

## Process

### 1. Read the AI Contract

Read `CLAUDE.md` at vault root — this is the operating agreement. Internalize the conventions, project list, and accountability protocol before doing anything else.

### 2. Read the Projects Dashboard + each Active Project

Read `200 Projects/000 Projects Dashboard.md`.

For each Active project listed, read BOTH of the following:

1. **Project Hub** (`<Project> Project Hub.md`) — human-authored strategy, the "what each project is" frame. Use this for context and open questions.
2. **Activity Log** (`<Project> Activity Log.md`) — live state. The frontmatter `next_action:` is the canonical source of truth for "what's the next physical action" (CLAUDE.md §Accountability System). The most recent body entry tells you what just moved.

If a project has no Activity Log, fall back to the Hub's `next_action` (rare — flag it as a gap).

When the briefing quotes the next action, **quote the Activity Log frontmatter near-verbatim**. Do not paraphrase the dashboard or soften deadlines.

### 3. Read Recent Meeting Notes

List the last 3 dated folders in `700 Meetings/`. Read any meeting notes inside them that relate to Active projects from step 2. These are the highest-fidelity record of what was actually said — sales calls, partner conversations, decisions.

### 4. Check the Inbox

Read `100 Inbox/README.md`, then list all files currently in `100 Inbox/` (excluding README.md).

Note: how many unprocessed items are there? Are any of them time-sensitive?

### 5. Check the Last Two Journal Entries

List files in `800 Journal/` sorted by name descending. Read the most recent **two** entries.

Today's entry is often still mid-template (morning setup only). Yesterday's entry usually carries the actual progress log + reflection — that's where commitments and lessons live.

If today's "What would I do differently" section in yesterday's entry made specific commitments (fill morning priorities, update X log, stop deferring Y), check today's morning setup against them. Flag mismatches.

If no journal entries exist yet, note that.

### 6. Check Git Status

!`git log -5 --oneline`
!`git status --short`

Note recent vault commits to understand what has changed recently.

---

## Output: Session Briefing

Provide a concise, scannable briefing in this format:

### Active Projects

For each project: name + current phase, then the **Activity Log `next_action` quoted near-verbatim** (trim only for readability — never paraphrase away specifics like prices, deadlines, scope caps, or "do NOT" guardrails). Include the Activity Log's `updated:` date so staleness is visible.

Flag any project where `next_action` is empty, hasn't been updated in >3 days, or is contradicted by something in a recent meeting note / journal entry.

### Inbox

- Number of unprocessed items
- Any items that look time-sensitive or actionable right now

### Energy Check

Based on the last two journal entries: current energy, mood, focus. If today's morning setup is still empty templates, say so.

### Accountability — Yesterday → Today

If yesterday's journal had a "What would I do differently" section (or end-of-day reflection commitments), check them against today's morning setup. Call out anything that was committed yesterday but isn't reflected today. Be direct — this is the accountability disposition from SOUL.md.

### What Needs Attention Today

Based on everything read: what is the single most important thing to work on right now? Be direct. Don't hedge. If a buried deadline (e.g., from an Activity Log `next_action`) conflicts with today's stated priority list, surface the conflict.

### Open Questions for Owner

Ask 1–3 specific questions to clarify priorities or unblock something. No more than 3.

---

**Keep this briefing short and direct. The goal is clarity, not comprehensiveness.**
