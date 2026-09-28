"""Find possible duplicates and related issues/PRs across in-scope tmforum-oda repos.

Read-only. Builds several searches from the item's title and body (title
keywords, backticked identifiers, CamelCase/kebab names, quoted error lines),
runs them with `gh search issues --include-prs`, and scores candidates by how
many searches hit them and by title-word overlap. Returns *candidates only*:
the model must read them and confirm; a duplicate needs the same problem.

Usage:
    python find_related.py <url | [owner/]repo number> [--repos a/b,c/d] [--limit 10]
    python find_related.py --text "free text to search for" [--repos ...]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gh import GhError, emit, gh_json, parse_target  # noqa: E402

DEFAULT_REPOS = [
    "tmforum-oda/oda-canvas", "tmforum-oda/reference-example-components", "tmforum-oda/oda-helm-charts",
    "tmforum-oda/canvas-prerequisites", "tmforum-oda/TMFOP006-Event-Management",
    "tmforum-oda/TMFCOP009-model-as-a-service-operator",
    "tmforum-oda/TMFOP012-data-products-lifecycle-management-operator", "tmforum-oda/oda-ca-docs",
]
STOP = set("""a an and are as at be but by can canvas component components could do does for from has have how i if in
into is it its not of on or oda our should so that the their there this to use used using was we what when which
will with would add added adding update updated support new issue feature fix bug subject operator operators ctk
please need needs allow make""".split())


def words(text: str) -> list[str]:
    return [w for w in re.findall(r"[A-Za-z][A-Za-z0-9_.-]{2,}", text.lower()) if w not in STOP]


def build_queries(title: str, body: str) -> list[str]:
    title = re.sub(r"^\s*<[^>]*>\s*:?\s*(subject)?", "", title)  # unfilled template prefixes
    title = re.sub(r"^\s*[\w-]+\s*:\s*", "", title) if ":" in title[:40] else title
    qs = []
    # GitHub search ANDs every term, so long queries find nothing. Use pairs of the most distinctive
    # title words (longest first), and let the multi-query score rank candidates.
    tw = list(dict.fromkeys(words(title)))
    key = sorted(tw, key=len, reverse=True)[:4]
    pairs = [f"{key[i]} {key[j]}" for i in range(len(key)) for j in range(i + 1, len(key))]
    qs += pairs[:5] if pairs else key[:1]
    idents = re.findall(r"`([^`\n]{3,60})`", body or "")
    idents += re.findall(r"\b([A-Z][a-z]+(?:[A-Z][a-z0-9]+)+)\b", f"{title} {body or ''}")  # CamelCase
    idents += re.findall(r"\b([a-z0-9]+(?:-[a-z0-9]+){1,4})\b", title)                      # kebab-case names
    seen = set()
    for i in idents:
        i = i.strip()
        if i.lower() in seen or i.lower() in STOP or len(i) < 4:
            continue
        seen.add(i.lower())
        qs.append(f'"{i}"')
        if len(seen) >= 3:
            break
    for line in (body or "").splitlines():
        if re.search(r"(error|exception|failed|denied|not found|forbidden)", line, re.I) and 15 < len(line) < 140:
            qs.append('"' + re.sub(r'["\\]', "", line.strip())[:80] + '"')
            break
    return list(dict.fromkeys(q for q in qs if q.strip('" ')))


def search(query: str, repos: list[str], limit: int) -> list[dict]:
    args = ["search", "issues", query, "--include-prs", "--limit", str(limit),
            "--json", "number,title,url,state,repository,isPullRequest,createdAt,updatedAt"]
    for r in repos:
        args += ["--repo", r]
    try:
        return gh_json(args) or []
    except GhError:
        return []


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("target", nargs="*")
    ap.add_argument("--text")
    ap.add_argument("--repos", default=",".join(DEFAULT_REPOS))
    ap.add_argument("--limit", type=int, default=10)
    a = ap.parse_args()
    repos = [r.strip() for r in a.repos.split(",") if r.strip()]

    self_ref = None
    if a.text:
        title, body = a.text, ""
    elif a.target:
        owner, name, number = parse_target(a.target)
        self_ref = (f"{owner}/{name}", number)
        try:
            item = gh_json(["issue", "view", str(number), "-R", f"{owner}/{name}", "--json", "title,body"])
        except GhError:
            item = gh_json(["pr", "view", str(number), "-R", f"{owner}/{name}", "--json", "title,body"])
        title, body = item["title"], item.get("body") or ""
    else:
        ap.error("give an item or --text")

    queries = build_queries(title, body)
    cands: dict[tuple[str, int], dict] = {}
    for q in queries:
        for hit in search(q, repos, 15):
            key = (hit["repository"]["nameWithOwner"], hit["number"])
            if key == self_ref:
                continue
            c = cands.setdefault(key, {"repo": key[0], "number": key[1], "title": hit["title"], "url": hit["url"],
                                       "state": hit["state"], "type": "PR" if hit["isPullRequest"] else "issue",
                                       "createdAt": hit["createdAt"][:10], "matched_queries": []})
            c["matched_queries"].append(q)
    tset = set(words(title))
    for c in cands.values():
        cw = set(words(c["title"]))
        overlap = len(tset & cw) / max(1, len(tset | cw))
        c["title_overlap"] = round(overlap, 2)
        c["score"] = round(len(c["matched_queries"]) + 3 * overlap, 2)
    ranked = sorted(cands.values(), key=lambda c: -c["score"])[: a.limit]
    emit({"source": {"title": title, "item": f"{self_ref[0]}#{self_ref[1]}" if self_ref else None},
          "queries": queries, "repos": repos, "candidates": ranked,
          "note": "Candidates only. Read each one; call it a duplicate only if it is the same problem."})


if __name__ == "__main__":
    main()
