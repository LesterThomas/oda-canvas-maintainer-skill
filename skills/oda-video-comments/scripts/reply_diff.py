"""Compare a drafted video-comment reply with what Lester actually posted (learning-loop signal 3).

Offline and read-only. The skill reads the posted reply from YouTube Studio in the browser
and appends it to the draft file under '## Posted reply'; this script then compares the
'Draft reply' block with the 'Posted reply' block and reports what changed: similarity,
sentences removed and added, length change, and a line diff. The model turns meaningful
differences into *proposed* guidance changes (never applied silently).

Usage:
    python reply_diff.py <draft.md>
    python reply_diff.py --all <drafts_dir>     # every draft not yet renamed *.learned.md

Draft file format (written by the skill):
    ---
    video_id: w0iQv9FtuiM
    comment_id: UgxC7YRpVPPX2cBP6Bx4AaABAg
    drafted_at: 2026-11-16T10:00:00Z
    recommended_action: Reply
    ---
    ...
    **Draft reply**
    ```text
    <text>
    ```
    ...
    ## Posted reply
    ```text
    <text Lester posted>
    ```
    (or a sentence instead of the block, e.g. "Not posted: hearted only")
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

FENCE = r"(`{3,})[\w-]*[ \t]*\n(.*?)\n[ \t]*\1"


def frontmatter(text: str) -> dict:
    meta: dict = {}
    m = re.match(r"^﻿?---\s*\n(.*?)\n---\s*\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip("'\"")
    return meta


def section(text: str, heading: str) -> tuple[bool, str | None, str]:
    """Find a heading ('## X' or '**X**'). Return (found, fenced_body_or_None, raw_section_text)."""
    m = re.search(rf"^(?:#+\s*{heading}\s*|\*\*{heading}\*\*\s*)$", text, re.M | re.I)
    if not m:
        return False, None, ""
    rest = text[m.end():]
    nxt = re.search(r"^(?:#{1,3}\s|\*\*[^*\n]+\*\*\s*$)", rest, re.M)
    raw = rest[: nxt.start()] if nxt else rest
    f = re.search(FENCE, raw, re.S)
    return True, (f.group(2).strip() if f else None), raw.strip()


QUERY = re.compile(r"(https?://[^\s\[\]]+) \[query ([^\]]*)\]")


def normalise(text: str) -> str:
    """Undo extract_inbox.js's query-string encoding and Windows line endings, so a
    reply read back from Studio compares cleanly with the draft."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return QUERY.sub(lambda m: m.group(1) + "?" + "&".join(
        p.replace(": ", "=", 1) for p in m.group(2).split(" | ") if p), text)


def sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", re.sub(r"[>*_`#]", "", text)).strip()
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\s-\s|\n", text) if len(s.strip()) > 3]


def compare(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta = frontmatter(text)
    result = {
        "draft": str(path),
        "video_id": meta.get("video_id"),
        "comment_id": meta.get("comment_id"),
        "comment_link": meta.get("comment_link"),
        "drafted_at": meta.get("drafted_at"),
        "draft_recommended_action": meta.get("recommended_action"),
    }
    _, draft, _ = section(text, "Draft reply")
    found, posted, raw = section(text, "Posted reply")
    if not found:
        result["status"] = "no '## Posted reply' section yet: read the posted reply in Studio and append it"
        return result
    if posted is None:
        result.update({"status": "not posted as text", "note": raw[:500]})
        return result
    if not draft:
        result["status"] = "draft has no fenced 'Draft reply' block to compare"
        return result
    draft, posted = normalise(draft).strip(), normalise(posted).strip()
    # YouTube trims trailing spaces on each line; ignore whitespace-only differences.
    draft = "\n".join(line.strip() for line in draft.splitlines())
    posted = "\n".join(line.strip() for line in posted.splitlines())
    ratio = difflib.SequenceMatcher(None, draft, posted).ratio()
    ds, ps = sentences(draft), sentences(posted)
    removed = [s for s in ds if max((difflib.SequenceMatcher(None, s, t).ratio() for t in ps), default=0) < 0.6]
    added = [s for s in ps if max((difflib.SequenceMatcher(None, s, t).ratio() for t in ds), default=0) < 0.6]
    url = re.compile(r"https?://\S+")
    result.update({
        "status": "posted",
        "similarity": round(ratio, 2),
        "assessment": ("posted essentially as drafted" if ratio > 0.9 else
                       "edited" if ratio > 0.5 else "substantially rewritten"),
        "length_change_chars": len(posted) - len(draft),
        "links_removed": sorted(set(url.findall(draft)) - set(url.findall(posted))),
        "links_added": sorted(set(url.findall(posted)) - set(url.findall(draft))),
        "sentences_removed": removed,
        "sentences_added": added,
        "line_diff": "\n".join(difflib.unified_diff(draft.splitlines(), posted.splitlines(),
                                                    "draft", "posted", lineterm=""))[:6000],
    })
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("draft", nargs="?", help="a draft .md file")
    ap.add_argument("--all", metavar="DIR", help="compare every unprocessed draft in DIR")
    args = ap.parse_args()
    if args.all:
        d = Path(args.all).expanduser()
        if not d.is_dir():
            sys.exit(f"not a directory: {d}")
        files = sorted(p for p in d.glob("*.md") if not p.name.endswith(".learned.md"))
        out = [compare(p) for p in files]
    elif args.draft:
        out = compare(Path(args.draft).expanduser())
    else:
        ap.error("give a draft file or --all <dir>")
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
