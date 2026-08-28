---
description: "Decompose a large implementation plan into focused, independently-executable sub-phase plans"
argument-hint: [path-to-large-plan]
---

# Decompose Plan Into Sub-Phases

## Input Plan: $ARGUMENTS

## Mission

Transform a large, monolithic implementation plan into multiple **focused sub-phase plans**, each
independently executable by an AI agent in a single session using `/execute`.

**Core Principle**: Every sub-phase plan must be **fully self-contained** — an execution agent must
succeed using ONLY the sub-phase plan file, with zero reference to the parent plan. Context must be
duplicated, not referenced.

**Key Philosophy**: Right-Sizing Over Completeness. A sub-phase that's too large defeats the
purpose. Each sub-phase should produce testable, runnable artifacts within one focused session (~3–8
atomic tasks).

---

## Decomposition Process

### Phase 1: Plan Ingestion

Read the full input plan at `$ARGUMENTS` and extract:

1. **Inventory**: List all phases, tasks, and their dependency relationships
2. **Artifacts**: Identify what each task creates or modifies
3. **Validation gates**: Identify points where progress can be independently verified (server
   starts, tests pass, commands succeed, UI renders)
4. **Size check**: Count total tasks; estimate target sub-phase count (target: 3–8 tasks each)

### Phase 2: Dependency Graph Analysis

Build an explicit dependency map:

- Which tasks **must complete** before others can start? (hard dependencies)
- Which tasks are **logically cohesive** even without hard dependencies? (natural groupings)
- What is the **minimum viable state** at the end of each potential boundary?

**Look for these natural boundary types:**

| Boundary Type | Example | Why it's a good split |
|---|---|---|
| Foundation complete | Config + DB engine exist | Everything else imports these |
| Schema locked | All DB models + migrations run | Services can start being built |
| Service layer running | Core API responds to requests | Frontend / agent can be built |
| Integration point | Agent loop wired to channels | End-to-end testable |
| User-facing complete | Dashboard renders live data | Manual smoke test possible |

**Anti-patterns to avoid:**

- Splitting mid-dependency: Task A creates a file that Task B in the same sub-phase imports — keep them together
- Orphaned tasks: a task that logically belongs with neither adjacent sub-phase — assign to the one that creates its dependencies
- Single-task sub-phases: too granular; merge with adjacent

### Phase 3: Sub-Phase Boundary Definition

For each identified sub-phase, define before writing anything:

```
Name:         <kebab-case-descriptive-name>
Scope:        Tasks <X.Y to X.Z> from parent plan
Prerequisites: What must exist before this sub-phase starts (files, DB state, running services)
Exit State:   What must be true at completion (specific and verifiable)
Gate Command: Single command that proves this sub-phase is done
```

**Sizing rules:**

- `< 3 tasks` → merge with adjacent sub-phase
- `3–8 tasks` → correct size ✓
- `9–12 tasks` → consider splitting; split if there's a clean internal boundary
- `> 12 tasks` → must split; find the natural midpoint

Apply this recursively. A parent plan phase marked "Medium" complexity might become 1 sub-phase.
A phase marked "High" or containing >8 tasks must become 2+ sub-phases.

### Phase 4: Sub-Phase Plan Generation

For each boundary defined in Phase 3, generate a complete plan file.

**Critical rule**: Each sub-phase plan must pass the "No Prior Knowledge Test" — an agent with
ZERO context about the project must be able to execute it using only the sub-phase plan. This means:

- **Duplicate patterns**: Copy all relevant patterns from the parent plan into the sub-phase plan.
  Do NOT write "see parent plan for patterns." Write the pattern.
- **Duplicate gotchas**: Copy all gotchas relevant to this sub-phase's tasks.
- **Duplicate imports**: Specify exact imports for every task.
- **Carry forward conventions**: Naming, logging, error handling — state them explicitly in each plan.

### Phase 5: Manifest Generation

Create `00-manifest.md` in the output directory showing all sub-phases, their dependencies, and
the sequential execution commands.

---

## Sub-Phase Plan Template

Use this template for every generated sub-phase plan file:

