#!/usr/bin/env python3
"""SessionEnd / PreCompact flush hook for the vault.

When a Claude Code session ends (or just before it auto-compacts), this reads
the session transcript and appends a compact, high-signal capture to today's
daily note, under a dedicated "## Session Captures (auto)" section:
  - the owner's prompts / intents (the decision-bearing turns)
  - the files created or edited during the session

No LLM call -> zero added token cost, fully deterministic, non-blocking. It is
intentionally a raw-but-clean log, not a polished summary; promote anything
worth keeping up into the Progress Log during review. The auto section is kept
separate from hand-written sections so it never clobbers the owner's writing.

Reads the hook payload (JSON) on stdin: transcript_path, hook_event_name, etc.
Writes nothing for trivial sessions (e.g. a quick /clear) — a capture only
happens for a *substantial* session, and the LLM summary is reserved for those
plus PreCompact (loss prevention). Never raises.

The hook never *creates* the daily note — whatever creates your daily notes
(Obsidian's Daily Notes core plugin, Templater, or you by hand) owns that file.
If today's daily note already exists, the capture is appended to it; if it
doesn't exist yet, the capture is written into 100 Inbox/ instead (the vault's
"dump zone", processed in the weekly review).

NOTE: if nothing is creating your daily notes, every capture silently lands in
100 Inbox/ and the daily loop never starts. `/onboard` settles this during
setup; see 000 Meta/Vault Setup.md for the decision that was made.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

MAX_PROMPT_CHARS = 280
EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
SECTION = "## Session Captures (auto)"

# Claude Code marks auto-injected user-role records with `isMeta: true` at the
# JSONL record level. That covers slash-command rendered output (e.g. /context's
# table, delivered as a clean `role=user` markdown blob with NO wrapper text),
# skill bodies (e.g. /commit's instructions), image placeholders, and local-
# command caveats. The wrappers themselves (`<command-name>/foo</command-name>`)
# do NOT carry isMeta but are caught by clean_prompt()'s `<` check + the marker
# scan below (defense-in-depth for the rare case where a wrapper + body share
# one record as sibling text blocks).
COMMAND_MARKERS = (
    "<command-name>",
    "<command-message>",
    "<command-args>",
    "<local-command-stdout>",
    "<local-command-stderr>",
    "<local-command-caveat>",
)

# The auto-generated continuation summary written by /compact / auto-compact is
# a regular user-role record (no isMeta) that always opens with this prefix.
COMPACT_CONTINUATION_PREFIX = (
    "This session is being continued from a previous conversation"
)

# --- Summary layer (LLM) ----------------------------------------------------
# A short synthesized "what was decided / done / learned" via headless `claude`.
# Runs on the Claude subscription (not API $). Degrades gracefully: any failure
# or timeout just skips the summary and the deterministic capture still writes.
SUMMARY_ENABLED = True
SUMMARY_MODEL = "haiku"          # cheap/fast; set "" to use the Claude default
SUMMARY_TIMEOUT = 60             # seconds; on timeout we skip the summary
LOCK_ENV = "BRAIN_FLUSH_LOCK"    # set when we spawn `claude` so hooks don't recurse

# --- Substance gate ---------------------------------------------------------
# A capture (and its summary) only happens for a *substantial* session, so a
# casual /clear or exit of a quick question writes nothing and spawns no
# `claude` call -> instant, no latency, no journal noise. PreCompact always
# counts as substantial because context is about to be lost.
SUBSTANCE_MIN_CHARS = 1500       # condensed-transcript length
SUBSTANCE_MIN_PROMPTS = 3        # number of real user turns

# --- Debug log (temporary diagnostic) ---------------------------------------
# Writes one line per invocation to .claude/hooks/flush-debug.log so we can see
# whether/what events actually fire. Flip DEBUG = False once it's confirmed.
DEBUG = False


def _debug(msg: str) -> None:
    if not DEBUG:
        return
    try:
        logp = Path(__file__).resolve().parent / "flush-debug.log"
        with logp.open("a", encoding="utf-8") as fh:
            fh.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}\n")
    except Exception:
        pass


def vault_root() -> Path:
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    return Path(env) if env else Path(__file__).resolve().parents[2]


def load_payload() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def iter_records(transcript_path: str):
    p = Path(transcript_path)
    if not p.is_file():
        return
    with p.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception:
                continue


def text_blocks(content) -> list[str]:
    out: list[str] = []
    if isinstance(content, str):
        out.append(content)
    elif isinstance(content, list):
        for blk in content:
            if isinstance(blk, dict) and blk.get("type") == "text":
                out.append(blk.get("text", ""))
    return out


def clean_prompt(text: str) -> "str | None":
    t = text.strip()
    if not t or t.startswith("<") or t.startswith("Caveat:"):
        return None  # skip system-reminders / command wrappers / caveat lines
    t = " ".join(t.split())
    if len(t) > MAX_PROMPT_CHARS:
        t = t[:MAX_PROMPT_CHARS].rstrip() + "…"
    return t


def is_command_message(blocks: list[str]) -> bool:
    return any(any(m in b for m in COMMAND_MARKERS) for b in blocks)


def is_noise_user_record(rec: dict, blocks: list[str]) -> bool:
    """Return True for user-role records that aren't a real user prompt.

    Primary signal: `isMeta: true` (Claude Code's own marker for auto-injected
    user records — slash output, skill bodies, image placeholders, caveats).
    Also catches the compaction continuation summary and any wrapper text.
    """
    if rec.get("isMeta") is True:
        return True
    if is_command_message(blocks):
        return True
    for b in blocks:
        if b.lstrip().startswith(COMPACT_CONTINUATION_PREFIX):
            return True
    return False


def parse_transcript(transcript_path: str):
    prompts: list[str] = []
    files: list[str] = []
    seen: set[str] = set()
    for rec in iter_records(transcript_path):
        msg = rec.get("message") or {}
        role = msg.get("role") or rec.get("type")
        content = msg.get("content")
        if role == "user":
            if isinstance(content, list) and all(
                isinstance(b, dict) and b.get("type") == "tool_result" for b in content
            ):
                continue  # tool results, not a real prompt
            blocks = text_blocks(content)
            if is_noise_user_record(rec, blocks):
                continue  # auto-injected record (slash output, skill body, etc.)
            for tb in blocks:
                c = clean_prompt(tb)
                if c:
                    prompts.append(c)
        elif role == "assistant" and isinstance(content, list):
            for blk in content:
                if (
                    isinstance(blk, dict)
                    and blk.get("type") == "tool_use"
                    and blk.get("name") in EDIT_TOOLS
                ):
                    fp = (blk.get("input") or {}).get("file_path")
                    if fp and fp not in seen:
                        seen.add(fp)
                        files.append(fp)
    return prompts, files


def rel_to_vault(fp: str, root: Path) -> str:
    try:
        return str(Path(fp).resolve().relative_to(root.resolve()))
    except Exception:
        return fp


def build_condensed(transcript_path: str, limit: int = 16000) -> str:
    """A compact transcript (user text + assistant text + edits) for the summarizer.
    Keeps the most recent ~limit chars so the outcome of the session is included."""
    turns: list[str] = []
    for rec in iter_records(transcript_path):
        msg = rec.get("message") or {}
        role = msg.get("role") or rec.get("type")
        content = msg.get("content")
        if role == "user":
            if isinstance(content, list) and all(
                isinstance(b, dict) and b.get("type") == "tool_result" for b in content
            ):
                continue
            blocks = text_blocks(content)
            if is_noise_user_record(rec, blocks):
                continue  # auto-injected record; not real user content
            for tb in blocks:
                t = tb.strip()
                if t and not t.startswith("<") and not t.startswith("Caveat:"):
                    turns.append("User: " + " ".join(t.split())[:1200])
        elif role == "assistant" and isinstance(content, list):
            for blk in content:
                if not isinstance(blk, dict):
                    continue
                if blk.get("type") == "text" and blk.get("text", "").strip():
                    turns.append("Assistant: " + " ".join(blk["text"].split())[:1200])
                elif blk.get("type") == "tool_use" and blk.get("name") in EDIT_TOOLS:
                    fp = (blk.get("input") or {}).get("file_path")
                    if fp:
                        turns.append(f"[{blk.get('name')} {fp}]")
    text = "\n".join(turns)
    return text[-limit:] if len(text) > limit else text


def summarize(condensed: str) -> "str | None":
    if not SUMMARY_ENABLED or not condensed.strip() or not shutil.which("claude"):
        return None
    prompt = (
        "Summarize this Claude Code working session for my second-brain daily "
        "journal. In 3-6 terse, concrete bullets capture: what was decided, what "
        "was actually done/changed, and any lessons or gotchas worth remembering "
        "later. No preamble or sign-off — output only the bullet list.\n\n"
        "<session>\n" + condensed + "\n</session>"
    )
    cmd = ["claude", "-p"]
    if SUMMARY_MODEL:
        cmd += ["--model", SUMMARY_MODEL]
    cmd.append(prompt)
    env = dict(os.environ)
    env[LOCK_ENV] = "1"  # the spawned claude must not re-trigger these hooks
    try:
        res = subprocess.run(
            cmd, capture_output=True, text=True, timeout=SUMMARY_TIMEOUT, env=env
        )
    except Exception:
        return None
    out = (res.stdout or "").strip()
    return out or None


def build_block(prompts, files, root, event, reason) -> str:
    now = datetime.now()
    label = event or "SessionEnd"
    if reason:
        label += f" · {reason}"
    lines = [f"### {now:%H:%M} · {label}"]
    if prompts:
        lines.append("**Prompts / intents:**")
        lines += [f"- {p}" for p in prompts]
    if files:
        lines.append("**Files touched:**")
        lines += [f"- `{rel_to_vault(f, root)}`" for f in files]
    return "\n".join(lines)


def today_note(root: Path) -> Path:
    return root / "800 Journal" / f"{datetime.now():%Y-%m-%d}.md"


# --- Capture target ---------------------------------------------------------
# The hook never creates the daily note (Obsidian's Templater owns that file).
# If today's daily note already exists, append to it; otherwise write into
# 100 Inbox/ so the capture still lands and gets folded in at the weekly review.


def ensure_inbox_note(path: Path) -> None:
    if path.exists():
        return
    now = datetime.now()
    body = (
        f"---\ntype: note\nstatus: active\ndate: {now:%Y-%m-%d}\n"
        f"tags: [type/note, session-capture]\n---\n\n"
        f"# Session Captures · {now.strftime('%A, %B')} {now.day}, {now.year}\n\n"
        "_Auto-captured by the session flush hook because today's daily note "
        "didn't exist yet. Fold anything worth keeping into your daily note or "
        "projects at the weekly review, then delete this._\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def capture_target(root: Path) -> Path:
    daily = today_note(root)
    if daily.exists():
        return daily
    inbox = root / "100 Inbox" / f"Session Captures {datetime.now():%Y-%m-%d}.md"
    ensure_inbox_note(inbox)
    return inbox


def append_capture(path: Path, block: str) -> None:
    existing = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    out = []
    if existing and not existing.endswith("\n"):
        out.append("\n")
    if SECTION not in existing:
        out.append(f"\n{SECTION}\n")
    out.append(f"\n{block}\n")
    with path.open("a", encoding="utf-8") as fh:
        fh.write("".join(out))


def is_substantial(event: str, prompts, files, condensed: str) -> bool:
    if event == "PreCompact":  # context about to be lost -> always worth capturing
        return True
    return (
        bool(files)
        or len(prompts) >= SUBSTANCE_MIN_PROMPTS
        or len(condensed) >= SUBSTANCE_MIN_CHARS
    )


def main() -> int:
    payload = load_payload()
    event = payload.get("hook_event_name", "")
    reason = payload.get("reason") or payload.get("trigger") or ""
    transcript_path = payload.get("transcript_path")
    locked = bool(os.environ.get(LOCK_ENV))
    _debug(f"FIRED event={event!r} reason={reason!r} locked={locked} transcript={bool(transcript_path)}")
    if locked:
        return 0  # inside a summary call we spawned — do not recurse
    if not transcript_path:
        _debug("skip: no transcript_path")
        return 0
    prompts, files = parse_transcript(transcript_path)
    condensed = build_condensed(transcript_path)
    substantial = is_substantial(event, prompts, files, condensed)
    _debug(f"prompts={len(prompts)} files={len(files)} condensed_len={len(condensed)} substantial={substantial}")
    if not substantial:
        return 0  # trivial session (e.g. a quick /clear) -> capture nothing, no summary

    # Write the deterministic capture FIRST so it always lands, even if the
    # session is torn down (e.g. /clear) before a slow summary call returns.
    root = vault_root()
    target = capture_target(root)
    append_capture(target, build_block(prompts, files, root, event, reason))
    _debug(f"wrote capture -> {target}")

    # Summary is best-effort, runs AFTER the capture is safe, and is skipped on
    # /clear (which immediately starts a new session — no blocking teardown lag).
    if event == "PreCompact" or (event == "SessionEnd" and reason != "clear"):
        summary = summarize(condensed)
        _debug(f"summary={'yes' if summary else 'none'}")
        if summary:
            with target.open("a", encoding="utf-8") as fh:
                fh.write(f"**Summary:**\n{summary}\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # never break session teardown / compaction
        sys.stderr.write(f"[flush-to-daily] skipped: {exc}\n")
        sys.exit(0)
