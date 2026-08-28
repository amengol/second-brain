# CLAUDE.md — AI Contract for This Vault

This file is the operating agreement between this vault and any AI collaborator (Claude Code, Cursor, Claude Desktop, etc.). Read it before touching anything.

Identity, voice, and boundaries live in `SOUL.md`. The owner's profile and project facts live in `USER.md`. Durable decisions and lessons live in `MEMORY.md`. This file holds the contract and the vault mechanics.

> **First time in this vault?** If `000 Meta/Vault Setup.md` does not exist, this vault has not been set up yet. Suggest `/onboard` — a short interview that personalizes `SOUL.md`, `USER.md`, this file, and the Projects Dashboard. Suggest it once; don't insist. The shipped defaults are valid working configuration, so someone exploring the vault before committing to it should not be blocked.

@SOUL.md
@USER.md

---

## Vault Structure

The vault uses a numbered PARA-inspired system:

```
000 Meta/          → Vault conventions, templates
100 Inbox/         → Brain dumps, quick captures — process weekly
200 Projects/      → Active work with defined outcomes and deadlines
300 Areas/         → Ongoing responsibilities (no end date)
400 Resources/     → Reference material, curated knowledge
500 Knowledge/     → Learning notes, deep dives, concepts
600 Media/         → Books, podcasts, videos, courses
700 Meetings/      → Meeting notes (one folder per date)
800 Journal/       → Daily notes, reflections, morning pages
900 Archive/       → Completed, dormant, or reference-only material
```

---

## Plan Organization

Implementation plans for vault projects live under `.agents/plans/` with a 3-folder lifecycle (`0-active/`, `1-done/`, `2-deprecated/`). Top-level plan filenames carry a `YYYY-MM-DD-` start-date prefix for chronological sort. Sub-phase batches live in a sibling folder next to their parent plan; their progress is tracked live in `<parent>/00-manifest.md`. The full convention — filenames, status blockquotes, command behaviors — is in the README below, loaded into every session via the `@`-import.

@.agents/plans/README.md

---

## Conventions

### Wikilinks
- Always use `[[wikilinks]]` for internal cross-references, never bare filenames.
- Every new note should link to at least 2 existing notes (the "2-link rule").

### Frontmatter
All notes require frontmatter. Minimum required fields:

```yaml
---
type: note | project | daily | meeting | resource | template
status: active | in-progress | waiting | completed | archived
date: YYYY-MM-DD
tags: []
---
```

Project notes also require:
```yaml
---
type: project
status: active
date: YYYY-MM-DD
tags: []
next_action: "What is the very next physical action?"
deadline: YYYY-MM-DD
energy: high | medium | low
---
```

### Note Naming
- Daily notes: `YYYY-MM-DD.md` inside `800 Journal/`
- Meeting notes: `YYYY-MM-DD / Meeting Title.md` inside `700 Meetings/`
- Project notes: Descriptive kebab-case names inside the project folder
- No spaces in filenames — use hyphens

### Tags
- Use `#project/[name]` for project-specific tags
- Use `#area/[name]` for area tags
- Use `#status/active`, `#status/waiting`, `#status/done`
- Use `#type/idea`, `#type/decision`, `#type/problem`

---

## Accountability System

This is CRITICAL. The vault contains a weekly review template and a Projects Dashboard. When the owner asks you to check in on them or review their progress:

1. Read `200 Projects/000 Projects Dashboard.md` first.
2. Read the most recent daily note in `800 Journal/`.
3. Read all notes tagged `#status/waiting` or `#status/blocked`.
4. Ask specifically about:
   - What progress was made on the `next_action` field of each active project?
   - What got stuck and why?
   - What is the single most important thing to do next?

The project's `next_action` — in its Activity Log, or its PRD if it has one — is the canonical source of truth for "what's next on this project". Any skill that changes a plan's lifecycle state (`/plan-feature`, `/plan-sub-phases`, `/execute`) MUST also bump the matching project's `next_action` in the same commit. A stale `next_action` is a bug, not just drift — flag it the moment you notice.

(The *disposition* for this — pushing back, never letting the owner off the hook — lives in `SOUL.md`.)

---

## Brain Dump Protocol

When the owner says "brain dump" or "let me think out loud":
1. Create a new note in `100 Inbox/` with today's date as prefix.
2. Capture everything they say with minimal formatting.
3. At the end, ask: "Do you want me to extract action items, project connections, or ideas from this?"
4. When processing the inbox, suggest where each item belongs in PARA.

---

## Session Context

`MEMORY.md`, the Projects Dashboard (`200 Projects/000 Projects Dashboard.md`), and the most recent daily notes (`800 Journal/`) are the *current state*. Once the **SessionStart hook** is in place it will inject these automatically; until then, read them at the start of a working session.
