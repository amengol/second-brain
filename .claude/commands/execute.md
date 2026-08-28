---
description: Execute an implementation plan
argument-hint: [path-to-plan]
---

# Execute: Implement from Plan

## Plan to Execute

Read plan file: `$ARGUMENTS`

## Execution Instructions

### 1. Read and Understand

- Read the ENTIRE plan carefully
- Understand all tasks and their dependencies
- Note the validation commands to run
- Review the testing strategy

### 2. Execute Tasks in Order

For EACH task in "Step by Step Tasks":

#### a. Navigate to the task
- Identify the file and action required
- Read existing related files if modifying

#### b. Implement the task
- Follow the detailed specifications exactly
- Maintain consistency with existing code patterns
- Include proper type hints and documentation
- Add structured logging where appropriate

#### c. Verify as you go
- After each file change, check syntax
- Ensure imports are correct
- Verify types are properly defined

### 3. Implement Testing Strategy

After completing implementation tasks:

- Create all test files specified in the plan
- Implement all test cases mentioned
- Follow the testing approach outlined
- Ensure tests cover edge cases

### 4. Run Validation Commands

Execute ALL validation commands from the plan in order:

```bash
# Run each command exactly as specified in plan
```

If any command fails:
- Fix the issue
- Re-run the command
- Continue only when it passes

### 5. Final Verification

Before completing:

- ✅ All tasks from plan completed
- ✅ All tests created and passing
- ✅ All validation commands pass
- ✅ Code follows project conventions
- ✅ Documentation added/updated as needed

### 5.5. If the plan can't complete (blocked)

Sometimes execution genuinely can't finish — a dependency is missing, an upstream service is down, the design has a flaw that needs revisiting. Don't pretend to complete a plan you couldn't.

When you must stop:

1. Prepend `> **Status: BLOCKED** — <one-line reason>` to the plan file (replace any existing status note).
2. Below the blockquote, add a short paragraph describing what would unblock it (e.g. "Waiting on the Stripe API key from the owner", "Upstream bug — issue #XYZ", "Needs design decision: see open question N").
3. For sub-phase plans, also update the parent's `00-manifest.md` Status column for this sub-phase from `pending`/`in progress` to `blocked`.
4. **Do not move the file.** It stays in `0-active/` until either unblocked (status removed → resume by re-running `/execute`) or formally abandoned (`> Status: DEPRECATED` + `git mv` to `2-deprecated/`).
5. Stage the edits and tell the user the plan is blocked, why, and what would unblock it. Skip the remaining steps below.

### 6. Update Status and Move Plan to `1-done/`

Plans live in lifecycle folders under `.agents/plans/` — `0-active/`, `1-done/`, `2-deprecated/`. The folder communicates broad status; the status blockquote inside each file gives the fine signal; for sub-phase batches, the parent's `00-manifest.md` Status column is the live source of truth. See `.agents/plans/README.md`.

Classify the plan being executed by its path and contents:

- **Sub-phase plan** — path matches `.agents/plans/<lifecycle>/<anything>/<NN>-*.md` (e.g. `.agents/plans/0-active/2026-05-23-phase-1-daily-memory-reflection/03-launchd-scheduling.md`). The test is "this file lives inside a sibling folder of a parent `.md` AND its basename starts with `<NN>-`". The parent folder name itself can be anything — date-prefixed (vault convention) or not (legacy / pre-migration repos).
- **Named-phase plan** — plan title or body explicitly completes a named phase (e.g. "Phase 1 — Daily memory reflection") that appears under the `## 12. Implementation Phases` section of a PRD at `200 Projects/<Project>/PRD.md`.
- **Generic plan** — neither of the above (a standalone feature/bug/refactor plan).

#### Sub-phase plan

Update the plan file, the parent's manifest, and the parent project's PRD `next_action`. **Do NOT move the file.**

**a. The sub-phase plan file itself:**
- Prepend a `> **Status: COMPLETE** — implemented <YYYY-MM-DD>` blockquote on the first line after the title, or replace any existing status note in the header.

