#!/usr/bin/env python3
"""SessionStart hook for the vault.

Read-only. Injects the *current state* into every Claude Code session so the
assistant already knows where things stand without the owner running /prime:
  - MEMORY.md            durable decisions / lessons
  - Projects Dashboard   live status / next actions
  - the most recent daily notes
  - today's unprocessed inbox session-capture, if one exists (the flush hook
    writes there when the daily note doesn't exist yet) — flagged so it gets
    folded in instead of silently sitting in the inbox

It prints to stdout; Claude Code adds SessionStart stdout to the session
context. No writes, no network, no API calls -> zero token cost to produce.

Static identity/contract (CLAUDE.md + its @imports of SOUL.md / USER.md) is
already loaded by Claude Code itself, so this hook only adds the dynamic layer.

Test it any time from the vault root:
    python3 .claude/hooks/session-start-context.py

If context injection ever stops working, swap the final stdout.write for the
JSON form (see note at the bottom).
"""

from __future__ import annotations

import os
import re
import sys
from datetime import datetime
from pathlib import Path

N_DAILY = 1                 # most recent daily only — keep total output under the 10KB inline limit
MAX_CHARS_PER_FILE = 3000   # per-section soft cap so one big file can't crowd out the others
TOTAL_BUDGET = 9500         # hard ceiling on the assembled output, in UTF-8 bytes. Claude Code injects SessionStart
                            # stdout inline ONLY if it's under ~10KB; above that it persists the output
                            # to a file and injects just a 2KB preview — so the context is effectively
                            # lost. Stay under this or the hook silently stops loading context.

DAILY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")  # excludes weekly notes (….-W##.md)


def vault_root() -> Path:
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env)
    # .claude/hooks/<this file>  ->  vault root is three parents up
    return Path(__file__).resolve().parents[2]


def read_capped(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > MAX_CHARS_PER_FILE:
        text = text[:MAX_CHARS_PER_FILE] + "\n\n[...truncated for session context...]"
    return text.rstrip()


def recent_daily_notes(journal: Path, n: int) -> list[Path]:
    if not journal.is_dir():
        return []
    dailies = [p for p in journal.iterdir() if DAILY_RE.match(p.name)]
    dailies.sort(key=lambda p: p.name, reverse=True)  # filenames sort = date sort
    return dailies[:n]


def assemble(parts: list[str], budget: int) -> str:
    """Join sections with `---` separators, keeping the UTF-8 byte length <= budget.

    Sections are consumed in priority order; once the budget is spent the current
    section is truncated (if a useful chunk still fits) and the rest are dropped.
    Budgeting is in bytes, not chars, because Claude Code measures the ~10KB inline
    limit in bytes and vault content has multibyte chars (em-dashes, arrows).
    """
    sep = "\n\n---\n\n"
    marker = "\n\n[...truncated to fit session-context budget...]"
    sep_b = len(sep.encode("utf-8"))
    marker_b = len(marker.encode("utf-8"))
    out: list[str] = []
    used = 0  # bytes
    for part in parts:
        extra = sep_b if out else 0
        avail = budget - used - extra
        if avail <= 0:
            break
        part_b = part.encode("utf-8")
        if len(part_b) <= avail:
            out.append(part)
            used += extra + len(part_b)
        else:
            keep = avail - marker_b
            if keep > 200:  # only bother if a meaningful chunk survives
                # errors="ignore" drops a trailing char split mid-byte-sequence
                out.append(part_b[:keep].decode("utf-8", errors="ignore") + marker)
            break
    return sep.join(out)


def main() -> int:
    if os.environ.get("BRAIN_FLUSH_LOCK"):
        return 0  # spawned by the flush summary call — don't inject context into it
    root = vault_root()
    parts: list[str] = [
        "# Vault session context (auto-loaded, read-only)\n"
        "Below is the current state of the owner's second brain, injected at session "
        "start. Treat it as the live picture of where things stand. Identity, "
        "boundaries, and profile are already loaded via CLAUDE.md / SOUL.md / USER.md."
    ]

    mem = root / "MEMORY.md"
    if mem.is_file():
        parts.append("## MEMORY.md — durable decisions & lessons\n\n" + read_capped(mem))

    dash = root / "200 Projects" / "000 Projects Dashboard.md"
    if dash.is_file():
        parts.append("## Projects Dashboard — live status & next actions\n\n" + read_capped(dash))

    inbox_cap = root / "100 Inbox" / f"Session Captures {datetime.now():%Y-%m-%d}.md"
    if inbox_cap.is_file():
        parts.append(
            "## ACTION — unprocessed session capture from earlier today\n"
            "The flush hook wrote this into `100 Inbox/` because today's daily "
            "note didn't exist yet. It hasn't been folded in anywhere. Surface it "
            "to the owner and offer to fold anything worth keeping into the daily note "
            "or projects, then delete the inbox file.\n\n" + read_capped(inbox_cap)
        )

    # Daily notes go last: longest and most expendable verbatim, so if the budget
    # gets tight the assembler truncates here rather than dropping the ACTION items.
    dailies = recent_daily_notes(root / "800 Journal", N_DAILY)
    if dailies:
        chunk = ["## Recent daily note(s) (most recent first)"]
        for p in dailies:
            chunk.append(f"### {p.stem}\n\n" + read_capped(p))
        parts.append("\n\n".join(chunk))

    # Write raw UTF-8 bytes (LF, not text-mode CRLF) so the emitted byte count
    # matches the budget assemble() computed — Windows text-mode stdout would
    # otherwise expand every \n to \r\n and inflate the size past the 10KB limit.
    sys.stdout.buffer.write((assemble(parts, TOTAL_BUDGET) + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # never break a session because of a hook
        sys.stderr.write(f"[session-start-context] skipped: {exc}\n")
        sys.exit(0)

# JSON fallback (if plain stdout ever stops injecting): replace the stdout.write
# in main() with:
#   import json
#   print(json.dumps({"hookSpecificOutput": {
#       "hookEventName": "SessionStart",
#       "additionalContext": assemble(parts, TOTAL_BUDGET)}}))
