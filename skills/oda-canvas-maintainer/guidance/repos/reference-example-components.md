---
name: repo-reference-example-components
description: Conventions and checks for tmforum-oda/reference-example-components, the reference ODA Component Helm charts and source, published as a Helm repo.
last_updated: 2026-09-28
---

# tmforum-oda/reference-example-components

This repo holds the reference ODA Components: TMFC001, 002, 005, 006, 007, 008 and 028. Each has a Helm chart in `charts/<Name>/` and source in `source/<Name>/`. The charts are published to the Helm repo at `https://tmforum-oda.github.io/reference-example-components` by `helm/chart-releaser-action` on every push to **`master`**. The default branch is `master`, not `main`.

These components are what the ODA Canvas BDD tests and demos install. A broken chart here breaks Canvas testing, so treat correctness as high-stakes.

## Checks

- **A chart change needs a `Chart.yaml` version bump.** This is blocking. chart-releaser only publishes new versions, so an unbumped change either never reaches the Helm repo or collides with an existing release.
  - Add a changelog comment line under `version:`, in the format `# version: 1.4.2 - <what changed>`. Every existing chart uses this format.
- **Component YAML must stay valid against the current Component spec (`v1`).** Check:
  - `apiVersion: oda.tmforum.org/v1`;
  - `coreFunction`, `managementFunction` and `securityFunction` are consistent;
  - `apiType` values are protocols (see `repos/oda-canvas.md`).
  
  If the component uses a feature that is new in `oda-canvas`, check that the Canvas version that supports it has been released.
- **No hard-coded release names or namespaces** in templates. Use `{{ .Release.Name }}` and `{{ .Release.Namespace }}`. This is a known past bug: "Fixed hardcoded release name in MCP API URL" (ProductCatalog 1.4.1).
- **Source and image in step.** If `source/<Name>/` changes, the image tag in the chart's `values.yaml` should move to the new build, and the chart must be bumped.
- **README table.** When a component is added, the README's "Available Components" table gets a row, and the component's README includes its architecture diagram (#73, #74).
- **Stray files.** `.DS_Store`, `.hypothesis/` and `.vscode/` have been committed here before. Ask for them to be removed from PRs, and don't add more.
- **Agent skills live in `skills/`** (`create-oda-component`). A PR that changes a skill should keep the skill consistent with the charts it generates.

## Open issues to be aware of

- **#70: the repository has no LICENSE file.** GitHub detects no licence. This is a governance question for the maintainers and TM Forum, not something to resolve in a review (see `sensitive-situations.md` → Licensing).
- **#63:** a broken Swagger URL for TMF672 v5.0.0. External issues about API spec URLs often belong upstream with the Open API team. Check before accepting a fix here.

## Change log

- 2026-09-28 — added — seed from the repo layout, `release.yml`, `Chart.yaml` conventions, recent PRs (#62–#74) and open issues