**b. The parent manifest** at `<parent-folder>/00-manifest.md`:
- In the "Execution Order" table, find the row matching this sub-phase's `NN`.
- Update the Status column from `pending` (or `in progress`) to `complete`.

**c. The parent project's PRD** (locate via `200 Projects/*/PRD.md` whose `## 12. Implementation Phases` (or equivalent) section names the phase this sub-phase belongs to — typically derivable from the parent plan's basename, e.g. `2026-05-23-phase-1-daily-memory-reflection` → "Phase 1 — Daily memory reflection"):
- Read the parent manifest's "Execution Order" table to find the next sub-phase.
- If a `pending` sub-phase still follows this one: update PRD frontmatter `next_action` to `"Execute Sub-Phase NN — <name>"` (use the next row's `NN` and human-readable name, suffixed with a brief scope hint if it fits within ~150 chars).
- If this was the final sub-phase in the manifest: update PRD frontmatter `next_action` to `"Execute parent plan via /execute to mark Phase X complete"` (substitute the actual phase number).
- If no matching PRD is found, skip this step silently — generic plans without a parent project don't have a PRD to update.
- Use `Edit` to change only the `next_action:` line; do not rewrite the whole frontmatter.

Sub-phase files stay inside their parent's folder. The whole parent (plan + sub-phase folder) moves to `1-done/` only when the parent plan itself is executed and marked complete (the "Named-phase plan" or "Generic plan" branch below).

Stage all three edits so they land in the same commit as the implementation.

#### Named-phase plan

Update **all three** of the following:

**a. The plan file itself** (the file passed to `/execute`):
- Prepend a `> **Status: COMPLETE** — implemented <YYYY-MM-DD>` blockquote on the first line after the title, or replace any existing status note in the header.

**b. The parent PRD** (locate by scanning `200 Projects/*/PRD.md` for an `### Phase` heading matching the plan's phase name):
- Find the matching phase section (e.g. `### Phase 1 — Close the Curation Loop (MVP)`).
- Insert or replace a `> **Status: COMPLETE** — implemented <YYYY-MM-DD>` blockquote immediately under that phase's heading.
- Also update the PRD's frontmatter `next_action:` field to point at the next phase if one exists, or set `status: completed` if this was the final phase.

**c. The plan file location** — `git mv` the plan, and its sibling sub-phase folder if one exists with the same basename, to `1-done/`:

```bash
# Plan file itself:
git mv .agents/plans/<current-lifecycle>/<name>.md .agents/plans/1-done/<name>.md

# If a sibling sub-phase folder exists (same basename, no .md), move it too:
git mv .agents/plans/<current-lifecycle>/<name>/ .agents/plans/1-done/<name>/
```

Stage all doc updates and include them in the same commit as the implementation.

#### Generic plan

Update the plan file and move it:

- Prepend a `> **Status: COMPLETE** — implemented <YYYY-MM-DD>` blockquote.
- `git mv` the plan (and sibling sub-phase folder if present) from its current lifecycle folder to `1-done/`, same as step (c) above.

Stage everything for the same commit.

### 7. Final hand-off

**STOP. Do not invoke `/commit` yourself.** Report the changes as staged and ready, then tell the user to run `/commit` when they're ready to review and create the commit.

Do not invoke any commit skill, do not run `git commit` directly, and do not pre-stage the commit message — `/commit` will draft and present it.

## Output Report

Provide summary:

### Completed Tasks
- List of all tasks completed
- Files created (with paths)
- Files modified (with paths)

### Tests Added
- Test files created
- Test cases implemented
- Test results

### Validation Results
```bash
# Output from each validation command
```

### Ready for Commit
- Confirm all changes are complete
- Confirm all validations pass
- Suggest the user run `/commit` when ready. Do not run it.

## Notes

- If you encounter issues not addressed in the plan, document them
- If you need to deviate from the plan, explain why
- If tests fail, fix implementation until they pass
- Don't skip validation steps
