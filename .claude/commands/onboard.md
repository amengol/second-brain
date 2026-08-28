---
description: Set up this vault — a short interview that configures SOUL.md, USER.md, CLAUDE.md and your projects
argument-hint: [amend]
---

# onboard

Turn this template into **their** second brain.

You will interview the owner and then rewrite the vault's contract files from their answers. This is a conversation, not a form. The output is a vault that knows who they are, what they're carrying, and how blunt to be with them.

> **This command is the one sanctioned exception to `SOUL.md`'s "Do NOT create new files unless explicitly asked."** It creates and rewrites files by design — but only the files listed in the mapping table below, and only after the owner has approved a preview. Outside that list, the boundary still holds.

---

## Hard rules

- **One stage per turn.** Ask a stage, wait, then move on. A nine-question wall gets skimmed and answered badly, and the answers are the entire product.
- **Use `AskUserQuestion` wherever the answer set is closed.** Stages 3, 5, 6, 7 and 8 all have a known set of answers — present them as selectable options rather than making the owner type prose. It is faster, it shows them what the choices actually are, and it stops setup feeling like an interview.
  - The tool auto-adds an **"Other"** choice, so an owner can always type something custom. That is how the "describe your own" archetype is offered — you don't need a fourth option for it.
  - Max 4 options per question, max 4 questions per call. Batch questions that belong together (Stage 7's three mechanics questions are one call).
  - Use `multiSelect: true` where more than one answer is valid (Stage 6's cadences).
  - Use `preview` to show the owner what a choice actually *looks like* (Stage 5's voice samples). Previews are single-select only.
- **Use free text only where the answer is genuinely open** — their name, what they do, their constraints, their project names. Do not force those into options; a made-up list of "what kind of person are you" choices is worse than an open question.
- **Never ask what you can infer.** If they said "I contract for three clients," do not then ask whether they're a freelancer. Reflect the inference back instead: *"So — solo/freelance, three live engagements. Right?"*
- **Propose-first, write-on-approval.** Nothing is written until Stage 8 and the owner has approved the file list. If they paste back edited content, write that verbatim.
- **No fabrication.** Write down what they told you. Do not invent a project, a constraint, or a preference to make a section look complete. An empty section is honest.
- **Respect the blast radius** (below). `/onboard` writes contract and content files. It never edits the machinery.
- **Stoppable at any point.** If they abandon mid-interview, write nothing and do not create `000 Meta/Vault Setup.md`. A half-onboarded vault is worse than an un-onboarded one, because the defaults are valid and a partial rewrite is not.
- **Don't sell.** They already cloned the repo. Skip the pitch.
- **Do not ask about pronouns.** Write in second person — "you" — which is how these files read anyway, so third-person pronouns rarely arise. Where one is genuinely needed and none has been stated, use *they/them*. Never infer pronouns from a name. If the owner states a preference at any point, use it from then on and record it. Asking upfront is not required and reads as an interrogation during setup.

## Blast radius — what this command may write

**MAY write:** `SOUL.md` · `USER.md` · `CLAUDE.md` · `README.md` · `MEMORY.md` · `200 Projects/000 Projects Dashboard.md` · `200 Projects/<project>/` · `300 Areas/<area>/` · `800 Journal/<today>.md` · `000 Meta/Vault Setup.md` · `000 Meta/How To Use This Vault.md`

**MUST NEVER touch:** anything under `.claude/commands/` · `.claude/hooks/` · `.claude/settings.json` (one exception, Stage 7: removing hook entries if the owner declines hooks) · `000 Meta/Conventions/` · `000 Meta/Templates/` · `.agents/` · `.gitignore` · `.gitattributes` · `.obsidian/`

Those are the machinery the owner is receiving, not settings they are being asked about. Without this rule a helpful assistant "improves" the command files during setup and the vault silently diverges from the template on day one — which makes every future update a merge conflict.

---

## Stage 0 — Detect state

Read `000 Meta/Vault Setup.md`.

**If it does not exist** → first run. Continue to Stage 1.

**If it exists** → **amend mode**. Do not re-run the whole interview. Instead:
1. Show the current setup: archetype, name, projects, disposition, cadences, daily-note strategy.
2. Ask what they want to change.
3. Re-run only the stages that feed it, then jump to Stage 8.

If the owner passed `amend` as an argument but no setup file exists, tell them the vault hasn't been set up yet and offer the full run.

## Stage 1 — Orient

Three lines, no more:

- This takes about ten minutes and configures the vault around how they work.
- Nothing is written until they approve a list of files.
- Everything stays editable, and `/onboard amend` can change it later.

Then ask Stage 2's questions.

## Stage 2 — Identity

- What should the vault call them?
- What do they do? (One or two sentences — enough that an assistant reading `USER.md` alone understands their situation.)
- Anything standing that bounds their decisions — a full-time job, young kids, a second income, a health constraint, a hard weekly commitment. Explain *why* you're asking: an assistant that doesn't know these will confidently suggest things that were never possible.

## Stage 3 — Archetype

Read `000 Meta/Conventions/Onboarding Reference.md` first.

Ask with **`AskUserQuestion`** — header `Focus`, question *"What is this vault mainly for?"*, three options:

| Option | Description |
|---|---|
| Personal projects | Things you're building outside a job — side projects, a craft, learning |
| Inside a company | Your own work at a job — your tickets, meetings, and commitments |
| Solo founder / freelance | Clients, or a product, or both. The business is one of the projects |

The auto-added **"Other"** covers *describe your own* — handle that answer per the reference file, and do **not** silently fall back to personal-projects.

If Stage 2 already implied one, put it first and mark it `(Recommended)` so they confirm rather than choose blind.

Handle combinations as the reference file describes: pick a primary, borrow from the secondary, record both. If work and personal need to stay genuinely separate, say plainly that two vaults is a legitimate answer.

For **inside a company**, also ask about confidentiality — what may be written down and what may not. Record it in `USER.md` as a standing constraint, and say that a work vault should not be pushed to a personal public remote.

## Stage 4 — What they're carrying

Ask for the things they're actually carrying right now. For each: a name and one line on what it is.

**Cap it at five, and push back if they offer more.** Say why: a vault opened on day one with fifteen projects is abandoned by week two, and anything they haven't touched in a month is dormant, not active. Offer to record the rest as dormant — that is an honest signal, not a failure.

Ask which one matters most right now. That becomes the stated priority order on the Dashboard, with today's date on it.

## Stage 5 — Disposition

This sets how the assistant talks to them. **Show, don't describe.**

Ask with **`AskUserQuestion`** — header `Voice`, two options, each carrying a `preview` with the *same situation* written both ways so the difference is concrete:

**Option 1 — Direct (Recommended)** · preview:
```
Priority 2 wasn't touched. No evidence in the journal, the
activity logs, or git. That's the third day in a row —
what's the actual blocker?
```

**Option 2 — Supportive** · preview:
```
Priority 2 didn't get picked up today. Two of three moved,
which is a solid day. Worth a look at what keeps pushing
it down the list?
```

In the same call, ask a second question — header `Pushback`, *"Should the assistant push back when you say 'I'll do it later'?"* — options **Yes (Recommended)** / **No**.

Recommend Direct and say why in one line: a neutral assistant produces a neutral vault, and the accountability is the part people say they wanted six months in. Then take their answer without arguing — someone who knows they respond badly to bluntness is telling you something true about themselves.

## Stage 6 — Cadences

Ask with **`AskUserQuestion`**, two questions in one call:

1. Header `Cadences`, **`multiSelect: true`** — *"Which reviews will you genuinely do?"*
   Options: **Daily (5 min)** · **Weekly (30 min)** · **Monthly (1 hr)** · **Quarterly (2 hrs)**
2. Header `Review day` — *"Which day for the weekly review?"*
   Options: **Friday** · **Monday** · **Saturday** · **Sunday** — plus "Other" for anything else.

   Recommend by archetype rather than picking a house default: **Friday** for inside-a-company (closes the work week while it's still fresh, and protects the weekend), **Monday** for personal-projects and solo/freelance (sets the week rather than closing it). Say which you'd pick and why in one line, then let them choose.

Before asking, say the honest thing in one line: **a cadence they skip is worse than one they never claimed**, because it turns the vault into a record of their own non-compliance. If only daily and weekly survive, that is a complete and working setup — not a compromise.

Get a *specific* day. "Sometime on the weekend" is how the weekly review stops happening.

Then ask, as free text, about **protected time** — hours or days not available for work: a sabbath, family evenings, a standing commitment. Write it as a rule, not a preference, so the assistant reads a quiet weekend as designed rather than as slippage.

## Stage 7 — Mechanics

Three things the vault cannot do for itself. **Ask all three with one `AskUserQuestion` call**, then handle the follow-up work per the notes below.

| # | Header | Question | Options |
|---|---|---|---|
| 1 | `Daily notes` | How should today's daily note get created? | **Templater (Recommended)** · **Obsidian Daily Notes** · **Let Claude create it** |
| 2 | `Git` | Do you want version history and sync? | **Yes, with a remote** · **Local history only** · **No git** |
| 3 | `Hooks` | Keep the session hooks? | **Keep (Recommended)** · **Disable** |

Adjust option 1's recommendation based on what's actually installed — check for `.obsidian/plugins/templater-obsidian/` before recommending it. **Note that a plugin's `data.json` ships with the template but its code does not**, so a config file existing does not mean the plugin is installed.

Before the questions, check which community plugins are present under `.obsidian/plugins/` and tell them plainly what's missing, tiered:

- **Required — `dataview`, `templater-obsidian`.** Without Dataview the Projects Dashboard's three queries render as inert code blocks. Without Templater every daily note starts with manual date entry.
- **Recommended — `calendar`, `periodic-notes`.** Date navigation, and weekly review files named correctly.
- **Optional — `obsidian-git`.** Auto-backup from inside Obsidian.

Do not block setup on missing plugins — the vault works without them and they can install later. Just be specific about what each one costs them.

### 7a. Daily notes — do not skip this

**This is the most common silent failure.** The daily note is the spine of the whole system, and nothing in the repo creates it. If nothing does, `/wrap-day` refuses to run and every session capture lands in `100 Inbox/` instead — invisible until they wonder where their notes went.

Follow-up per answer:

- **Templater** → the template ships pre-wired: Templater's folder template maps `800 Journal/` to `000 Meta/Templates/Daily Note.md`, and Obsidian's Daily Notes core plugin points at the same pair. If the plugin isn't installed, link them to it. Confirm both are enabled, then **have them create today's note to prove it works.**
- **Obsidian Daily Notes** → the core plugin alone won't evaluate `<% tp.* %>`, so give them a Templater-free copy of the template with plain date placeholders.
- **Let Claude create it** → record `assistant-creates`. `/wrap-day` reads that value and will create the note from the template, filling the date fields itself.

**Whatever they choose, record it in `Vault Setup.md`.** `/wrap-day` and the flush hook both read that decision.

Do not reduce this to a link. Walk them through it, then verify a note actually appears.

### 7b. Git

If they chose a remote, walk them through creating it and check they can push.

**Say this plainly, once:** a second brain accumulates genuinely personal material — money, health, employment, family, half-formed thoughts about people they know. **Make the repository private, and check the visibility setting before the first push, not after.** Credentials belong in a password manager, never in a note.

### 7c. Hooks

Three hooks ship, wired in `.claude/settings.json`:

- **SessionStart** — injects `MEMORY.md`, the Dashboard, and the most recent daily note into every session
- **SessionEnd / PreCompact** — appends a capture of the session's prompts and edited files to today's daily note

They need a working Python 3 — verify one is on PATH before recommending Keep. They're the reason a fresh session already knows where things stand. If the owner chose **Disable**, remove those entries from `.claude/settings.json` — **the only machinery edit this command is permitted to make** — and note it in `Vault Setup.md`.

## Stage 8 — Preview and approve

List every file you're about to write, each with a one-line summary of the change. Group them: rewritten, created, seeded.

Then ask with **`AskUserQuestion`** — header `Ready?`, *"Write these files?"*, options **Write them** / **Change something first**. The auto-added "Other" lets them say exactly what to change.

**Do not write anything until they pick "Write them".** If they want changes, take them and re-show the list.

## Stage 9 — Write, then first run

Write the files per the mapping table. Then:

1. Create today's daily note (per the Stage 7a decision) and offer to fill in the morning priorities from Stage 4.
2. Write `000 Meta/Vault Setup.md` — the record of every answer, and how amend mode knows this vault is configured.
3. Write `000 Meta/How To Use This Vault.md` — the tailored guide (appendix below). **Written, not printed**: chat scrolls away, and this is the note they reread in week three when the habit wobbles.
4. Point at it in three lines — where the guide is, the one habit that matters, and `/onboard amend` to change anything.

Close by naming the habit, not the feature list: **five minutes in the morning, five at night.** Everything else in the vault is downstream of that.

---

## Mapping — which stage writes which file and section

This table is the contract. Do not write outside it.

| Stage | What it asks | Writes to | Which section |
|---|---|---|---|
| 2 Identity | Name, what they do, standing constraints | `USER.md` | `## Profile` |
| | | `SOUL.md` | `## My role` — the opening frame |
| 3 Archetype | Which of the four | `SOUL.md` | `## My role` framing + `## How to help` emphasis |
| | | `USER.md` | vocabulary throughout |
| | | `CLAUDE.md` | project-type language only — conventions untouched |
| 4 Commitments | 1–5 things they're carrying | `USER.md` | `## Active projects` table + `## Project context` |
| | | Dashboard | the manual active-projects section + priority order |
| | | `200 Projects/<name>/` | one Hub + Activity Log each, from `Project Note.md` |
| 5 Disposition | How direct; pushback on/off | `SOUL.md` | `## Disposition` + `## How to help` |
| 6 Cadences | Which reviews, which day, protected time | `USER.md` | `## Review cadences` |
| 7 Mechanics | Daily notes / git / hooks | `000 Meta/Vault Setup.md` | records each decision |
| | | `.claude/settings.json` | **only** if hooks are declined |
| 9 Finalize | — | `README.md` | whole file → their own vault README |
| | | `800 Journal/<today>.md` | the first daily note |
| | | `000 Meta/Vault Setup.md` | full record + completion date |
| | | `000 Meta/How To Use This Vault.md` | the tailored guide — see appendix |

**Two-way check before you finish:** every stage above maps to a row, and every section of `SOUL.md` and `USER.md` either has a stage feeding it or is generic by design. If a stage feeds nothing, cut it. If a section has no stage, you're missing a question.

---

## Writing the files — guidance

**Keep the voice.** `SOUL.md` and `USER.md` ship opinionated on purpose. Personalize them; do not neutralize them. A `SOUL.md` rewritten into corporate neutrality has lost the thing that makes this vault worth having.

**Write prose, not fields.** `USER.md`'s Profile is a paragraph about a person, not a form. Read what they told you back to them in their own register.

**Preserve every heading.** Other commands and the hooks read these files by section. Rewrite the contents, keep the structure.

**Seed projects properly.** Each gets a folder under `200 Projects/` with a Hub (from `000 Meta/Templates/Project Note.md`) and an Activity Log. Set `next_action` to a real next physical action, from their own words — not `"TBD"`. A vault that starts with five empty `next_action` fields has taught them on day one that the field is decorative.

**Two links minimum.** Per `CLAUDE.md`'s 2-link rule, every new note should link to at least two others.

**Date everything.** Use today's actual date in frontmatter and in the Dashboard's priority-order line.

---

## Appendix — `000 Meta/Vault Setup.md` format

Written at Stage 9. **This file must not exist in the template** — its absence is how Stage 0 detects a first run, and how `CLAUDE.md` knows to suggest `/onboard`.

Record preferences only. **Never put credentials, tokens, or account numbers here.** Add a `**Pronouns**:` line only if the owner volunteered one — do not create the field by asking.

```markdown
---
type: meta
status: active
date: <YYYY-MM-DD>
tags: [type/meta]
---

# Vault Setup

> Written by `/onboard` on <YYYY-MM-DD>. Run `/onboard amend` to change any of this.

## Owner
- **Name**: <what the vault calls them>
- **Context**: <one line from Stage 2>
- **Standing constraints**: <job, family, health, commitments — what bounds decisions>
- **Confidentiality**: <only if inside-a-company: what may and may not be written down>

## Archetype
- **Primary**: personal-projects | inside-a-company | solo-founder-freelance | custom
- **Secondary**: <if any, else none>
- **If custom**: <their description, in their own words>

## Disposition
- **Voice**: direct | supportive
- **Push back on "I'll do it later"**: yes | no

## Cadences
- **Active**: <e.g. daily, weekly>
- **Weekly review day**: <a specific day>
- **Protected time**: <e.g. "Sundays — not available for work" | none>

## Mechanics
- **Daily notes**: templater | core-daily-notes | assistant-creates
  *(Read by `/wrap-day` and the flush hook. If `assistant-creates`, the assistant may create today's note when missing — otherwise it must stop and say so.)*
- **Git**: remote configured | local only | none
- **Hooks**: enabled | disabled

## Projects seeded
- `<name>` — <one line>

## Amend history
- <YYYY-MM-DD> — initial setup
```

**Amend runs** append a dated line to Amend history and update the changed fields in place. Do not rewrite the whole file and do not lose earlier history.

---

## Appendix — `000 Meta/How To Use This Vault.md`

Written at Stage 9. **Tailored to their answers, not generic** — that is the entire reason it's written by the command rather than shipped in the repo. A guide that says *"your weekly review is Friday"* is worth more than one that says *"pick a review day."*

Do not restate the README. The README is the pre-onboarding document (what this is, how to install). This is the post-onboarding one: their rhythm, their commands, and what to do when they fall off.

Keep it under roughly 120 lines. A guide nobody rereads is the same as no guide.

```markdown
---
type: meta
status: active
date: <YYYY-MM-DD>
tags: [type/meta]
---

# How To Use This Vault

> Written for <name> by `/onboard` on <date>. Re-run `/onboard amend` if any of this stops fitting.

## Your rhythm

<Only the cadences they actually chose. If they picked daily + weekly, do not
mention monthly or quarterly at all — listing cadences they declined turns the
guide into a record of what they are not doing.>

**Every morning (5 min)** — open today's note in `800 Journal/`.
<Say concretely how it gets created, per their Stage 7a choice:
 templater → "Obsidian creates it when you open today's date in the Calendar"
 core-daily-notes → "use the Daily Note command"
 assistant-creates → "ask Claude to open today's note">
Fill three things: how you feel, your top priorities, what needs the most attention.

**During the day** — capture into the Progress Log or `100 Inbox/`. Don't organize; just capture.

**Every evening (5 min)** — run `/wrap-day`. It checks the morning's priorities
against what actually moved and proposes your reflections. It won't let you
quietly reframe a miss as a win — that's deliberate, and it's the part that makes
the rest work.

**Every <their chosen day> (30 min)** — run `/wrap-week`. Empty the inbox, review
every project, fix stale `next_action` fields.

<If they set protected time, state it here as a rule the assistant honours —
e.g. "Sundays are protected. Claude won't push work into them, and a quiet
Sunday reads as designed, not as slippage.">

## Your commands

<A short table. Lead with the three or four they will use daily; the plan →
execute pipeline goes last and gets one line, since most owners won't touch
it in week one.>

## Where things go

One line per folder they'll actually use early — Inbox, Projects, Journal.
Point at each folder's own `README.md` for the rest rather than repeating it.

**The one rule worth remembering:** a Project can be completed, an Area can only
be maintained. That's what decides which folder something belongs in.

## Your projects

<The projects seeded in Stage 4, each with its `next_action`. This doubles as
proof the vault already knows something real about their work.>

## When you fall off

You will. Everyone does.

**Missing a day costs nothing.** Open today's note and carry on — don't
backfill, and don't apologize to your own vault.

**Missing three weeks costs a lot** — not because of the gap, but because you
lose the thread of what you decided and why. If it happens, don't try to
reconstruct it. Run `/prime`, let it tell you where things actually stand, and
start from today.

The vault is not a streak. It's a place to put things down so you can pick them
back up.

## Changing any of this

`/onboard amend` — re-runs only the parts you want to change. Your setup record
is in `000 Meta/Vault Setup.md`.
```
