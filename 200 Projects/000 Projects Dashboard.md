---
type: dashboard
status: active
date: 2026-01-01
tags: [type/dashboard]
---

# Projects Dashboard

> **The single source of truth for everything you're actively building.**
> Updated at the weekly review. If it's not here, it doesn't exist.

---

## Active Projects

> Requires the [Dataview](https://blacksmithgu.github.io/obsidian-dataview/) plugin. Without it, the block below renders as code — harmless, and the manual list further down still works.

```dataview
TABLE 
  status as "Status",
  next_action as "Next Action",
  deadline as "Deadline",
  energy as "Energy"
FROM "200 Projects"
WHERE type = "project" AND status != "archived" AND status != "completed" AND status != "dormant"
SORT date DESC
```

---

## Blocked / Waiting

```dataview
LIST
FROM "200 Projects"
WHERE status = "waiting" OR status = "blocked"
```

---

## Accountability Check

> Ask Claude: *"Check my projects dashboard and hold me accountable. What have I been avoiding? What needs to move today?"*

**Last reviewed**: —
**Next review**: —

---

## Ongoing Areas

*Ongoing responsibilities with no end date. Link each one's hub note here. Check these at reviews, not daily — Areas degrade slowly, so watching them closely mostly produces noise.*

---

## Active Projects (Manual)

> The Dataview tables above are generated. This section is written by hand, and it is the one that carries **judgment** — priority order, why something is paused, what would bring it back.
>
> `/onboard` seeds this from your setup interview. `/wrap-week` keeps it honest.

*State the current priority order here, with a date. Something like:*

> **Priority order (as of YYYY-MM-DD):** Project A first, then B. Everything else is dormant until A ships.

### Example entry — replace with your own

**What it is**: One line. What the project is and why it exists.
**Phase**: Where it actually is right now — not where you hoped it would be.
**Next action**: The single next physical action. Canonically this lives in the project's Activity Log; point here rather than duplicating, so there's only one place to go stale.
**Deadline**: A real date, or none. An invented deadline you don't believe teaches you to ignore all of them.
**Link**: `[[<Project> Project Hub]]`

---

## Dormant / Parked

> Projects that aren't dead but aren't moving. **Say why each one is parked and what would bring it back** — "waiting on the client to respond" and "I lost interest" are both fine, and they mean very different things when you reread this in six months.

---

## Recently Completed

```dataview
LIST
FROM "200 Projects"
WHERE status = "completed"
SORT date DESC
LIMIT 5
```

---

## The Hard Questions (weekly)

Run through these at every weekly review:

1. What project am I avoiding, and why?
2. What is the one thing that would make the biggest difference this week?
3. Am I working on the most important thing, or just the most comfortable thing?
4. What needs to die or be archived because it's no longer a priority?
