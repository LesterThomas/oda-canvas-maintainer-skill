"""Deterministic checks for tmforum-oda/oda-canvas pull requests.

Read-only. Emits JSON findings with evidence; the model decides how to phrase
them (see guidance/repos/oda-canvas.md). Checks:

  prerelease-suffix           non-empty *PrereleaseSuffix at the PR head (same keys CI checks,
                              read from the generator config so it can't drift)
  image-version-not-bumped    image source changed but its version in values.yaml unchanged
  chart-version-not-bumped    files under charts/<chart>/ changed but Chart.yaml version unchanged
  chart-changelog-missing     Chart.yaml version bumped without a changelog comment
  umbrella-dependency-stale   sub-chart version bumped but canvas-oda's dependency not updated
  hardcoded-namespace         literal namespace: in added chart template lines
  crd-without-webhook         CRD templates changed with no change under source/webhooks/
  generated-workflow-edited   generated workflow files changed without the generator config
  dependency-added            new dependency lines (ask-first area)
  latest-tag                  ':latest' / tag: latest in added lines
  stray-artefact              planning/scratch/odd files added (e.g. PLAN-*.md, a file named '-w')
  possible-reformat           large near-symmetric Python diffs (formatting churn hides logic)

Usage:
    python canvas_pr_checks.py <url | [owner/]repo number>
"""

from __future__ import annotations

import base64
import json
import re
import sys
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gh import GhError, emit, gh_json, parse_target, run_gh  # noqa: E402

GEN_CONFIG = "automation/generators/dockerbuild-workflow-generator/dockerbuild-config.yaml"
GENERATED_WF_RE = re.compile(r"^\.github/workflows/(dockerbuild-.*\.ya?ml|check-no-prerelease-suffixes-in-PR\.ya?ml)$")
DEP_FILE_RE = re.compile(r"(^|/)(requirements[^/]*\.txt|package\.json|pom\.xml|pyproject\.toml|go\.mod)$")
STRAY_RE = re.compile(r"^(PLAN[-_].*\.md|.*\.orig|.*\.rej|.*\.bak|\.DS_Store|Thumbs\.db|-.*|.*\.log|nohup\.out)$", re.I)


# ---------- GitHub access ----------

class Repo:
    def __init__(self, owner: str, name: str):
        self.slug = f"{owner}/{name}"
        self._cache: dict[tuple[str, str], str | None] = {}

    def file_at(self, path: str, ref: str) -> str | None:
        key = (path, ref)
        if key not in self._cache:
            try:
                data = gh_json(["api", "-X", "GET", f"repos/{self.slug}/contents/{path}", "-f", f"ref={ref}"])
                self._cache[key] = base64.b64decode(data["content"]).decode("utf-8", "replace") if data and "content" in data else None
            except GhError:
                self._cache[key] = None
        return self._cache[key]


# ---------- tiny YAML helpers (stdlib only; enough for values/Chart/generator files) ----------

def _strip_value(v: str) -> str:
    v = re.sub(r"\s+#.*$", "", v).strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        v = v[1:-1]
    return v


def yaml_get(text: str | None, dotted: str) -> str | None:
    """Look up a scalar by a dotted mapping path like `.component-operator.deployment.compopVersion`."""
    if text is None:
        return None
    keys = [k for k in dotted.strip().lstrip(".").split(".") if k]
    lines = text.splitlines()
    start, end, parent_indent = 0, len(lines), -1
    for depth, key in enumerate(keys):
        found = None
        child_indent = None
        for i in range(start, end):
            raw = lines[i]
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            ind = len(raw) - len(raw.lstrip(" "))
            if ind <= parent_indent:
                end = i
                break
            if child_indent is None:
                child_indent = ind
            if ind != child_indent:
                continue
            m = re.match(r"^\s*([\"']?)([^:\"']+)\1\s*:(.*)$", raw)
            if m and m.group(2).strip() == key:
                found = (i, ind, m.group(3))
                break
        if not found:
            return None
        i, ind, rest = found
        if depth == len(keys) - 1:
            return _strip_value(rest)
        start, parent_indent = i + 1, ind
        end = len(lines)
        for j in range(start, len(lines)):
            r = lines[j]
            if r.strip() and not r.lstrip().startswith("#") and len(r) - len(r.lstrip(" ")) <= ind:
                end = j
                break
    return None