```markdown
# Sub-Phase <N>: <Descriptive Name>

> **Parent Plan**: `<path-to-parent-plan>`
> **Sub-Phase**: <N> of <M> total
> **Depends On**: [<list sub-phase names, or "none" if first>]
> **Estimated Complexity**: [Low / Medium / High]

The following plan is complete and self-contained. Validate all prerequisites before starting.
Pay close attention to import paths, model field names, and API signatures — they must be exact.

## Scope

<1–3 sentences describing exactly what this sub-phase builds and why it exists as a unit.>

## User Story

As a <role>
I want <goal achieved by this sub-phase>
So that <value it unlocks for subsequent work or the end user>

---

## PREREQUISITES

> **STOP. Verify ALL of the following before writing a single line of code.**
> If any prerequisite fails, complete that sub-phase first.

### Required Files

- [ ] `<file-path>` — <why it must exist>
- [ ] `<file-path>` — <why it must exist>

### Required Services (if applicable)

- [ ] PostgreSQL accessible — Verify: `<command>`
- [ ] Redis accessible — Verify: `<command>`

### Required Database State (if applicable)

- [ ] `<table/extension/migration>` exists — Verify: `<SQL or alembic command>`

### Prerequisite Verification Commands

```bash
# Run all of these — every command must succeed before starting
<verification commands>
```

---

## CONTEXT REFERENCES

### Relevant Codebase Files — MUST READ BEFORE IMPLEMENTING

<List only files relevant to THIS sub-phase's tasks>

- `path/to/file.py` (lines X–Y) — Why: <specific reason>
- `path/to/config.py` — Why: <specific reason>

### New Files to Create

<Files that will be created in this sub-phase only>

- `path/to/new_file.py` — <purpose>

### Relevant Documentation — READ BEFORE IMPLEMENTING

- [Library Docs](https://url#section)
  - Specific section: <section name>
  - Why: <why this is relevant to THIS sub-phase>

### Patterns to Follow

**Copy the relevant patterns from the parent plan verbatim here. Do NOT reference the parent plan.**

**Naming Conventions:**
<project-specific naming rules>

**Async Pattern:**
<async/await pattern with example>

**Logging Pattern:**
<structlog pattern with example>

**Error Handling:**
<error handling pattern with example>

**<Other relevant patterns for this sub-phase>:**
<pattern with example>

---

## IMPLEMENTATION PLAN

### Phase A: <logical grouping within this sub-phase>

<Description of this grouping>

**Tasks:**
- <task description>
- <task description>

### Phase B: <logical grouping within this sub-phase>

<Description of this grouping>

**Tasks:**
- <task description>

---

## STEP-BY-STEP TASKS

IMPORTANT: Execute every task in order, top to bottom. Each task is atomic and independently
testable. Do not proceed to the next task if the current task's VALIDATE command fails.

### {ACTION} `{target_file}`

- **IMPLEMENT**: <Specific, unambiguous implementation detail>
- **PATTERN**: <Reference to pattern above — copy the exact pattern here, not "see above">
- **IMPORTS**: <Exact import statements required>
- **GOTCHA**: <Known issue specific to this task>
- **VALIDATE**: `<executable command that confirms this task succeeded>`

<Repeat for all tasks in this sub-phase>

---

## TESTING STRATEGY

### Unit Tests

<Scope and test cases for THIS sub-phase only. Include the testing framework and fixture pattern.>

### Integration Tests (if applicable)

<Scope for THIS sub-phase only>

### Edge Cases

<Edge cases specific to THIS sub-phase's functionality>

---

## VALIDATION COMMANDS

Execute every command. Zero failures permitted before moving to the next sub-phase.

### Level 1: Syntax & Style
```bash
<lint/format commands for files created in this sub-phase>
```

### Level 2: Unit Tests
```bash
<unit test commands scoped to this sub-phase's new files>
```

### Level 3: Integration Tests
```bash
<integration test commands if applicable>
```

### Level 4: Manual Validation
```bash
<manual steps to verify the sub-phase's core deliverable works>
```

---

## ACCEPTANCE CRITERIA

- [ ] All tasks completed in order
- [ ] All validation commands pass with zero errors
- [ ] Unit tests pass with ≥80% coverage on new code
- [ ] No regressions in previously-passing tests
- [ ] <sub-phase-specific criterion 1>
- [ ] <sub-phase-specific criterion 2>
- [ ] Handoff state verified (see below)

---

## HANDOFF STATE

> What the next sub-phase can depend on after this one completes.
> The next sub-phase will verify this state using the command below before starting.

### Files Created/Modified

- `<file>` — <what it provides to subsequent sub-phases>
- `<file>` — <what it provides>

### Services / Database State

- <database tables/extensions that now exist>
- <services that are now configured>

### Handoff Verification Command

```bash
# The NEXT sub-phase runs this to confirm this sub-phase is complete.
# Must exit 0 on success.
<single command or short script that verifies the handoff state>
```

---

## COMPLETION CHECKLIST

- [ ] All tasks completed in dependency order
- [ ] Each task's VALIDATE command passed immediately after implementation
- [ ] All validation commands executed successfully
- [ ] Full test suite for this sub-phase passes
- [ ] No linting or type-checking errors
- [ ] Handoff verification command exits 0
- [ ] Ready to hand off to next sub-phase
```

---

## Output Format

**Directory**: Same lifecycle folder as the parent plan. The sub-phase folder is created **next to** the parent `.md` file, sharing its full basename (date prefix included).
(e.g., for parent at `.agents/plans/0-active/2026-05-23-phase-1-complete-implementation.md` → sub-phase folder at `.agents/plans/0-active/2026-05-23-phase-1-complete-implementation/`)

**Sub-phase files**: `<NN>-<kebab-case-name>.md` (zero-padded sequence number) — no date prefix at this level; sequence encodes execution order.
(e.g., `01-scaffolding-database.md`, `02-license-api-core.md`)

