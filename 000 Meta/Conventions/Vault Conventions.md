---
type: meta
status: active
date: 2026-03-23
tags: [type/meta]
---

# Vault Conventions

> The rules of this vault. Read before creating anything.

---

## Folder Structure

| Folder | Purpose | Examples |
|--------|---------|---------|
| `000 Meta/` | Vault rules, templates, this file | CLAUDE.md, Templates |
| `100 Inbox/` | Brain dumps, quick captures | Anything unprocessed |
| `200 Projects/` | Active work with clear outcomes | A product build, a client engagement |
| `300 Areas/` | Ongoing responsibilities | Marketing, Engineering |
| `400 Resources/` | Reference material | Tools, frameworks |
| `500 Knowledge/` | Learning notes, concepts | Book notes, research |
| `600 Media/` | Books, podcasts, videos | Reading list |
| `700 Meetings/` | All meeting notes | One folder per date |
| `800 Journal/` | Daily notes, reflections | 2026-03-23.md |
| `900 Archive/` | Completed / inactive material | OpenClaw Study |

---

## Required Frontmatter

Every note must have at minimum:

```yaml
---
type: [see types below]
status: [see statuses below]
date: YYYY-MM-DD
tags: []
---
```

### Types
- `note` — general note
- `project` — active project hub
- `daily` — daily journal entry
- `weekly-review` — weekly review
- `meeting` — meeting note
- `brain-dump` — unstructured dump from Inbox
- `resource` — reference material
- `template` — note template (lives in `000 Meta/Templates/`)
- `meta` — vault configuration and conventions
- `dashboard` — aggregated view (uses Dataview)

### Statuses
- `active` — currently in use
- `in-progress` — being worked on right now
- `waiting` — blocked on something external
- `completed` — done
- `archived` — no longer active, kept for reference

---

## File Naming

| Type | Format | Example |
|------|--------|---------|
| Daily note | `YYYY-MM-DD.md` | `2026-03-23.md` |
| Meeting note | `YYYY-MM-DD - Title.md` | `2026-03-23 - Project Kickoff.md` |
| Project hub | `[Project Name] Project Hub.md` | `Website Redesign Project Hub.md` |
| Regular note | `kebab-case-title.md` | `meta-pixel-setup.md` |
| Brain dump | `YYYY-MM-DD - Brain Dump.md` | `2026-03-23 - Brain Dump.md` |

**Rule**: No spaces in filenames (use hyphens). Exception: meeting notes and daily notes.

---

## Linking Rules

1. **Every new note links to at least 2 existing notes** (the "2-link rule")
2. Use `[[wikilinks]]` for internal references — never copy-paste content
3. Use `[[Note Title|Display Text]]` for custom link labels
4. Use `![[filename]]` to embed notes within notes

---

## Tagging Strategy

```
#project/website-redesign  → Project-specific
#project/newguy-io
#area/marketing
#area/engineering
#status/active
#status/waiting
#status/blocked
#type/idea
#type/decision
#type/problem
#type/resource
```

---

## Processing Inbox

Run weekly (every Sunday). For each note in `100 Inbox/`:

1. **Delete** — if no longer relevant
2. **Archive** → `900 Archive/` — if done but worth keeping
3. **Elaborate** → expand, add frontmatter, move to correct PARA folder

Target: Inbox empty by end of Sunday review.

---

## The 2-Minute Rule

If a note can be processed, linked, and filed in under 2 minutes — do it now, not later.

---

## Synced Meeting Notes

If you use a meeting-transcription tool that syncs into `700 Meetings/` (Granola, Otter, and others have Obsidian integrations), tag those notes `#type/meeting` and **do not rename them manually** — let the plugin manage its own files, or the next sync will duplicate them.

Without such a tool, write meeting notes by hand from the `Meeting Note` template. Capture what was decided and who owes what by when; the rest is optional.

After a meeting is synced:
1. Add relevant frontmatter (`project:` field)
2. Extract action items to the relevant project hub
3. Link to the project hub with a wikilink
