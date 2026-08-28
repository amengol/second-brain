#!/usr/bin/env bash
# Cross-platform Python launcher for the vault's Claude Code hooks.
#
# Hooks are authored once in .claude/settings.json (committed, shared Mac<->Windows)
# but `python3` is not portable: on Windows it resolves to the Microsoft Store
# execution-alias stub under WindowsApps, which exits with "Permission denied"
# when exec'd from a shell. This picks the first interpreter that is BOTH real
# (not the stub) and actually runnable, then hands off to it.
#
# Usage: bash run-python.sh <script.py> [args...]
set -euo pipefail

# Force UTF-8 for stdin/stdout/stderr and file I/O. Windows Python defaults
# stdout to the cp1252 console codepage, which raises UnicodeEncodeError when a
# hook prints vault content containing non-Latin1 chars (e.g. the "->" arrow).
# macOS already defaults to UTF-8, so this is a no-op there.
export PYTHONUTF8=1

for cand in python3 python py; do
  path="$(command -v "$cand" 2>/dev/null)" || continue
  case "$path" in
    *WindowsApps*) continue ;;   # skip the Store stub that shadows python3 on Windows
  esac
  if "$path" -c '' >/dev/null 2>&1; then
    exec "$path" "$@"
  fi
done

echo "run-python.sh: no working Python interpreter found on PATH (tried python3, python, py)" >&2
exit 1
