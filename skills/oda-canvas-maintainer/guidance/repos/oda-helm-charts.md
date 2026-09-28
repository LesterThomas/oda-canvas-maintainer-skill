---
name: repo-oda-helm-charts
description: Conventions for tmforum-oda/oda-helm-charts, the planned central Helm chart repository for the Canvas, core operators and prerequisites.
last_updated: 2026-09-28
---

# tmforum-oda/oda-helm-charts

This will be the central repository for Helm charts that deploy the ODA Canvas, its core operators and its prerequisites. As of 2026-09-28 it contains only a README, and it has no PRs or issues. It fits the move to modular, independent operators (ADR-0022), where charts are versioned and released separately from operator source.

Until its own conventions exist, review charts here with the **chart rules in `repos/oda-canvas.md`**:
- `Chart.yaml` version bump with a changelog comment;
- no hard-coded namespaces;
- `condition:` on optional dependencies;
- no `:latest` tags;
- least-privilege RBAC.

Also check:

- **One source of truth.** While charts exist in both `oda-canvas/charts/` and here, a change in one place should say how the other is kept in step, or which copy is authoritative. Drift between two copies of the same chart is the main risk of this repo.
- **Release mechanics.** The first PR that adds a release workflow (for example chart-releaser) sets the versioning rules for everything after it. Review it carefully, and ask for them to be documented in the README.

## Change log

- 2026-09-28 — added — seed; repo empty apart from README
