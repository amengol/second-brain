---
description: Create a new commit for all uncommitted changes
argument-hint: [WSL|PS] [push]  # shell + optional push flag
---

# Commit: Create Atomic Commit

**Arguments (`$ARGUMENTS`):** a shell selector plus an optional push flag, in any order.

- **Shell** — `WSL` (WSL/Bash) or `PS` (PowerShell). If omitted, default to **PS** per project preference. This only picks the command syntax; the assistant runs `git commit` directly in **either** shell.
- **Push flag** — `push` or `--push`. When present, run `git push` after the commit. When absent, commit only — do **not** push.

The old "PowerShell commits via the IDE" rule is retired. `/commit` always creates the commit itself.

---

## 1. Inspect Uncommitted Changes

Run the following so we know what will be committed.

**WSL:**
```bash
git status && git diff HEAD && git status --porcelain
```

**PS (PowerShell):**
```powershell
git status; git diff HEAD; git status --porcelain
```

---

## 2. Stage All Changes

Both shells:
```
git add -A
```

---

## 3. Create the Commit

Compose one atomic commit message that summarizes the work. Add a conventional tag: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, etc.

**WSL (Bash):** double quotes for `-m`; escape inner double quotes with `\"`.
```bash
git commit -m "feat: short description of change"
```

**PS (PowerShell):** for a multi-line message use a single-quoted here-string (closing `'@` at column 0):
```powershell
git commit -m @'
feat: short description of change
'@
```

---

## 4. Push (only if the push flag was passed)

If `push` / `--push` is in the arguments, push after the commit succeeds. Otherwise stop after step 3.

Both shells:
```
git push
```

If on the default branch with no upstream, set it: `git push -u origin HEAD`.

---

## Summary

| Step    | Command | Runs when |
|---------|---------|-----------|
| Inspect | `git status; git diff HEAD; git status --porcelain` | always |
| Stage   | `git add -A` | always |
| Commit  | `git commit -m "msg"` | always (both shells) |
| Push    | `git push` | only if `push` / `--push` passed |

The assistant runs these directly. Composing the message is always fine; pushing happens **only** with the push flag.
