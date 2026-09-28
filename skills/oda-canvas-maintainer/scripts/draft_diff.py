"""Compare a saved draft with what the maintainer actually posted (learning-loop signal 3).

Read-only. Looks up the item named in the draft's frontmatter, finds the
maintainer's comments/reviews posted after the draft was written, picks the
closest match to the draft comment, and reports what changed: similarity,
sentences removed/added, verdict change, and a line diff. The model turns
meaningful differences into *proposed* guidance changes (never applied silently).

Usage:
    python draft_diff.py <draft.md> [--maintainer LesterThomas]
    python draft_diff.py --all <drafts_dir> [--maintainer LesterThomas]   # every undiffed draft

Draft file format (written by the skill):
    ---
    repo: tmforum-oda/oda-canvas
    number: 613
    kind: pr
    drafted_at: 2026-09-28T17:05:00Z
    recommended_action: Request changes
    ---
    ...brief...
    ## Draft comment
    ```markdown
    <text>
    ```
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gh import emit  # noqa: E402

HERE = Path(__file__).resolve().parent
VERDICT_MAP = {"APPROVED": "Approve", "CHANGES_REQUESTED": "Request changes", "COMMENTED": "Comment"}


def read_draft(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    meta = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip("'\"")
    body = ""
    m = re.search(r"^## Draft comment\s*\n+(`{3,})\w*\s*\n(.*?)\n\1", text, re.S | re.M)
    if m:
        body = m.group(2).strip()
    return meta, body


def sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", re.sub(r"[>*_`#]", "", text)).strip()
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\s-\s", text) if len(s.strip()) > 3]


def compare(draft_path: Path, maintainer: str) -> dict:
    meta, draft = read_draft(draft_path)
    if not meta.get("repo") or not meta.get("number"):
        return {"draft": str(draft_path), "error": "draft has no repo/number frontmatter"}
    proc = subprocess.run([sys.executable, str(HERE / "gather_item.py"), meta["repo"], meta["number"],
                           "--maintainer", maintainer, "--no-diff"],
                          capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        return {"draft": str(draft_path), "error": proc.stderr.strip()[-500:]}
    item = json.loads(proc.stdout)
    since = meta.get("drafted_at", "")
    posted = [p for p in item.get("posted_by_me", []) if (p["at"] or "") >= since and (p["body"] or "").strip()]
    result = {"draft": str(draft_path), "item": item["url"], "drafted_at": since,
              "draft_recommended_action": meta.get("recommended_action")}
    reviews_after = [p for p in item.get("posted_by_me", []) if (p["at"] or "") >= since and p["kind"].startswith("review:")]
    if reviews_after:
        result["posted_verdict"] = VERDICT_MAP.get(reviews_after[-1]["kind"].split(":", 1)[1], reviews_after[-1]["kind"])
        result["verdict_changed"] = (meta.get("recommended_action") or "").lower() != result["posted_verdict"].lower()
    if not posted:
        result["status"] = "not posted yet (no comment or review by the maintainer since the draft)"
        return result
    if not draft:
        result["status"] = "draft has no '## Draft comment' block to compare"
        return result
    best = max(posted, key=lambda p: difflib.SequenceMatcher(None, draft, p["body"]).ratio())
    ratio = difflib.SequenceMatcher(None, draft, best["body"]).ratio()
    ds, ps = sentences(draft), sentences(best["body"])
    removed = [s for s in ds if max((difflib.SequenceMatcher(None, s, t).ratio() for t in ps), default=0) < 0.6]
    added = [s for s in ps if max((difflib.SequenceMatcher(None, s, t).ratio() for t in ds), default=0) < 0.6]
    result.update({
        "status": "posted",
        "posted_at": best["at"], "posted_kind": best["kind"],
        "similarity": round(ratio, 2),
        "assessment": ("posted essentially as drafted" if ratio > 0.9 else
                       "edited" if ratio > 0.5 else "substantially rewritten"),
        "length_change_chars": len(best["body"]) - len(draft),
        "sentences_removed": removed, "sentences_added": added,
        "line_diff": "\n".join(difflib.unified_diff(draft.splitlines(), best["body"].splitlines(),
                                                    "draft", "posted", lineterm=""))[:6000],
    })
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("draft", nargs="?")
    ap.add_argument("--all", metavar="DRAFTS_DIR")
    ap.add_argument("--maintainer", default="LesterThomas")
    a = ap.parse_args()
    if a.all:
        paths = sorted(Path(a.all).expanduser().glob("*.md"))
        briefs = [p for p in paths if not re.search(r"(\.learned|\.comment(\.learned)?)\.md$", p.name)
                  and not p.name.startswith("sweep-")]
        emit([compare(p, a.maintainer) for p in briefs])
    elif a.draft:
        emit(compare(Path(a.draft).expanduser(), a.maintainer))
    else:
        ap.error("give a draft file or --all <drafts_dir>")


if __name__ == "__main__":
    main()
