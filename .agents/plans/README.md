# `.agents/plans/`

Implementation plans, organized by lifecycle stage. The folder tells you broad status; the **status blockquote** inside the file gives the fine signal; for sub-phase batches, the parent's `00-manifest.md` **Status column** is the live source of truth.

## Layout

| Folder | Meaning |
|---|---|
| `0-active/` | Plans not yet shipped — drafted by `/plan-feature` and/or in-flight. In-flight vs. just-drafted is distinguished by the status blockquote inside the file (and, for sub-phase batches, by the manifest). |
| `1-done/` | Plans completed by `/execute`. The command `git mv`s them here on completion. |
| `2-deprecated/` | Plans abandoned or superseded. Move manually with a `> **Status: DEPRECATED** — <reason>` blockquote prepended. |

Numeric prefixes (`0-`, `1-`, `2-`) sort the lifecycle stages naturally instead of alphabetically.

## Filename conventions

- **Top-level plans:** `<YYYY-MM-DD>-<kebab-case-name>.md`
  - Date prefix = the plan's **start date** (when `/plan-feature` is invoked). ISO 8601 so files sort chronologically in `ls`.
  - The filename does **not** change as the plan moves between lifecycle folders. The completion date is captured separately in the status blockquote inside the file.
  - Examples: `2026-05-23-phase-1-daily-memory-reflection.md`, `2026-06-01-add-search-api.md`.
- **Sub-phase files:** `<NN>-<kebab-case-name>.md` — two-digit zero-padded sequence number for execution order. `00-manifest.md` is always the manifest.
  - No date prefix at the sub-phase level. Sequence already encodes order, and the parent plan's date prefix conveys when the whole batch was created.
  - Examples: `00-manifest.md`, `01-scaffolding.md`, `02-launchd-job.md`.

## Structure conventions

- **Sub-phase folders** share the parent plan's full basename. A parent at `2026-05-23-phase-1.md` has its sub-phases in a sibling folder `2026-05-23-phase-1/` containing `00-manifest.md` + `01-*.md`, `02-*.md`, etc.
- **Sub-phases stay put** through their entire lifecycle. The parent's `.md` file + sibling sub-phase folder move together to `1-done/` only when the parent plan itself is marked complete.
- **All moves use `git mv`** so history is preserved.

## Status conventions

The first line after a plan's title can carry a status blockquote. `/execute` writes these; `/plan-feature` and `/plan-sub-phases` don't.

| Blockquote | Meaning |
|---|---|
| (none) | Pending (just drafted) or in-flight (work started, not yet complete). Folder location says it's still active; the manifest disambiguates sub-phase progress. |
| `> **Status: COMPLETE** — implemented <YYYY-MM-DD>` | Done. For top-level plans, `/execute` also `git mv`s the file to `1-done/` after writing this. |
| `> **Status: BLOCKED** — <one-line reason>` | Execution stopped on an external dependency or unresolved decision. The file stays in `0-active/`. The paragraph below the blockquote explains what would unblock it. Resume by removing the blockquote and re-running `/execute`. |
| `> **Status: DEPRECATED** — <reason>` | Abandoned. Pair with a manual `git mv` to `2-deprecated/`. |

For sub-phase batches, the parent's `00-manifest.md` Execution Order table has a Status column per sub-phase. Reading the manifest is the fast way to see "3 of 8 done, 1 blocked, 4 pending" without opening each sub-phase file.

## Commands that touch this directory

- **`/plan-feature <name>`** → creates `0-active/<YYYY-MM-DD>-<name>.md`.
- **`/plan-sub-phases <plan-path>`** → creates `<lifecycle>/<parent>/00-manifest.md` (with a Status column initialized to `pending` per sub-phase) + sub-phase files alongside the parent plan, in whatever lifecycle folder the parent currently sits in.
- **`/execute <plan-path>`** → updates the plan's status blockquote. For sub-phase plans, also updates the parent manifest's Status column. For top-level plans, `git mv`s the plan + sibling sub-phase folder to `1-done/` on completion. Sub-phase plans stay in place.

## Example state

```
.agents/plans/
├── 0-active/
│   ├── 2026-05-23-phase-1-daily-memory-reflection.md
│   ├── 2026-05-23-phase-1-daily-memory-reflection/
│   │   ├── 00-manifest.md           ← Status column: 01=complete, 02=in progress, 03=pending
│   │   ├── 01-scaffolding.md        ← > **Status: COMPLETE** — implemented 2026-05-25
│   │   ├── 02-launchd-job.md        ← no blockquote (in progress per manifest)
│   │   └── 03-backfill-script.md    ← no blockquote
│   └── 2026-05-30-phase-2-notification-service.md
├── 1-done/
└── 2-deprecated/
```
