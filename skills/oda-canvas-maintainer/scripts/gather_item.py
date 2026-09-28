"""Gather everything needed to triage an issue or review a PR, as one JSON bundle.

Read-only: every GitHub call goes through _gh.run_gh, which refuses writes.

Usage:
    python gather_item.py <url | owner/repo number | repo number>
        [--maintainer LesterThomas] [--co-maintainers a,b,c]
        [--max-diff-chars 60000] [--max-file-diff-chars 8000] [--no-diff]

Output (stdout, JSON): item metadata, body, conversation, reviews and review
threads (PRs), CI checks, linked items, changed files and a truncated diff,
plus derived fields the skill uses directly:
  - author_is_maintainer / author_prior_merged_prs_in_org (first-timer detection)
  - maintainer_activity: who of the maintainers has engaged, and when
  - waiting_on: "maintainers" or "author", from who spoke last
  - copilot_comments: Copilot review comments, separated for triage
  - attachments: links to uploaded files (e.g. BDD test-report PDFs)
  - posted_by_me: the maintainer's own comments/reviews (learning-loop input)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gh import GhError, emit, graphql, gh_json, parse_target, run_gh  # noqa: E402

COPILOT_LOGINS = {"copilot-pull-request-reviewer", "Copilot", "copilot"}
ATTACH_RE = re.compile(r"https://github\.com/user-attachments/(?:files|assets)/[^\s)\]\"'<>]+")

PR_QUERY = """
query($owner:String!,$name:String!,$number:Int!){
 repository(owner:$owner,name:$name){
  pullRequest(number:$number){
   number title url body state isDraft createdAt updatedAt mergedAt closedAt
   author{login} authorAssociation baseRefName headRefName baseRefOid headRefOid
   additions deletions changedFiles mergeable reviewDecision
   labels(first:30){nodes{name}}
   files(first:100){totalCount nodes{path additions deletions changeType}}
   comments(first:100){totalCount nodes{author{login} body createdAt url}}
   reviews(first:100){totalCount nodes{author{login} state body submittedAt url}}
   reviewThreads(first:100){totalCount nodes{isResolved isOutdated path line
     comments(first:30){nodes{author{login} body createdAt url}}}}
   closingIssuesReferences(first:10){nodes{number title url state}}
   commits(last:1){nodes{commit{oid statusCheckRollup{state
     contexts(first:100){nodes{__typename
       ... on CheckRun{name conclusion status detailsUrl}
       ... on StatusContext{context state targetUrl}}}}}}}
  }}}
"""

ISSUE_QUERY = """
query($owner:String!,$name:String!,$number:Int!){
 repository(owner:$owner,name:$name){
  issue(number:$number){
   number title url body state stateReason createdAt updatedAt closedAt
   author{login} authorAssociation
   labels(first:30){nodes{name}}
   comments(first:100){totalCount nodes{author{login} body createdAt url}}
   timelineItems(first:50,itemTypes:[CROSS_REFERENCED_EVENT,CONNECTED_EVENT]){nodes{
     __typename
     ... on CrossReferencedEvent{createdAt source{__typename
        ... on PullRequest{number title url state merged}
        ... on Issue{number title url state}}}
     ... on ConnectedEvent{createdAt subject{__typename
        ... on PullRequest{number title url state merged}}}}}
  }}}
"""

THREAD_QUERY = """
query($owner:String!,$name:String!,$number:Int!){
 repository(owner:$owner,name:$name){ issueOrPullRequest(number:$number){ __typename
  ... on Issue{number title url state body author{login} comments(first:100){totalCount nodes{author{login} body createdAt url}}}
  ... on PullRequest{number title url state body author{login} comments(first:100){totalCount nodes{author{login} body createdAt url}}}
 } } }
"""

REF_RE = re.compile(r"(?:(?<![\w/])#(\d+)\b|github\.com/([\w.-]+)/([\w.-]+)/(?:issues|pull)/(\d+))")

KIND_QUERY = """
query($owner:String!,$name:String!,$number:Int!){
 repository(owner:$owner,name:$name){ issueOrPullRequest(number:$number){ __typename } } }
