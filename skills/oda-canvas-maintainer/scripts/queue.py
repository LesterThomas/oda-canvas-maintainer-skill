"""Rank open issues and PRs across repos for the maintainer queue, or list backlog-sweep batches.

Read-only. One paginated GraphQL query per repo. Ranking follows
guidance/queue-priorities.md (the model may re-rank if that guidance changes):

  1 security?        title/body mentions security/vulnerability/CVE/exploit/leak
  2 ext-pr-unreviewed   external PR, no maintainer review or comment yet (oldest first)
  3 ext-issue-unanswered external issue, no maintainer reply yet (oldest first)
  4 author-replied   author (or someone else) spoke after the last maintainer activity
  5 maint-pr-unreviewed co-maintainer PR with no review from another maintainer
  6 stale            no activity for >= --stale-days (candidates for a backlog sweep)
  7 in-progress      everything else (waiting on author, recently handled, drafts)

Usage:
    python queue.py [--repos a/b,c/d] [--maintainer X] [--co-maintainers a,b]
                    [--no-response-days 7] [--stale-days 60] [--limit 15] [--format md|json]
    python queue.py --sweep [--repos ...] [--batch-size 10] [--offset 0]     # backlog sweep batches
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gh import GhError, emit, graphql  # noqa: E402

DEFAULT_REPOS = [
    "tmforum-oda/oda-canvas", "tmforum-oda/reference-example-components", "tmforum-oda/oda-helm-charts",
    "tmforum-oda/canvas-prerequisites", "tmforum-oda/TMFOP006-Event-Management",
    "tmforum-oda/TMFCOP009-model-as-a-service-operator",
    "tmforum-oda/TMFOP012-data-products-lifecycle-management-operator",
]
BOTS = {"copilot-pull-request-reviewer", "Copilot", "copilot", "github-actions", "dependabot"}
# Vulnerability-disclosure language only. Authentication, authorisation and secrets are everyday
# Canvas design vocabulary (there is a whole Authentication epic), so they are deliberately not matched.
SECURITY_RE = re.compile(
    r"\b(vulnerabilit(y|ies)|CVE-\d{4}-\d+|exploit(s|able|ed)?|security (issue|flaw|hole|bug|advisory)"
    r"|remote code execution|RCE|XSS|SQL injection|privilege escalation"
    r"|(token|password|secret|api key|private key)s? (is |are |was |were )?(leaked|exposed|committed|in plain ?text))\b", re.I)
SECURITY_FRESH_DAYS = 90  # older mentions are noted, not escalated

Q = """
query($owner:String!,$name:String!,$prCursor:String,$issueCursor:String,$withPRs:Boolean!,$withIssues:Boolean!){
 repository(owner:$owner,name:$name){
  pullRequests(states:OPEN,first:50,after:$prCursor) @include(if:$withPRs){
   pageInfo{hasNextPage endCursor}
   nodes{number title url createdAt updatedAt isDraft body author{login}
     reviews(last:30){nodes{author{login} state submittedAt}}
     comments(last:30){nodes{author{login} createdAt}}
     labels(first:10){nodes{name}}}}
  issues(states:OPEN,first:50,after:$issueCursor) @include(if:$withIssues){
   pageInfo{hasNextPage endCursor}
   nodes{number title url createdAt updatedAt body author{login}
     comments(last:30){nodes{author{login} createdAt}}
     labels(first:10){nodes{name}}
     timelineItems(last:20,itemTypes:[CROSS_REFERENCED_EVENT]){nodes{... on CrossReferencedEvent{
        source{__typename ... on PullRequest{number url state merged mergedAt title}}}}}}}
 }}