def parse_generator_config(text: str) -> list[dict]:
    """Parse dockerbuild-config.yaml: top-level image keys with scalar fields and a `paths:` list."""
    images, cur, in_paths = [], None, False
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if not raw.startswith((" ", "\t")):
            m = re.match(r"^([^:#]+?)\s*:\s*$", raw)
            if m:
                cur = {"name": m.group(1).strip(), "paths": []}
                images.append(cur)
                in_paths = False
            continue
        if cur is None:
            continue
        s = raw.strip()
        if s.startswith("- ") and in_paths:
            cur["paths"].append(_strip_value(s[2:]))
            continue
        m = re.match(r"^([\w-]+)\s*:\s*(.*)$", s)
        if m:
            in_paths = m.group(1) == "paths" and not m.group(2).strip()
            if not in_paths:
                cur[m.group(1)] = _strip_value(m.group(2))
    return images


def chart_deps(text: str | None) -> dict[str, str]:
    """name -> version for `dependencies:` entries in a Chart.yaml."""
    deps, cur = {}, None
    if not text:
        return deps
    in_deps = False
    for raw in text.splitlines():
        if re.match(r"^dependencies\s*:", raw):
            in_deps = True
            continue
        if in_deps and raw and not raw.startswith((" ", "-", "\t")) and not raw.startswith("#"):
            break
        if not in_deps:
            continue
        s = raw.strip()
        m = re.match(r"^-?\s*name\s*:\s*(.+)$", s)
        if m:
            cur = _strip_value(m.group(1))
            continue
        m = re.match(r"^version\s*:\s*(.+)$", s)
        if m and cur:
            deps[cur] = _strip_value(m.group(1))
    return deps


# ---------- diff helpers ----------

def added_lines(patch: str | None):
    """Yield (new_line_number, text) for added lines in a unified diff patch."""
    if not patch:
        return
    new_ln = 0
    for line in patch.splitlines():
        m = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if m:
            new_ln = int(m.group(1))
            continue
        if line.startswith("+") and not line.startswith("+++"):
            yield new_ln, line[1:]
            new_ln += 1
        elif line.startswith("-"):
            continue
        else:
            new_ln += 1


# Changes under these paths don't go into an image, so they never require a version bump.
NON_IMAGE_RE = re.compile(r"(^|/)(tests?|manual_test|docs?)/|\.md$|(^|/)test_[^/]*\.py$|_test\.py$")


def path_matches(path: str, pattern: str) -> bool:
    """GitHub Actions `paths` semantics: `*` does not cross `/`, so this mirrors what triggers an image build."""
    rx = "^" + re.escape(pattern).replace(r"\*\*", ".*").replace(r"\*", "[^/]*") + "$"
    return re.match(rx, path) is not None


# ---------- main ----------

