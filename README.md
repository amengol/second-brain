# Second Brain Template

> A personal knowledge management system for Obsidian, driven by AI through Claude Code.
> Clone it, run `/onboard`, and you have a working second brain configured around how *you* work.

---

## What this is

Most "second brain" templates give you empty folders and a naming convention. The folders are the easy part. What actually makes a vault useful is an **operating agreement** — a written contract telling the AI who you are, what you're carrying, how blunt to be with you, and what it must never do.

This template ships that contract, the commands that run on it, and an installer that fills it in by interviewing you:

- **`CLAUDE.md`** — the vault contract: conventions, accountability protocol, plan lifecycle
- **`SOUL.md`** — disposition and hard boundaries. Direct, accountability-first, coach-not-cheerleader
- **`USER.md`** — who you are, what you're carrying, which reviews you'll actually do
- **Ten commands** — a daily and weekly loop, plus a plan → execute pipeline
- **Three hooks** — session context injection and automatic session capture

It is opinionated on purpose. A neutral assistant produces a neutral vault.

## Setup

**1. Clone this repo** and open the folder as a vault in [Obsidian](https://obsidian.md).

**2. Install the community plugins** (Settings → Community plugins). The vault ships pre-configured for all of these, so installing them is all that's needed. Only the first two are load-bearing:

| | Plugin | Why |
|---|---|---|
| **Required** | [Dataview](https://blacksmithgu.github.io/obsidian-dataview/) | The Projects Dashboard runs three queries. Without it they render as inert code blocks and half the dashboard is dead |
| **Required** | [Templater](https://silentvoid13.github.io/Templater/) | Fills the date fields in new daily notes. Already wired to `800 Journal/`. Skip it and every daily note starts with manual date entry — which is exactly the friction that kills the habit |
| **Recommended** | [Calendar](https://github.com/liamcain/obsidian-calendar-plugin) | Click a date, get that daily note. High value in a journal-centric vault, zero cost |
| **Recommended** | [Periodic Notes](https://github.com/liamcain/obsidian-periodic-notes) | Weekly review files named `YYYY-Www`, so `/wrap-week` output lands in the right place automatically |
| **Optional** | [Obsidian Git](https://github.com/Vinzent03/obsidian-git) | Auto-backup from inside Obsidian — useful because journals get written without Claude Code open. Needs auth setup; `/commit` already covers the Claude-side path |

Obsidian's **Daily Notes** core plugin is already enabled and pointed at `800 Journal/` with the shipped template.

> **If you plan to use this on a phone:** Obsidian Git has poor mobile support. Mobile sync is a separate problem — Obsidian Sync, iCloud, or Dropbox — and worth solving before you build a habit around it.

**3. Open the same folder in [Claude Code](https://claude.com/claude-code).**

**4. Run `/onboard`.** It interviews you — who you are, what you're working on, how direct you want the assistant to be, which review cadences you'll genuinely keep — then rewrites `SOUL.md`, `USER.md`, `CLAUDE.md`, and the Projects Dashboard from your answers, and seeds a folder per project.

Nothing is written until you approve a list of files. Run `/onboard amend` any time to change your setup.

**Before onboarding, the vault already works.** The shipped defaults are real working configuration, not placeholders — so you can look around first and commit later.

## Vault structure

```
000 Meta/          → Conventions, templates, your setup record
100 Inbox/         → Brain dumps and quick captures — process weekly
200 Projects/      → Active work with defined outcomes
300 Areas/         → Ongoing responsibilities (no end date)
400 Resources/     → Reference material you collected
500 Knowledge/     → Understanding you wrote
600 Media/         → Books, podcasts, videos, courses
700 Meetings/      → Meeting notes, one folder per date
800 Journal/       → Daily notes and weekly reviews
900 Archive/       → Completed, dormant, or reference-only
```

PARA, with numbered prefixes so the folders sort in a sensible order instead of alphabetically. Each folder has a `README.md` explaining what belongs in it.

## Commands

| Command | What it does |
|---|---|
| `/onboard` | Interviews you and configures the vault. Run this first; `/onboard amend` to change it later |
| `/prime` | Loads full vault state and gives an accountability briefing. Run at the start of a session |
| `/wrap-day` | End of day: checks the morning's priorities against what actually moved, proposes reflections |
| `/wrap-week` | Weekly review: accountability across the week, inbox audit, stale `next_action` audit |
| `/fold-in` | Folds a session's substance into today's journal and any project logs it touched |
| `/create-prd` | Turns a conversation into a Product Requirements Document |
| `/plan-feature` | Deep-analysis implementation plan for a piece of work |
| `/plan-sub-phases` | Decomposes a large plan into independently executable sub-phases |
| `/execute` | Executes a plan and moves it through its lifecycle |
| `/commit` | Commits the vault with a composed message |

## The daily loop

The folders are storage. **This is the part that makes it work:**

- **Morning, 5 minutes** — open today's note. How you feel, three priorities, what needs attention.
- **During the day** — capture into the Progress Log or the Inbox. Don't organize; just capture.
- **Evening, 5 minutes** — `/wrap-day`. It checks your stated priorities against what actually happened and won't let you quietly reframe a miss as a win.
- **Weekly, 30 minutes** — `/wrap-week`. Empty the inbox, review every project, fix stale `next_action` fields.

Miss a day and nothing breaks. Miss three weeks and you'll find you can't remember what you decided or why — which is the exact problem the vault exists to solve.

## Under the hood

**Hooks** (`.claude/hooks/`, wired in `.claude/settings.json`) — these need a working Python 3 on your PATH:

- **SessionStart** injects `MEMORY.md`, the Projects Dashboard, and your most recent daily note into every new session, so Claude already knows where things stand without you running `/prime`.
- **SessionEnd / PreCompact** appends a capture of the session's prompts and edited files to today's daily note, under its own `## Session Captures (auto)` heading so it never clobbers your writing.

Both are read-mostly, make no network calls, and cost no tokens to produce. `/onboard` will offer to disable them.

**Plans** (`.agents/plans/`) — `/plan-feature`, `/plan-sub-phases`, and `/execute` write implementation plans through a three-stage lifecycle: `0-active/` → `1-done/` or `2-deprecated/`. See `.agents/plans/README.md` for the conventions.

**Conventions** (`000 Meta/Conventions/`) — frontmatter fields, `type` and `status` enums, file naming, and linking rules. Worth reading once.

## A note on privacy

A second brain accumulates genuinely personal material — money, health, employment, family, unfinished thoughts about people you know. That is what makes it valuable and what makes it sensitive.

**Keep the repository private.** If you sync it to a git host, check the visibility setting before your first push, not after. Keep credentials out of it entirely — API keys, account numbers, and passwords belong in a password manager, never in a note.

If you're using this for work under confidentiality obligations, tell `/onboard` during setup — it records what may and may not be written down, and a work vault should never be pushed to a personal remote.

## Requirements

- [Obsidian](https://obsidian.md) — free
- [Claude Code](https://claude.com/claude-code)
- Python 3 — only if you keep the hooks
- Git — only if you want history and sync across machines

## License

MIT — see [LICENSE](LICENSE).