"""


def parse_time(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def login(n) -> str:
    return (n.get("author") or {}).get("login") or "ghost"


def fetch(repo: str, with_prs: bool, with_issues: bool) -> tuple[list, list]:
    owner, name = repo.split("/", 1)
    prs, issues = [], []
    pc = ic = None
    more_p, more_i = with_prs, with_issues
    while more_p or more_i:
        vars_ = dict(owner=owner, name=name, withPRs=more_p, withIssues=more_i)
        if pc:
            vars_["prCursor"] = pc
        if ic:
            vars_["issueCursor"] = ic
        r = graphql(Q, **vars_)["repository"]
        if more_p:
            prs += r["pullRequests"]["nodes"]
            more_p, pc = r["pullRequests"]["pageInfo"]["hasNextPage"], r["pullRequests"]["pageInfo"]["endCursor"]
        if more_i:
            issues += r["issues"]["nodes"]
            more_i, ic = r["issues"]["pageInfo"]["hasNextPage"], r["issues"]["pageInfo"]["endCursor"]
    return prs, issues


def analyse(repo, node, kind, me, maintainers, now, no_resp_days, stale_days):
    author = login(node)
    external = author not in maintainers
    events = [(parse_time(c["createdAt"]), login(c), "comment") for c in node["comments"]["nodes"]]
    if kind == "pr":
        events += [(parse_time(r["submittedAt"]), login(r), f"review:{r['state']}") for r in node["reviews"]["nodes"] if r.get("submittedAt")]
    events = sorted(e for e in events if e[1] not in BOTS and not e[1].endswith("[bot]"))
    maint_events = [e for e in events if e[1] in maintainers and e[1] != author]
    last_maint = maint_events[-1] if maint_events else None
    last = events[-1] if events else None
    created, updated = parse_time(node["createdAt"]), parse_time(node["updatedAt"])
    age, idle = (now - created).days, (now - updated).days
    handlers = sorted({e[1] for e in maint_events if (now - e[0]).days <= stale_days and e[1] != me})
    approved_by = sorted({e[1] for e in maint_events if e[2] == "review:APPROVED"})
    text = f"{node['title']}\n{node.get('body') or ''}"
    item = {
        "repo": repo, "number": node["number"], "kind": kind, "title": node["title"], "url": node["url"],
        "author": author, "external": external, "age_days": age, "idle_days": idle,
        "draft": node.get("isDraft", False),
        "labels": [l["name"] for l in node["labels"]["nodes"]],
        "maintainer_responded": bool(maint_events),
        "last_activity_by": last[1] if last else None,
        "handled_by": handlers, "approved_by": approved_by,
    }
    if kind == "issue":
        merged = [s["source"] for s in node["timelineItems"]["nodes"]
                  if s.get("source", {}).get("__typename") == "PullRequest" and s["source"].get("merged")]
        item["merged_prs_referencing"] = [{"number": m["number"], "title": m["title"], "url": m["url"],
                                           "mergedAt": m["mergedAt"]} for m in merged]
    # Category (see module docstring).
    after_maint = last and last_maint and last[0] > last_maint[0] and last[1] not in maintainers
    sec = SECURITY_RE.search(text)
    item["security_terms"] = sec.group(0) if sec else None
    if sec and age <= SECURITY_FRESH_DAYS:
        cat, why = 1, f"possible vulnerability report ('{sec.group(0)}'): check before anything else"
    elif kind == "pr" and external and not maint_events and not item["draft"]:
        cat, why = 2, "external PR with no maintainer review yet"
    elif kind == "issue" and external and not maint_events:
        cat, why = 3, "external issue with no maintainer reply yet"
    elif after_maint and idle < stale_days:
        cat, why = 4, f"@{last[1]} replied after the last maintainer activity"
    elif kind == "pr" and not external and not approved_by and not item["draft"] and not any(
            e[1] != author for e in maint_events):
        cat, why = 5, "co-maintainer PR with no review from another maintainer"
    elif idle >= stale_days:
        cat, why = 6, f"stale: no activity for {idle} days"
    else:
        cat, why = 7, "in progress"
    if handlers and cat in (4, 5):
        why += f" (being handled by @{', @'.join(handlers)})"
    if sec and cat != 1:
        why += f" (mentions '{sec.group(0)}')"
    if cat in (2, 3) and age < no_resp_days:
        why += f" (new: {age}d old)"
    item["category"], item["why"] = cat, why
    return item


def next_step(it) -> str:
    c = it["category"]
    if c == 1:
        return "Open it; follow sensitive-situations.md"
    if c == 2:
        return "Review the PR"
    if c == 3:
        return "Triage and reply"
    if c == 4:
        return "Re-review / reply"
    if c == 5:
        return "Review, or leave to co-maintainers"
    if c == 6:
        if it.get("merged_prs_referencing"):
            return "Close as fixed? Check " + ", ".join(f"#{m['number']}" for m in it["merged_prs_referencing"])
        if it["external"] and not it["maintainer_responded"]:
            return "Answer, then close (default) / needs-info / keep"
        return "Keep, refresh or close"
    return "None needed now"


def to_md(items, total, title) -> str:
    rows = [f"### {title}", "", f"{len(items)} of {total} shown.", "",
            "| # | Item | Age | Type | Author | Why it's here | Suggested next step |",
            "|---|---|---:|---|---|---|---|"]
    for i, it in enumerate(items, 1):
        repo = it["repo"].split("/", 1)[1]
        who = f"@{it['author']}" + (" (ext)" if it["external"] else "")
        kind = "PR" + (" (draft)" if it.get("draft") else "") if it["kind"] == "pr" else "issue"
        rows.append(f"| {i} | [{repo}#{it['number']}]({it['url']}) {it['title'][:60]} | {it['age_days']}d | {kind} | {who} | {it['why']} | {next_step(it)} |")
    return "\n".join(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repos", default=",".join(DEFAULT_REPOS))
    ap.add_argument("--maintainer", default="LesterThomas")
    ap.add_argument("--co-maintainers", default="brian-burton,ferenc-hechler,adarshkumar4,anshulkumar-tmf")
    ap.add_argument("--no-response-days", type=int, default=7)
    ap.add_argument("--stale-days", type=int, default=60)
    ap.add_argument("--limit", type=int, default=15)
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--sweep", action="store_true", help="list open issues for a backlog sweep instead of the queue")
    ap.add_argument("--batch-size", type=int, default=10)
    ap.add_argument("--offset", type=int, default=0)
    a = ap.parse_args()

    me = a.maintainer
    maintainers = {me, *[x for x in a.co_maintainers.split(",") if x]}
    now = dt.datetime.now(dt.timezone.utc)
    items, errors = [], []
    for repo in [r.strip() for r in a.repos.split(",") if r.strip()]:
        try:
            prs, issues = fetch(repo, with_prs=not a.sweep, with_issues=True)
        except GhError as exc:
            errors.append(f"{repo}: {exc}")
            continue
        items += [analyse(repo, n, "pr", me, maintainers, now, a.no_response_days, a.stale_days) for n in prs]
        items += [analyse(repo, n, "issue", me, maintainers, now, a.no_response_days, a.stale_days) for n in issues]

    if a.sweep:
        # Sweep order: unanswered external issues first (oldest), then likely-fixed, then oldest idle.
        items = [i for i in items if i["kind"] == "issue"]
        items.sort(key=lambda i: (0 if (i["external"] and not i["maintainer_responded"]) else
                                  1 if i.get("merged_prs_referencing") else 2, -i["age_days"]))
        batch = items[a.offset:a.offset + a.batch_size]
        for i in batch:
            reasons = []
            if i["external"] and not i["maintainer_responded"]:
                reasons.append("external, never answered")
            if i.get("merged_prs_referencing"):
                reasons.append("referenced by merged " + ", ".join(f"#{m['number']}" for m in i["merged_prs_referencing"]))
            reasons.append(f"idle {i['idle_days']}d")
            if i.get("security_terms"):
                reasons.append(f"mentions '{i['security_terms']}'")
            i["why"] = "; ".join(reasons)
            i["category"] = 1 if i["category"] == 1 else 6
        out = {"mode": "sweep", "total_open_issues": len(items), "offset": a.offset,
               "next_offset": a.offset + len(batch) if a.offset + len(batch) < len(items) else None,
               "batch": batch, "errors": errors}
        title = f"Backlog sweep batch (issues {a.offset + 1}-{a.offset + len(batch)} of {len(items)})"
    else:
        items.sort(key=lambda i: (i["category"], -(i["age_days"] if i["category"] in (2, 3, 6) else -i["idle_days"])))
        batch = items[:a.limit]
        counts = {c: sum(1 for i in items if i["category"] == c) for c in range(1, 8)}
        out = {"mode": "queue", "total_open": len(items), "category_counts": counts, "shown": batch, "errors": errors}
        title = "Maintainer queue"
    if a.format == "json":
        emit(out)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(to_md(batch, len(items), title))
        if not a.sweep:
            names = {1: "security?", 2: "external PRs unreviewed", 3: "external issues unanswered",
                     4: "author replied", 5: "co-maintainer PRs unreviewed", 6: "stale", 7: "in progress"}
            print("\nTotals: " + " · ".join(f"{names[c]} {n}" for c, n in counts.items() if n))
        elif out["next_offset"] is not None:
            print(f"\nNext batch: --sweep --offset {out['next_offset']}")
        for e in errors:
            print(f"\n⚠ {e}")


if __name__ == "__main__":
    main()