"""


def login(node) -> str:
    return (node.get("author") or {}).get("login") or "ghost"


# Files whose diffs are rarely worth review budget; listed as skipped instead.
SKIP_DIFF_RE = re.compile(r"(^|/)(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|Chart\.lock|poetry\.lock|uv\.lock)$|\.min\.(js|css)$|\.(svg|png|jpg|pdf)$")


def truncate_diff(diff: str, max_total: int, max_file: int) -> tuple[str, dict]:
    """Keep the diff within budget; report exactly which files were clipped, omitted or skipped."""
    parts = re.split(r"(?m)^(?=diff --git )", diff)
    out, total = [], 0
    report = {"clipped": [], "omitted": [], "skipped": []}
    for part in parts:
        if not part:
            continue
        m = re.match(r"diff --git a/(\S+)", part)
        path = m.group(1) if m else "?"
        if SKIP_DIFF_RE.search(path):
            report["skipped"].append(path)
            continue
        if len(part) > max_file:
            part = part[:max_file] + f"\n... [file diff truncated at {max_file} chars]\n"
            report["clipped"].append(path)
        if total + len(part) > max_total:
            report["omitted"].append(path)
            if path in report["clipped"]:
                report["clipped"].remove(path)
            continue
        out.append(part)
        total += len(part)
    return "".join(out), report


def linked_threads(owner: str, name: str, number: int, texts: list[str], extra: list[int],
                   maintainers: set[str], limit: int = 8) -> list[dict]:
    """Full comment threads of associated issues/PRs: closing issues plus #refs and same-org links in the text."""
    refs: list[tuple[str, str, int]] = [(owner, name, n) for n in extra]
    for t in texts:
        for m in REF_RE.finditer(t or ""):
            if m.group(1):
                refs.append((owner, name, int(m.group(1))))
            elif m.group(2) == owner:
                refs.append((m.group(2), m.group(3), int(m.group(4))))
    seen, out = set(), []
    for ref in refs:
        if ref in seen or ref == (owner, name, number):
            continue
        seen.add(ref)
        if len(out) >= limit:
            out.append({"note": f"more references not fetched (limit {limit})"})
            break
        try:
            node = graphql(THREAD_QUERY, owner=ref[0], name=ref[1], number=ref[2])["repository"]["issueOrPullRequest"]
        except GhError:
            continue
        if not node:
            continue
        out.append({
            "repo": f"{ref[0]}/{ref[1]}", "number": node["number"], "type": node["__typename"],
            "title": node["title"], "url": node["url"], "state": node["state"],
            "author": login(node), "body": node.get("body") or "",
            "comments": [{"author": login(c), "is_maintainer": login(c) in maintainers,
                          "createdAt": c["createdAt"], "body": c["body"], "url": c["url"]}
                         for c in node["comments"]["nodes"]],
            "comments_truncated": node["comments"]["totalCount"] > len(node["comments"]["nodes"]),
        })
    return out


