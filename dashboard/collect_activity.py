"""Collect LesterThomas's maintainer activity in tmforum-oda since 2026-09-28.

Read-only: uses `gh api graphql` queries only.

Usage:
    python collect_activity.py <out.json> [<session-transcript.jsonl>]

Writes {"rows": [...]} with one row per action (closed, merged, approved,
reviewed, commented, opened), each with the issue or PR it was on. Items
named in the drafts folder or the optional transcript get
"discussedInSession": true.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

USER = "LesterThomas"
ORG = "tmforum-oda"
SINCE = "2026-09-28"
DRAFTS = os.path.expanduser("~/.oda-canvas-maintainer/drafts")


def gql(query, **vars_):
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in vars_.items():
        args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    out = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if out.returncode:
        raise SystemExit(out.stderr)
    return json.loads(out.stdout)["data"]


SEARCH = """
query($q: String!, $cursor: String) {
  search(query: $q, type: ISSUE, first: 50, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      __typename
      ... on Issue {
        number title url state stateReason createdAt closedAt
        repository { name }
        author { login }
        timelineItems(itemTypes: [CLOSED_EVENT], last: 5) {
          nodes { ... on ClosedEvent { createdAt actor { login } } }
        }
        comments(last: 100) { nodes { author { login } createdAt url } }
      }
      ... on PullRequest {
        number title url state createdAt closedAt mergedAt
        repository { name }
        author { login }
        mergedBy { login }
        timelineItems(itemTypes: [CLOSED_EVENT], last: 5) {
          nodes { ... on ClosedEvent { createdAt actor { login } } }
        }
        comments(last: 100) { nodes { author { login } createdAt url } }
        reviews(last: 50) { nodes { author { login } state submittedAt url } }
      }
    }
  }
}
"""


def search(q):
    cursor, nodes = None, []
    while True:
        kw = {"q": q}
        if cursor:
            kw["cursor"] = cursor
        data = gql(SEARCH, **kw)["search"]
        nodes += [n for n in data["nodes"] if n]
        if not data["pageInfo"]["hasNextPage"]:
            return nodes
        cursor = data["pageInfo"]["endCursor"]


def drafted_items():
    """Repo/number pairs the skill drafted something for (from drafts/ file names)."""
    items = set()
    for root, _dirs, files in os.walk(DRAFTS):
        for name in files:
            m = re.match(r"^(oda-canvas|reference-example-components)-(\d+)[.-]", name)
            if m:
                items.add((m.group(1), int(m.group(2))))
            # Sweep tables list one issue per row: "| #474 Title ... |"
            s = re.match(r"^sweep-(oda-canvas|reference-example-components)-batch", name)
            if s:
                text = open(os.path.join(root, name), encoding="utf-8").read()
                for num in re.findall(r"^\|\s*#(\d+)", text, re.M):
                    items.add((s.group(1), int(num)))
    # PRs the skill prepared on request (release-charts fix and the #63 fix).
    items |= {("reference-example-components", 76), ("reference-example-components", 77)}
    return items


def main():
    queries = [
        f"org:{ORG} closed:>={SINCE}",
        f"org:{ORG} commenter:{USER} updated:>={SINCE}",
        f"org:{ORG} is:pr reviewed-by:{USER} updated:>={SINCE}",
        f"org:{ORG} is:pr author:{USER} created:>={SINCE}",
        f"org:{ORG} is:issue author:{USER} created:>={SINCE}",
    ]
    seen = {}
    for q in queries:
        for n in search(q):
            seen[(n["repository"]["name"], n["number"])] = n

    drafted = drafted_items()
    # Items discussed in this chat session: "#123" mentions in the transcript.
    if len(sys.argv) > 2:
        text = open(sys.argv[2], encoding="utf-8").read()
        mentioned = {int(n) for n in re.findall(r"#(\d{2,3})\b", text)}
        drafted |= {(r, n) for (r, n) in seen if n in mentioned}
    records = []
    for (repo, num), n in sorted(seen.items()):
        kind = "pr" if n["__typename"] == "PullRequest" else "issue"
        actions = []
        closer = next(
            (e for e in reversed(n["timelineItems"]["nodes"]) if e and e.get("actor")), None
        )
        if kind == "pr" and n.get("mergedAt") and n["mergedAt"][:10] >= SINCE and (n.get("mergedBy") or {}).get("login") == USER:
            actions.append({"type": "merged", "date": n["mergedAt"]})
        elif closer and closer["actor"]["login"] == USER and closer["createdAt"][:10] >= SINCE and n.get("state") == "CLOSED":
            actions.append({"type": "closed", "date": closer["createdAt"]})
        for c in n["comments"]["nodes"]:
            if (c.get("author") or {}).get("login") == USER and c["createdAt"][:10] >= SINCE:
                actions.append({"type": "commented", "date": c["createdAt"], "url": c["url"]})
        for r in (n.get("reviews") or {}).get("nodes", []):
            if (r.get("author") or {}).get("login") == USER and (r.get("submittedAt") or "")[:10] >= SINCE:
                kind_r = {"APPROVED": "approved", "CHANGES_REQUESTED": "changes_requested"}.get(r["state"], "reviewed")
                actions.append({"type": kind_r, "date": r["submittedAt"], "url": r["url"]})
        if (n.get("author") or {}).get("login") == USER and n["createdAt"][:10] >= SINCE:
            actions.append({"type": "opened", "date": n["createdAt"]})
        if not actions:
            continue
        # One row per action, so the file is a flat table.
        for a in sorted(actions, key=lambda a: a["date"]):
            records.append({
                "day": a["date"][:10],
                "at": a["date"],
                "action": a["type"],
                "ref": f"{repo}#{num}",
                "repo": repo,
                "number": num,
                "kind": kind,
                "title": n["title"],
                "url": a.get("url") or n["url"],
                "author": (n.get("author") or {}).get("login"),
                "state": "MERGED" if n.get("mergedAt") else n["state"],
                "closeReason": n.get("stateReason"),
                "discussedInSession": (repo, num) in drafted,
            })

    doc = {
        "schemaVersion": 1,
        "maintainer": USER,
        "org": ORG,
        "periodStart": SINCE,
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "rows": records,
    }
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
    print(f"{len(records)} actions on {len({r['ref'] for r in records})} items written")


main()
