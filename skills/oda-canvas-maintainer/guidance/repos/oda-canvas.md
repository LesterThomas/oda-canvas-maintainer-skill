---
name: repo-oda-canvas
description: Conventions and checks specific to tmforum-oda/oda-canvas, the main ODA Canvas Reference Implementation repo.
last_updated: 2026-09-28
---

# tmforum-oda/oda-canvas

Run `scripts/canvas_pr_checks.py` on every `oda-canvas` PR first. It covers the mechanical checks below and reads the live generator config, so it stays in step with CI. This file explains what each finding means and how to phrase it.

## Where the conventions live

Read these from the repo's current `main` when you need detail. They are the source of truth, so link to them rather than restating them:

- `AGENTS.md`;
- `docs/writing-style.md`;
- `docs/developer/work-with-dockerimages.md`;
- the skills in `skills/`: `helm-chart-development`, `write-bdd-feature`, `create-oda-operator`, `canvas-usecase-documentation`.

## CI

Every PR runs:
- `run_tests_job` (the BDD suite on a cluster; long-running);
- `lint-python-code`;
- `check-pr-does-not-contain-prereleasesuffixes-job`;
- `check_skip_tests_job`;
- `build_badges_job`.

`[skip tests]` in the PR title skips the BDD run. That's fine for docs-only or design-note PRs. For behaviour changes, ask for test evidence (an attached report is fine).

Copilot code review is active. Triage its comments; don't duplicate them.

## Versioning and images

These rules gate merges into **`main`**. For PRs into other branches, such as `feature/ai-canvas-experimental-changes`, the suffix and CI checks don't apply, and the PR gets a Comment, not an approval (see `pr-review.md`). (learned 2026-09-29 from eval review, oda-canvas#601)

This is the most common source of blocking findings.

- **Prerelease suffixes** (for example `LT5`, `-JS3`) are used while developing and **must be empty before merge**. CI fails otherwise, but explain it kindly: "clear the `…PrereleaseSuffix` values before we merge". This is blocking.
- **Operator or service source changed means the image version must be bumped** in the `valuesYamlFile` and `valuesPathVersion` recorded in `automation/generators/dockerbuild-workflow-generator/dockerbuild-config.yaml`. The same version must also be bumped in the sub-chart's own `values.yaml` where it has one (#573). This is blocking.
- **Chart content changed means `Chart.yaml` `version` must be bumped** (at least a patch bump, #516), with a changelog comment in `Chart.yaml`. If a sub-chart version changes, the `canvas-oda` umbrella dependency and `Chart.lock` must follow (`helm dependency update`). This is blocking.
- **Generated workflow files must not be hand-edited.** `.github/workflows/dockerbuild-*.yml` and `check-no-prerelease-suffixes-in-PR.yml` are generated. A new image is added to `dockerbuild-config.yaml`, and the workflows are regenerated as in `docs/developer/work-with-dockerimages.md` (#596). This is blocking.
- **No `:latest` image tags** in charts. This is blocking for new defaults.

## Charts

- **No hard-coded namespaces** in templates. Use `{{ .Release.Namespace }}` or values. This is blocking.
- **Optional dependencies** in the umbrella chart use `condition:`, so they can be switched off. Heavy capabilities stay optional and are not installed by default, which keeps the base Canvas lean (#518).
- **RBAC.** New ClusterRoles should be no broader than the operator needs. Broad RBAC in a genuinely new feature can be a follow-up (#603 → #610), but call it out.

## CRDs, webhooks and the Component model

- **CRD schema changes** (`charts/oda-crds/templates/*crd*.yaml`) must keep **N-2 compatibility** (`v1`, `v1beta4`, `v1beta3`) and update the **webhook conversion** (`source/webhooks/`) when fields are added, renamed or change meaning. A schema change without a webhook change is a `question:` at minimum.
- **CRD descriptions document defaults and interpretation.** For example, a missing `segment` means `coreFunction` (#573).
- **Segment consistency.** Changes to `coreFunction` handling usually also apply to `managementFunction` and `securityFunction` (#581, #573).
- **Sub-resource names** (`ExposedAPI`, `DependentAPI`) are expected to match their definition in the Component. Downstream code relies on this (#573).
- New `apiType` enum values for AI-Native work (for example `mcp` and `a2a`) are aligned by default (see `approval-criteria.md`). Check that they are handled by the relevant API operators and the webhook.
- **`apiType` values name semantic-layer application protocols** (`openapi`, `mcp`, `a2a`, `prometheus`/`openmetrics`), **not transports** such as SSE or WebSockets. If a PR or issue proposes a transport as an `apiType` in order to support a protocol, suggest supporting that protocol as the type instead. *Why:* the `apiType` tells operators what the interface *is*, so they can configure gateways, timeouts and tooling for it. A transport says how bytes move, not what the API means. (learned 2026-09-28 from oda-canvas#612)

## Operators

- Operators follow the kopf patterns, with `source/operators/TMFOP001-Component-Management/component-management/` as the exemplar. Each operator lives in its own `TMFOPnnn-<Name>/` folder.
- The folder layout and a plain `Dockerfile` name follow `skills/create-oda-operator` (#596).
- **Docstrings are required.** They are part of the documentation of the system.
- **Code duplication across segments** is a `suggestion (non-blocking):`. Propose a generic function parameterised by segment (#573).

## BDD and use cases

- Behaviour changes trace to a **use case** (`usecase-library/UCnnn-*.md`) and a **BDD feature** (`feature-definition-and-test-kit/features/UCnnn-Fnnn-*.feature`). Features carry the standard header comment and `@UCnnn` / `@UCnnn-Fnnn` tags, and their steps are implementation-agnostic. The details are in `skills/write-bdd-feature`.
- Test data changes (`feature-definition-and-test-kit/testData/`) must stay valid against the current Component spec.

## Docs

- Follow `docs/writing-style.md` (for example, hyphenate "use-case" in titles).
- Consistency matters more than which variant is used (#567).
- New capabilities should be reachable from the README and design docs. If they aren't, that's usually a follow-up (#598).

## Split-out operators

Work specific to an operator that now has its own repo (ADR-0022), for example events → `TMFOP006-Event-Management`, belongs in that repo, including its BDD features. Old `oda-canvas` issues about it are closed with a pointer, not re-scoped here. (learned 2026-09-28 from oda-canvas backlog sweep #105–#220)

## Scope etiquette

- Lint failures in files the PR didn't change are out of scope for this PR.
- Formatting-only changes belong in their own PR (#596).
- Planning and scratch files from coding agents must be removed (`PLAN-*.md`, #596).

## Change log

- 2026-09-29 — added — versioning and suffix rules apply to PRs into `main` only — Lester's review of the #601 eval runs
- 2026-09-28 — added — split-out operators own their work and BDD features; close old oda-canvas issues with a pointer — Lester, sweep batch 1
- 2026-09-28 — added — `apiType` means a semantic-layer protocol, not a transport; removed `sse` from the examples — Lester's #612 comment, approved in conversation
- 2026-09-28 — added — seed from `AGENTS.md`, the `oda-canvas` skills and workflows, and `research/review-norms.md` §2
