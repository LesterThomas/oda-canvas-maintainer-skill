---
name: repo-canvas-prerequisites
description: Conventions for tmforum-oda/canvas-prerequisites, the charts and guidance for what must exist before the Canvas is installed (e.g. Keycloak).
last_updated: 2026-09-28
---

# tmforum-oda/canvas-prerequisites

This repo holds the non-Canvas prerequisites that the Canvas relies on, such as the identity provider. Per the Security Principles, identity sits outside the Canvas, and the Canvas installation stays lean. brian-burton is building it: #1 is "Add structure to repo and initial keycloak chart work", and PR #2 ("Initial version for testing") is open. The `oda-canvas` issue #523, "Create Helm Chart for Non-Canvas Prerequisites with Default Values", is related.

## Checks

- **Boundary.** Anything here must be a *prerequisite*: something an enterprise would normally already have, such as an identity provider or certificate management. It must not be Canvas functionality. If a change moves Canvas behaviour here, or prerequisites into `oda-canvas`, raise it against "layered security; defined boundaries" in `SecurityPrinciples.md`.
- **Defaults for testing, not production.** Default values should make a test or dev Canvas easy to stand up, and they should say plainly that they aren't production settings. This is the Reference Implementation's "run in production, but not ready for production" stance. Secrets should never be committed. Generated or bootstrap credentials follow "bootstrap everything".
- **Chart rules** from `repos/oda-canvas.md` apply.
- **Docs.** The `oda-canvas` installation guide should point here once this repo is usable. Suggest the cross-link as a follow-up.

## Change log

- 2026-09-28 — added — seed from repo survey (#1, #2) and `oda-canvas` `SecurityPrinciples.md`