**Manifest**: `00-manifest.md` in the same directory. The manifest's Execution Order table includes a **Status column** per sub-phase, initialized to `pending`. `/execute` updates the Status column to `complete` (or `blocked`) as each sub-phase finishes — making the manifest the live source of truth for sub-phase progress.

**Lifecycle**: Sub-phase files stay in this folder for their entire lifecycle. Per-file status is tracked via a `> **Status: COMPLETE** — implemented <YYYY-MM-DD>` blockquote inside each file AND mirrored in the parent manifest's Status column. When the parent plan is marked complete by `/execute`, the parent `.md` and the entire sub-phase folder move together to `1-done/`. See `.agents/plans/README.md`.

---

## Manifest Template

```markdown
# Sub-Phase Manifest: <Parent Plan Name>

> **Generated from**: `<parent-plan-path>`
> **Total sub-phases**: N
> **Execute each with**: `/execute .agents/plans/<dir>/<NN>-<name>.md`

---

## Dependency Graph

<ASCII or table representation of dependencies>

Example:
01 → 02 → 04
          ↗
     03 ──
05 (independent, can start after 02)

---

## Execution Order

| # | Sub-Phase | File | Depends On | Gate Command | Status |
|---|---|---|---|---|---|
| 01 | <name> | `01-name.md` | — | `<verify command>` | pending |
| 02 | <name> | `02-name.md` | 01 | `<verify command>` | pending |
| 03 | <name> | `03-name.md` | 01 | `<verify command>` | pending |
| 04 | <name> | `04-name.md` | 02, 03 | `<verify command>` | pending |

> **Status column** is the live source of truth for sub-phase progress. `/execute` updates it from `pending` to `complete` (or `blocked`) as each sub-phase finishes. Valid values: `pending`, `in progress`, `complete`, `blocked`.

---

## Sub-Phase Summaries

### 01 — <name>
**Scope**: <1–2 sentences>
**Delivers**: <what it produces — specific files, services, DB state>
**Task count**: N
**Complexity**: Low/Medium/High

### 02 — <name>
...

---

## Sequential Execution Quick-Start

```bash
# 1. Execute sub-phase 01
# /execute .agents/plans/<dir>/01-<name>.md

# After completion, verify handoff:
<gate command for 01>

# 2. Execute sub-phase 02
# /execute .agents/plans/<dir>/02-<name>.md

# After completion, verify handoff:
<gate command for 02>

# ... continue in order
```
```

---

## Quality Criteria

### Right-Sizing ✓

- [ ] Each sub-phase has 3–8 atomic tasks
- [ ] No sub-phase is blocked mid-way by state it creates itself
- [ ] Each sub-phase produces at least one independently verifiable artifact

### Self-Containment ✓

- [ ] Each plan passes "No Prior Knowledge Test" without reading parent plan
- [ ] All relevant patterns are **duplicated** (not referenced) in each sub-plan
- [ ] Prerequisites are explicit with verification commands

### Dependency Clarity ✓

- [ ] Every prerequisite has a verification command
- [ ] Handoff state is explicitly declared per sub-phase
- [ ] Sub-phase N+1's prerequisites exactly match sub-phase N's handoff state
- [ ] Gate commands in the manifest are the same as each sub-phase's handoff verification command

### Context Completeness ✓

- [ ] All file references include line numbers where relevant
- [ ] All gotchas from parent plan are propagated to the relevant sub-phases
- [ ] No generic references — all specific and actionable
- [ ] Import statements are specified exactly (not "add the relevant imports")

---

## Update Parent PRD `next_action`

After writing the manifest and all sub-phase files, locate the parent project's PRD (if any) and bump its `next_action` to point at the first sub-phase. The PRD's `next_action` is canonical for "what's next on this project" — leaving it pointing at the now-completed decomposition step is a bug.

Steps:

1. Identify the parent project via `200 Projects/*/PRD.md` whose `## 12. Implementation Phases` (or equivalent) section names the phase being decomposed. The phase name is usually derivable from the parent plan's basename (e.g. `2026-05-23-phase-1-daily-memory-reflection` → "Phase 1 — Daily memory reflection").
2. If a matching PRD is found, update its frontmatter `next_action:` line via `Edit`:
   - `next_action: "Execute Sub-Phase 01 — <name> (<one-line scope hint>)"`
   - Use the manifest's row 01 name and a brief scope hint. Keep the line under ~150 characters.
3. If no matching PRD is found, skip silently.

Stage the PRD edit so it lands in the same commit as the manifest + sub-phase files when the user runs `/commit`.

## Report

After generating all sub-phase plans and the manifest, provide:

1. **Sub-phase count** and the decomposition rationale
2. **Full paths** to all generated files
3. **Dependency graph** in text form showing execution order
4. **Any concerns** about the decomposition (ambiguous boundaries, tasks that could go either way)
5. **Parent PRD update** — whether `next_action` was bumped (and to what), or "no parent PRD found"
6. **Confidence score** N/10 that each sub-phase can be executed independently with `/execute`
