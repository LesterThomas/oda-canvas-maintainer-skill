---
name: repo-canvas-operator-repos
description: Shared conventions for the standalone Canvas operator repos (TMFOPnnn-* and TMFCOPnnn-*), which are split out of oda-canvas under ADR-0022.
applies_to: ["tmforum-oda/TMFOP*", "tmforum-oda/TMFCOP*"]
last_updated: 2026-09-28
---

# Standalone Canvas operator repos (TMFOPnnn / TMFCOPnnn)

These repos hold Canvas operators developed outside `oda-canvas`, following ADR-0022 (modular and independent operators). Examples are `TMFOP006-Event-Management`, `TMFCOP009-model-as-a-service-operator` and `TMFOP012-data-products-lifecycle-management-operator`. They are young and have little process: README and LICENSE only, no CI, no CONTRIBUTING, and GitHub's default labels.

**Load `repos/oda-canvas.md` as well.** Its operator, CRD and chart rules apply here too, except where this file says otherwise. The generator-config and prerelease-suffix checks do **not** apply, because these repos have no such config. Don't run `canvas_pr_checks.py` on them.

## Checks

- **No CI means nothing is verified automatically.** The brief must say so under "Not verified". Ask for test evidence in the PR, either BDD output or a report. TMFOP012 has a `test/bdd/` suite with `run_bdd.sh`.
- **Operator shape.** Python kopf operators should follow the `oda-canvas` exemplar (`TMFOP001` component operator), with docstrings, a `Dockerfile`, and a Helm chart under `charts/<name>/` with RBAC no broader than needed.
- **CRDs.** A new CRD (e.g. `crds/dataresourceconfig-crd.yaml`) is an architecture addition:
  - check that an ADR covers the capability (ADRs 0015–0020 cover much of the AI-Native work);
  - check the API group and versioning follow the ODA pattern (`oda.tmforum.org`, versioned);
  - a CRD for a capability no ADR covers → suggest an ADR.
- **Integration with the Canvas.** The operator should work from Component declarations and Canvas services, such as the Service Inventory, dependent APIs and the AI Gateway. It should not work through side channels. The alignment tests in `approval-criteria.md` apply in full.
- **Demo code vs product code.** Several repos target DTW demos (e.g. TMFOP012's demo agent). Demo assets are fine, but they should be clearly separated (for example in `demo-app/`) and not required by the operator.
- **Vendor specifics.** Operators wrapping a vendor product (e.g. Databricks in TMFOP012) are fine as *one implementation* of a capability. The CRD and Component declarations should stay vendor-neutral where the design has a pluggable slot.

## Licences

- `TMFOP006` is Apache-2.0, which is in line with the policy.
- **Policy: `TMFOPnnn` repos are Apache-2.0** (see `sensitive-situations.md`). `TMFOP012` currently carries a TM Forum RAND notice, so it is out of line and should get the Apache-2.0 LICENSE. `TMFCOP009` also carries RAND, and its PR #1 proposes Apache-2.0 → RAND. Whether `TMFCOPnnn` repos are covered is to be confirmed, so escalate that PR. (learned 2026-09-28 in conversation)
- `oda-canvas` is Apache-2.0.

A PR that moves a repo *towards* Apache-2.0 is a normal PR. Moves *away* from it, and code copied between repos with different licences, are escalations (see `sensitive-situations.md` → Licensing).

## Repo notes

- **TMFCOP009-model-as-a-service-operator:** `model-as-a-service-crds` is being merged into this repo, so MaaS CRD changes are reviewed here. The README title still says `canvas-ai-operator`.
- **TMFOP012-data-products-lifecycle-management-operator:** the README title says `TMFCOP012`, but the repo is `TMFOP012`. PR #1 was self-merged by its author, which is normal for maintainers.
- **TMFOP006-Event-Management:** the repo is empty apart from the README and LICENSE. The first PRs will set its conventions, so review them with that in mind.

## Change log

- 2026-09-28 — changed — TMFOPnnn repos should be Apache-2.0; TMFOP012 flagged as out of line — Lester, in conversation
- 2026-09-28 — added — seed from repo surveys (layout, licences, PRs) and ADR-0022