def main() -> None:
    owner, name, number = parse_target(sys.argv[1:] or ["--help"])
    repo = Repo(owner, name)
    try:
        pr = gh_json(["pr", "view", str(number), "-R", repo.slug, "--json", "headRefOid,baseRefOid,baseRefName,title,isCrossRepository"])
        files = [json.loads(l) for l in run_gh(["api", "-X", "GET", f"repos/{repo.slug}/pulls/{number}/files",
                                                  "-f", "per_page=100", "--paginate", "--jq", ".[]"]).splitlines() if l.strip()]
    except GhError as exc:
        raise SystemExit(str(exc))

    head, base = pr["headRefOid"], pr["baseRefOid"]
    base_branch = pr["baseRefName"]
    # Suffix/version rules gate merges into main. For other branches they are informational only.
    into_main = base_branch == "main"
    gate = "blocking" if into_main else "info"
    changed = {f["filename"]: f for f in files}
    findings: list[dict] = []
    not_checked: list[str] = []

    def add(check, severity, message, file=None, line=None, evidence=None):
        findings.append({k: v for k, v in dict(check=check, severity=severity, file=file, line=line,
                                                  evidence=evidence, message=message).items() if v is not None})

    # --- generator-config driven checks: suffixes + image version bumps ---
    gen_text = repo.file_at(GEN_CONFIG, base)
    images = parse_generator_config(gen_text) if gen_text else []
    if not images:
        not_checked.append(f"prerelease-suffix / image-version-not-bumped: could not read {GEN_CONFIG}")
    seen_suffix = set()
    for img in images:
        vfile = img.get("valuesYamlFile")
        if not vfile:
            continue
        spath = img.get("valuesPathPrereleaseSuffix")
        if into_main and spath and (vfile, spath) not in seen_suffix:
            seen_suffix.add((vfile, spath))
            val = yaml_get(repo.file_at(vfile, head), spath)
            if val:
                add("prerelease-suffix", "blocking",
                    f"Prerelease suffix '{val}' is set for {img['name']}; it must be cleared before merging to main (CI job check-pr-does-not-contain-prereleasesuffixes-job).",
                    file=vfile, evidence=f"{spath}: {val}")
        vpath = img.get("valuesPathVersion")
        touched = [p for p in changed if not NON_IMAGE_RE.search(p)
                   and any(path_matches(p, pat) for pat in img.get("paths", []))]
        if touched and vpath:
            old, new = yaml_get(repo.file_at(vfile, base), vpath), yaml_get(repo.file_at(vfile, head), vpath)
            if old is not None and old == new:
                add("image-version-not-bumped", gate,
                    f"Source for image {img['name']} changed but its version is still {new}; bump {vpath} in {vfile} (and the sub-chart values.yaml if it has its own copy).",
                    file=vfile, evidence=f"changed: {', '.join(touched[:5])}{' …' if len(touched) > 5 else ''}")

    # --- chart version bumps ---
    charts_changed: dict[str, list[str]] = {}
    for p in changed:
        parts = PurePosixPath(p).parts
        if len(parts) >= 3 and parts[0] == "charts":
            chart_dir = "/".join(parts[:3]) if parts[1] == "experimental" and len(parts) >= 4 else "/".join(parts[:2])
            charts_changed.setdefault(chart_dir, []).append(p)
    bumped: dict[str, tuple[str, str]] = {}
    for cdir, paths in sorted(charts_changed.items()):
        cy = f"{cdir}/Chart.yaml"
        base_cy, head_cy = repo.file_at(cy, base), repo.file_at(cy, head)
        if head_cy is None:
            continue  # chart deleted
        if base_cy is None:
            continue  # new chart: nothing to bump
        old, new = yaml_get(base_cy, "version"), yaml_get(head_cy, "version")
        cname = yaml_get(head_cy, "name") or cdir.split("/")[-1]
        if old == new:
            substantive = [x for x in paths if "/templates/" in x or "/crds/" in x
                           or x.endswith(("Chart.yaml", "_helpers.tpl"))]
            if substantive:
                add("chart-version-not-bumped", gate,
                    f"Chart content in {cdir}/ changed but Chart.yaml version is still {new}; bump at least the patch version and add a changelog comment.",
                    file=cy, evidence=f"changed: {', '.join(substantive[:5])}{' …' if len(substantive) > 5 else ''}")
            else:
                add("chart-version-not-bumped", "question",
                    f"Only values/schema files changed in {cdir}/ and Chart.yaml is still {new}. Is a patch bump needed (e.g. new image versions or defaults)?",
                    file=cy, evidence=f"changed: {', '.join(paths[:5])}{' …' if len(paths) > 5 else ''}")
        else:
            bumped[cname] = (old, new)
            patch = (changed.get(cy) or {}).get("patch")
            if not any(t.lstrip().startswith("#") and new in t for _, t in added_lines(patch)):
                add("chart-changelog-missing", "non-blocking",
                    f"{cy} version bumped {old} -> {new} without a changelog comment mentioning {new}.", file=cy)
    if bumped:
        umb = "charts/canvas-oda/Chart.yaml"
        deps = chart_deps(repo.file_at(umb, head))
        for cname, (old, new) in bumped.items():
            if cname in deps and deps[cname] != new:
                add("umbrella-dependency-stale", gate,
                    f"Sub-chart {cname} is now {new} but {umb} still depends on {deps[cname]}; update it and run `helm dependency update`.",
                    file=umb, evidence=f"{cname}: {deps[cname]}")

    # --- line-level checks on added lines ---
    for p, f in changed.items():
        patch = f.get("patch")
        if (patch is None and f.get("status") != "removed"
                and not re.search(r"\.(png|jpe?g|gif|svg|pdf|ico)$", p, re.I)):
            not_checked.append(f"line checks: no patch for {p} (binary or too large)")
        in_templates = p.startswith("charts/") and "/templates/" in p
        # Generated workflows legitimately publish a moving :latest tag, and docs mention it in prose.
        latest_skip = p.startswith(".github/workflows/") or p.endswith((".md", ".txt"))
        fname = PurePosixPath(p).name.lower()
        latest_strict = p.startswith("charts/") or fname.startswith("dockerfile") or fname.endswith("-dockerfile")
        for ln, text in added_lines(patch):
            if in_templates:
                m = re.match(r"^\s*namespace\s*:\s*(\S+)", text)
                if m and "{{" not in m.group(1):
                    add("hardcoded-namespace", "blocking",
                        "Hard-coded namespace in a chart template; use {{ .Release.Namespace }} or a value.",
                        file=p, line=ln, evidence=text.strip())
            if (not latest_skip and re.search(r":latest\b|\btag\s*:\s*[\"']?latest\b", text)
                    and not text.lstrip().startswith("#")):
                add("latest-tag", "issue" if latest_strict else "non-blocking",
                    "Uses a 'latest' image tag; pin a version so installs are reproducible.",
                    file=p, line=ln, evidence=text.strip())
        if DEP_FILE_RE.search(p) and f.get("status") != "removed":
            added_ = [t.strip() for _, t in added_lines(patch)]
            if p.endswith("package.json"):
                new_deps = [t.rstrip(",") for t in added_ if re.match(r'^"[@\w./-]+"\s*:\s*"[\^~>=<*]?\d', t)
                            and not t.startswith('"version"')]
            elif p.endswith("pom.xml"):
                new_deps = [re.sub(r"</?artifactId>", "", t) for t in added_ if t.startswith("<artifactId>")]
            else:
                new_deps = [t for t in added_ if t and not t.startswith(("#", "//", "[", "}"))]
            if new_deps:
                add("dependency-added", "info",
                    "Dependency file changed (ask-first area): check each new dependency is needed, maintained and Apache-2.0 compatible.",
                    file=p, evidence=("new file; " if f.get("status") == "added" else "") + "; ".join(new_deps[:10])
                    + (f" (+{len(new_deps) - 10} more)" if len(new_deps) > 10 else ""))
        base_name = PurePosixPath(p).name
        if f.get("status") == "added" and STRAY_RE.match(base_name):
            add("stray-artefact", "blocking",
                "Looks like a planning/scratch/accidental file; remove it from the PR.", file=p)
        if p.endswith(".py") and f.get("additions", 0) > 100:
            a_, d_ = f["additions"], f.get("deletions", 0)
            if d_ and abs(a_ - d_) / max(a_, d_) < 0.15:
                add("possible-reformat", "non-blocking",
                    f"{a_} additions / {d_} deletions: this looks like reformatting mixed with logic changes, which makes review hard. Suggest a separate formatting PR.",
                    file=p)

    # --- file-set checks ---
    crd = [p for p in changed if p.startswith("charts/oda-crds/templates/")]
    if crd and not any(p.startswith("source/webhooks/") for p in changed):
        add("crd-without-webhook", "question",
            "CRD templates changed without any change under source/webhooks/. Is webhook conversion affected (N-2 support: v1, v1beta4, v1beta3)?",
            evidence=", ".join(crd))
    gen = [p for p in changed if GENERATED_WF_RE.match(p)]
    if gen and GEN_CONFIG not in changed:
        add("generated-workflow-edited", "blocking",
            f"Generated workflow files changed without changing {GEN_CONFIG}; add the image to the generator config and regenerate (docs/developer/work-with-dockerimages.md).",
            evidence=", ".join(gen))
    elif gen:
        add("generated-workflow-edited", "info",
            "Generated workflows changed together with the generator config; check they were regenerated, not hand-edited.",
            evidence=", ".join(gen))

    order = {"blocking": 0, "issue": 1, "question": 2, "non-blocking": 3, "info": 4}
    findings.sort(key=lambda x: (order.get(x["severity"], 9), x["check"]))
    if not into_main:
        not_checked.insert(0, f"prerelease-suffix: skipped (PR targets '{base_branch}', not main); version checks downgraded to info")
    emit({"repo": repo.slug, "number": number, "title": pr["title"], "base_branch": base_branch,
          "into_main": into_main, "base": base, "head": head,
          "files_changed": len(changed), "findings": findings,
          "summary": {s: sum(1 for f in findings if f["severity"] == s) for s in order},
          "not_checked": not_checked,
          "note": "Deterministic checks only. Alignment, correctness and quality still need review."})


if __name__ == "__main__":
    main()
