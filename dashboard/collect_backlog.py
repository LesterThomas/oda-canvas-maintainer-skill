"""Work out how many issues and PRs were open on each day of the last 6 months.

Covers every non-archived repository in tmforum-oda. Read-only: uses
`gh api graphql` queries only.

Usage:
    python collect_backlog.py <out.json>

Writes {"rows": [...]} with one row per repository and day:
{"day", "repo", "openIssues", "openPRs"}. Repositories with nothing open
in the window are left out.

An item counts as open on a day if it was created on or before that day and
was not yet closed by the end of it. GitHub keeps only the latest close time,
so an item that was closed and later reopened counts as open from its
creation, and one that was reopened and closed again counts as open until
the last close.
"""
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ORG = "tmforum-oda"
DAYS = 183


def gql(query, **vars_):
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in vars_.items():
        args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    out = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if out.returncode:
        raise SystemExit(out.stderr)
    return json.loads(out.stdout)["data"]


REPOS = """
query($org: String!, $cursor: String) {
  organization(login: $org) {
    repositories(first: 100, after: $cursor, isArchived: false, privacy: PUBLIC) {
      pageInfo { hasNextPage endCursor }
      nodes { name }
    }
  }
}
"""

# One query shape for both connections; $kind picks the field name.
ITEMS = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    %s(first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes { createdAt closedAt state }
    }
  }
}
"""


def paged(query, path, **vars_):
    cursor, nodes = None, []
    while True:
        kw = dict(vars_)
        if cursor:
            kw["cursor"] = cursor
        data = gql(query, **kw)
        for key in path:
            data = data[key]
        nodes += [n for n in data["nodes"] if n]
        if not data["pageInfo"]["hasNextPage"]:
            return nodes
        cursor = data["pageInfo"]["endCursor"]


def open_per_day(items, days):
    """Count the items open at the end of each day."""
    counts = []
    for d in days:
        end = d.isoformat() + "T23:59:59Z"
        counts.append(sum(
            1 for it in items
            if it["createdAt"] <= end
            and (it["state"] == "OPEN" or not it["closedAt"] or it["closedAt"] > end)
        ))
    return counts


def main():
    today = datetime.now(timezone.utc).date()
    days = [today - timedelta(days=i) for i in range(DAYS - 1, -1, -1)]
    repos = sorted(r["name"] for r in paged(REPOS, ["organization", "repositories"], org=ORG))

    rows = []
    for repo in repos:
        issues = paged(ITEMS % "issues", ["repository", "issues"], owner=ORG, name=repo)
        prs = paged(ITEMS % "pullRequests", ["repository", "pullRequests"], owner=ORG, name=repo)
        oi, op = open_per_day(issues, days), open_per_day(prs, days)
        if not any(oi) and not any(op):
            continue
        rows += [
            {"day": d.isoformat(), "repo": repo, "openIssues": i, "openPRs": p}
            for d, i, p in zip(days, oi, op)
        ]
        print(f"{repo}: {oi[-1]} issues, {op[-1]} PRs open now", file=sys.stderr)

    doc = {
        "schemaVersion": 1,
        "org": ORG,
        "periodStart": days[0].isoformat(),
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "rows": rows,
    }
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1)
    print(f"{len(rows)} rows for {len({r['repo'] for r in rows})} repositories written")


main()
