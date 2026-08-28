---
type: meta
status: active
date: 2026-01-01
tags: [type/meta]
---

# Onboarding Reference

> The archetype definitions `/onboard` works from. Read this alongside `.claude/commands/onboard.md` — the command owns the interview flow, this file owns *what changes* per archetype.

---

## The rule that governs everything below

**Focus shapes content and vocabulary. It never shapes the folder skeleton.**

The following are **constant across every archetype**, including "describe your own". Do not fork them, do not offer to drop them, do not "simplify" them for a particular kind of user:

- The ten numbered folders, in full
- `800 Journal/` — the daily note, morning pages, and the evening reflection
- The daily loop: morning priorities → progress log → `/wrap-day`
- The weekly review
- All nine commands
- The frontmatter contract and the `type` / `status` enums
- Everything in `SOUL.md` under "Hard boundaries"

The temptation is strongest with the **inside-a-company** archetype: it looks like it should drop the journal in favour of meeting notes and decision records. That is wrong. A vault used inside a company is still a *personal* system helping one person carry their own work, and in that exact setting the journal is the most-used part of it — it is where you find out whether your stated priorities and your actual week have quietly diverged.

What varies is what fills the folders, and the words used to describe it.

---

## Archetype 1 — Personal projects

**Who**: someone building things outside a job — side projects, a craft, learning, creative work, life admin. Possibly employed elsewhere, but the vault is not about that job.

| Dimension | Value |
|---|---|
| `SOUL.md` "My role" | "…the single source of truth for your projects, knowledge, ideas, and life." Emphasis on continuity across long gaps — side projects go quiet for weeks and the vault is what makes the gap survivable. |
| Vocabulary | *projects* |
| `200 Projects/` seeds | The things they're actually building. Cap at five. |
| `300 Areas/` starters | Health, Finances, Home, plus any craft they're maintaining |
| Cadences on by default | Daily, Weekly |
| Cadences to offer | Monthly, Quarterly |
| Dashboard framing | Priority order, and honesty about what's dormant. This archetype accumulates dormant projects faster than any other — make dormancy easy to declare and free of guilt. |

**Emphasis in `SOUL.md` "How to help"**: *when they're stuck* and *pattern detection*. Side projects die from drift, not from hard problems.

---

## Archetype 2 — Inside a company

**Who**: an employee using the vault for their own work — their tickets, their meetings, their commitments, their standing. Not a team wiki. Personal, and usually private.

| Dimension | Value |
|---|---|
| `SOUL.md` "My role" | "…the single source of truth for the work you're carrying." Emphasis on commitments made to other people and on not dropping threads across sprints. |
| Vocabulary | *workstreams* and *initiatives* alongside *projects*; *stakeholders* rather than *clients* |
| `200 Projects/` seeds | Current initiatives, plus recurring duties that behave like projects (an on-call rotation, a quarterly review they own) |
| `300 Areas/` starters | The domains they own, Career/Growth, Team |
| Cadences on by default | Daily, Weekly |
| Cadences to offer | Monthly (useful if their company runs monthly or quarterly cycles — align the vault's cadence to the company's) |
| Dashboard framing | Who is waiting on what. `#status/waiting` and `#status/blocked` matter far more here than in the other archetypes, because most delay is other people. |

**Emphasis in `SOUL.md` "How to help"**: *when they open a project* and the accountability protocol. This archetype's failure mode is a commitment made verbally in a meeting and never written down.

**Ask about confidentiality.** If their employer's work is under NDA or otherwise restricted, note it in `USER.md` as a standing constraint — what may be written down and what may not. Say plainly that the vault is only as private as where it is stored, and that a work vault should not be pushed to a personal public remote.

---

## Archetype 3 — Solo founder / freelance

**Who**: running their own thing. Clients, or a product, or both. The business itself is one of the projects.

| Dimension | Value |
|---|---|
| `SOUL.md` "My role" | "…the single source of truth for your business, your clients, and your own work." Emphasis on cash-flow honesty and on not letting unpaid work quietly displace paid work. |
| Vocabulary | *clients* and *engagements* alongside *projects* |
| `200 Projects/` seeds | One per live client or engagement, plus the business itself (marketing, ops, admin) |
| `300 Areas/` starters | Finances, Sales/Pipeline, Operations, plus their delivery domain |
| Cadences on by default | Daily, Weekly, Monthly |
| Cadences to offer | Quarterly — genuinely useful here, where killing a line of business is a real decision |
| Dashboard framing | Revenue-bearing first. Offer a written filter rule — something like *"demo-only or unpaid work moves to dormant unless it's paying or about to"* — and record the date it was set. |

**Emphasis in `SOUL.md` "How to help"**: *pattern detection* and honest pushback. This archetype's failure mode is a pipeline of warm-but-unpaid relationships that feel like progress.

---

## Archetype 4 — Describe your own

**Who**: anyone the three above don't fit — a student, a researcher, someone managing a household or a health situation, someone doing several of these at once.

Do **not** silently fall back to Archetype 1. Ask what they're carrying and what a good week looks like, then set the five dimensions above from their answer. If their description substantially matches one of the three, say so and offer it as a starting point they can adjust — that is faster than building from nothing, and it is honest.

Record in `000 Meta/Vault Setup.md` that the archetype is custom, along with the description in their own words. A future `/onboard` amend run needs it.

---

## Combinations

People are frequently more than one of these — an employee with side projects is the most common combination there is.

**Pick the primary archetype from where most of their attention goes**, then borrow specifics from the secondary. Do not try to merge two archetypes into an averaged one; that produces vocabulary that fits nobody. Record both in `Vault Setup.md`, primary first.

If work and personal life need to stay genuinely separate — different confidentiality rules, different devices, an employer that shouldn't see personal notes — say plainly that two vaults is a legitimate answer, and that this template can be cloned twice. Do not push someone into one vault because the tool prefers it.
