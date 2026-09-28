"""Shared, read-only helpers for calling the GitHub CLI.

Every script in this skill goes through ``run_gh`` so the read-only guarantee
is enforced in one place: any ``gh`` subcommand that could write to GitHub is
refused before it runs, and ``gh api`` is only allowed with GET (GraphQL
queries are allowed; GraphQL mutations are refused).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

# gh subcommands (first two words) that only read.
_READ_ONLY = {
    ("issue", "view"), ("issue", "list"),
    ("pr", "view"), ("pr", "list"), ("pr", "diff"), ("pr", "checks"),
    ("repo", "view"), ("run", "view"), ("run", "list"),
    ("search", "issues"), ("search", "prs"), ("label", "list"),
    ("auth", "status"),
}


class GhError(RuntimeError):
    pass


def _check_read_only(args: list[str]) -> None:
    if not args:
        raise GhError("empty gh command")
    if args[0] == "api":
        method = "GET"
        for i, a in enumerate(args):
            if a in ("-X", "--method") and i + 1 < len(args):
                method = args[i + 1].upper()
            elif a.startswith("--method="):
                method = a.split("=", 1)[1].upper()
        if method != "GET":
            raise GhError(f"refusing non-GET gh api call ({method}): this skill is read-only")
        if len(args) > 1 and args[1] == "graphql":
            query = " ".join(a for a in args if a.startswith("query="))
            if re.search(r"\bmutation\b", query):
                raise GhError("refusing GraphQL mutation: this skill is read-only")
        # `gh api` with -f/-F on a REST path implies POST unless --method GET is given.
        if len(args) > 1 and args[1] != "graphql" and any(a in ("-f", "-F", "--field", "--raw-field") for a in args):
            if not any(a in ("-X", "--method") or a.startswith("--method=") for a in args):
                raise GhError("refusing gh api REST call with fields but no explicit --method GET")
        return
    if tuple(args[:2]) not in _READ_ONLY:
        raise GhError(f"refusing gh {' '.join(args[:2])}: not in the read-only allowlist")


def run_gh(args: list[str], *, check: bool = True) -> str:
    """Run a read-only gh command and return stdout as text."""
    _check_read_only(args)
    try:
        proc = subprocess.run(
            ["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
    except FileNotFoundError as exc:
        raise GhError("the GitHub CLI `gh` is not installed or not on PATH") from exc
    if check and proc.returncode != 0:
        msg = proc.stderr.strip() or proc.stdout.strip()
        if "auth login" in msg or "authentication" in msg.lower():
            msg += "\nHint: run `gh auth login` (or `gh auth status` to check)."
        raise GhError(f"gh {' '.join(args[:3])} failed: {msg}")
    return proc.stdout


def gh_json(args: list[str]):
    out = run_gh(args)
    return json.loads(out) if out.strip() else None


def graphql(query: str, **variables) -> dict:
    args = ["api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    data = gh_json(args)
    if data.get("errors"):
        raise GhError(f"GraphQL errors: {data['errors']}")
    return data["data"]


_URL_RE = re.compile(r"github\.com/([^/\s]+)/([^/\s]+)/(issues|pull)/(\d+)")


def parse_target(target: list[str]) -> tuple[str, str, int]:
    """Accept `<url>`, `<owner/repo> <n>`, `<owner/repo>#<n>` or `<repo> <n>` (owner defaults to tmforum-oda)."""
    joined = " ".join(target)
    m = _URL_RE.search(joined)
    if m:
        return m.group(1), m.group(2), int(m.group(4))
    m = re.match(r"^\s*([\w.-]+/)?([\w.-]+)\s*(?:#|\s)\s*(\d+)\s*$", joined)
    if m:
        owner = (m.group(1) or "tmforum-oda/").rstrip("/")
        return owner, m.group(2), int(m.group(3))
    raise SystemExit(f"cannot parse target {joined!r}; use a GitHub URL or '<owner/repo> <number>'")


def emit(obj) -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    json.dump(obj, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