def prior_merged_prs(author: str, org: str) -> int | None:
    try:
        data = gh_json(["api", "-X", "GET", "search/issues",
                        "-f", f"q=is:pr is:merged author:{author} org:{org}", "-f", "per_page=1"])
        return data.get("total_count")
    except GhError:
        return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("target", nargs="+")
    ap.add_argument("--maintainer", default="LesterThomas")
    ap.add_argument("--co-maintainers", default="brian-burton,ferenc-hechler,adarshkumar4,anshulkumar-tmf")
    ap.add_argument("--max-diff-chars", type=int, default=60000)
    ap.add_argument("--max-file-diff-chars", type=int, default=8000)
    ap.add_argument("--no-diff", action="store_true")
    a = ap.parse_args()

    owner, name, number = parse_target(a.target)
    me = a.maintainer
    co = [x for x in a.co_maintainers.split(",") if x]
    maintainers = {me, *co}

    try:
        kind = graphql(KIND_QUERY, owner=owner, name=name, number=number)["repository"]["issueOrPullRequest"]
        if not kind:
            raise SystemExit(f"{owner}/{name}#{number} not found")
        is_pr = kind["__typename"] == "PullRequest"
        node = graphql(PR_QUERY if is_pr else ISSUE_QUERY, owner=owner, name=name, number=number)["repository"][
            "pullRequest" if is_pr else "issue"]
    except GhError as exc:
        raise SystemExit(str(exc))

    author = login(node)
    comments = [{"author": login(c), "is_maintainer": login(c) in maintainers, "createdAt": c["createdAt"],
                 "body": c["body"], "url": c["url"]}
                for c in node["comments"]["nodes"]]
    result = {
        "repo": f"{owner}/{name}", "number": number, "kind": "pr" if is_pr else "issue",
        "title": node["title"], "url": node["url"], "state": node["state"],
        "createdAt": node["createdAt"], "updatedAt": node["updatedAt"], "closedAt": node.get("closedAt"),
        "author": author, "authorAssociation": node.get("authorAssociation"),
        "author_is_maintainer": author in maintainers,
        "labels": [l["name"] for l in node["labels"]["nodes"]],
        "body": node.get("body") or "",
        "comments": comments,
        "truncation": {"comments": node["comments"]["totalCount"] > len(comments)},
    }

    events = [(c["createdAt"], c["author"], "comment", c["body"]) for c in comments]
    reviews, threads, copilot = [], [], []

    if is_pr:
        result.update({
            "isDraft": node["isDraft"], "mergedAt": node.get("mergedAt"),
            "base": node["baseRefName"], "head": node["headRefName"],
            "baseOid": node["baseRefOid"], "headOid": node["headRefOid"],
            "additions": node["additions"], "deletions": node["deletions"],
            "changedFiles": node["changedFiles"], "mergeable": node["mergeable"],
            "reviewDecision": node["reviewDecision"],
            "files": node["files"]["nodes"],
            "closingIssues": node["closingIssuesReferences"]["nodes"],
        })
        result["truncation"]["files"] = node["files"]["totalCount"] > len(node["files"]["nodes"])
        for r in node["reviews"]["nodes"]:
            rv = {"author": login(r), "state": r["state"], "submittedAt": r["submittedAt"], "body": r["body"], "url": r["url"]}
            reviews.append(rv)
            events.append((r["submittedAt"], rv["author"], f"review:{r['state']}", r["body"]))
            if rv["author"] in COPILOT_LOGINS and r["body"].strip():
                copilot.append({"kind": "review", **rv})
        for t in node["reviewThreads"]["nodes"]:
            tc = [{"author": login(c), "createdAt": c["createdAt"], "body": c["body"], "url": c["url"]}
                  for c in t["comments"]["nodes"]]
            threads.append({"path": t["path"], "line": t["line"], "isResolved": t["isResolved"],
                            "isOutdated": t["isOutdated"], "comments": tc})
            for c in tc:
                events.append((c["createdAt"], c["author"], "inline", c["body"]))
            if tc and tc[0]["author"] in COPILOT_LOGINS:
                copilot.append({"kind": "inline", "path": t["path"], "line": t["line"],
                                "isResolved": t["isResolved"], "body": tc[0]["body"],
                                "replies": [c for c in tc[1:]]})
        result["reviews"] = reviews
        result["reviewThreads"] = threads
        result["unresolvedThreads"] = sum(1 for t in threads if not t["isResolved"] and not t["isOutdated"])
        rollup = (node["commits"]["nodes"] or [{}])[0].get("commit", {}).get("statusCheckRollup") or {}
        checks = []
        for c in (rollup.get("contexts") or {}).get("nodes", []):
            if c["__typename"] == "CheckRun":
                checks.append({"name": c["name"], "status": c["status"], "conclusion": c["conclusion"], "url": c["detailsUrl"]})
            else:
                checks.append({"name": c["context"], "status": "COMPLETED", "conclusion": c["state"], "url": c["targetUrl"]})
        result["checks"] = {"overall": rollup.get("state"), "runs": checks,
                            "failing": [c["name"] for c in checks if (c["conclusion"] or "") in ("FAILURE", "ERROR", "TIMED_OUT", "CANCELLED", "ACTION_REQUIRED")],
                            "pending": [c["name"] for c in checks if c["status"] not in ("COMPLETED",) and not c["conclusion"]]}
        result["copilot_comments"] = copilot
        if not a.no_diff:
            try:
                diff = run_gh(["pr", "diff", str(number), "-R", f"{owner}/{name}"])
                d, rep = truncate_diff(diff, a.max_diff_chars, a.max_file_diff_chars)
                result["diff"] = d
                result["truncation"]["diff"] = bool(rep["clipped"] or rep["omitted"])
                result["truncation"]["diff_files"] = rep
                if rep["omitted"]:
                    result["truncation"]["diff_hint"] = ("Some file diffs were omitted to stay within budget. Fetch them "
                        f"individually if needed: gh api -X GET repos/{owner}/{name}/pulls/{number}/files --paginate")
            except GhError as exc:
                result["diff"] = ""
                result["truncation"]["diff_error"] = str(exc)
    else:
        result["stateReason"] = node.get("stateReason")
        linked = []
        for ev in node["timelineItems"]["nodes"]:
            src = ev.get("source") or ev.get("subject") or {}
            if src.get("number"):
                linked.append({"type": src["__typename"], "number": src["number"], "title": src.get("title"),
                               "url": src.get("url"), "state": src.get("state"), "merged": src.get("merged"),
                               "at": ev.get("createdAt")})
        result["linkedItems"] = linked

    # Derived fields.
    events.sort(key=lambda e: e[0] or "")
    human = [e for e in events if e[1] not in COPILOT_LOGINS and not e[1].endswith("[bot]")]
    result["maintainer_activity"] = {
        m: {"count": sum(1 for e in human if e[1] == m),
            "last": max((e[0] for e in human if e[1] == m), default=None),
            "approved": any(r["author"] == m and r["state"] == "APPROVED" for r in reviews)}
        for m in sorted(maintainers) if any(e[1] == m for e in human)
    }
    last = human[-1] if human else None
    if not last:
        result["waiting_on"] = "maintainers (no human response yet)" if not result["author_is_maintainer"] else "nobody (no discussion yet)"
    elif last[1] == author:
        result["waiting_on"] = "maintainers" if not result["author_is_maintainer"] else "reviewers"
    elif last[1] in maintainers:
        result["waiting_on"] = "author"
    else:
        result["waiting_on"] = f"unclear (last: @{last[1]})"
    result["last_human_activity"] = {"at": last[0], "by": last[1], "kind": last[2]} if last else None

    # Associated issues/PRs with their full discussions (decisions often live there, not in the title).
    extra = [i["number"] for i in result.get("closingIssues", [])]
    extra += [i["number"] for i in result.get("linkedItems", []) if i.get("type") == "Issue"]
    result["linked_issue_threads"] = linked_threads(owner, name, number, [node["title"], result["body"]],
                                                    extra, maintainers)
    result["maintainer_comments_in_linked_threads"] = [
        {"item": t["number"], "author": c["author"], "createdAt": c["createdAt"], "body": c["body"]}
        for t in result["linked_issue_threads"] if "comments" in t for c in t["comments"] if c["is_maintainer"]]

    texts = [result["body"]] + [e[3] or "" for e in events]
    result["attachments"] = sorted({u for t in texts for u in ATTACH_RE.findall(t)})
    result["posted_by_me"] = [{"at": e[0], "kind": e[2], "body": e[3]} for e in events if e[1] == me]
    if not result["author_is_maintainer"]:
        result["author_prior_merged_prs_in_org"] = prior_merged_prs(author, owner)
    emit(result)


if __name__ == "__main__":
    main()
