---
name: approval-criteria
description: What the two approval criteria, ODA alignment and good-enough quality, mean in practice, with calibration examples from real decisions.
last_updated: 2026-09-28
---

# Approval criteria

A PR is approved when it meets **both** criteria. Nothing else is required: not who wrote it, not whether an AI wrote it, not perfection. Most PRs are expected to be AI-generated. Judge the change, not its origin.

## Criterion 1: alignment with the objectives of the ODA

### What the ODA Canvas is for

This is the background for judging alignment.

- The Canvas exists to serve **ODA Components**. The *standard* is the ODA Component Specification. The Canvas reads a Component's declared requirements and runs whatever lifecycle process meets them.
- This repo is the **Reference Implementation**, used to certify *Components*. There is no certification of other Canvas implementations (ADR-0013).
- Behaviour is defined implementation-agnostically, first in the use-case library and then in BDD features.
- Capabilities arrive as **modular, independent Software Operators** following the Kubernetes Operator Pattern (ADR-0022). Each operator is re-usable, extendable and replaceable.
- **Delivering an AI-Native Canvas is itself an ODA objective.** This covers MCP and A2A interfaces, agents as components, the AI gateway, Model-as-a-Service and evaluation.

### Signals that a change aligns

Look for most of these. Name the ones you rely on in the brief.

- **Serves the Component contract.** It implements, or corrects, behaviour a use case or the Component spec describes, or it advances an agreed design epic or ADR.
- **Declarative.** Components gain the capability by declaring it, and an operator acts on the declaration. There is no per-component or per-vendor special-casing. *Why:* this is what keeps the Canvas technology-independent.
- **Portable.** Custom Resources don't embed installation-specific details such as Canvas-internal URLs or hard-coded namespaces. Use fixed, well-known Canvas endpoints (for example `info.canvas.svc.cluster.local`). *Why:* the same Component and CRs must run on any Canvas. Lester raised this on #602.
- **Consistent across the model.** A change to `coreFunction` considers `managementFunction` and `securityFunction`. A change to one operator or API type considers its siblings. *Why:* partial changes create a component model that behaves differently per segment (#581, #573).
- **Operator-shaped.** New capability is an operator, or an extension of the right one, that can be deployed independently.
- **Backward-compatible.** It respects N-2 support of the Component spec (currently `v1`, `v1beta4`, `v1beta3`), with webhook conversion rather than breaking changes. It doesn't break reasonable downstream assumptions; for example, sub-resource names match the Component definition (#573).
- **BDD-traceable.** Behaviour changes link to a use case and a BDD feature, or bring them.
- **Keeps the base Canvas lean.** Heavyweight capabilities are optional charts that aren't installed by default (#518).
- **Consistent with the ADRs.** Fetch the ADR index (see `SKILL.md`) and check any ADR that covers the area.

### AI-Native work

AI-Native work is **aligned by default**. Examples are new `apiType` values for semantic-layer protocols (`mcp`, `a2a`), agent components, the AI gateway, MaaS operators and evaluation tooling. Review it on quality. Adding an enum value or CRD capability for AI-Native support is **not** a standards change needing ratification, but it still needs N-2 compatibility and webhook handling. *Why:* Lester confirmed an AI-Native Canvas is an ODA goal, and ADRs 0015–0020 set the direction.

### Red flags

Raise these; don't auto-reject.

- **Changes the Component Spec's meaning, or Canvas architecture, without an ADR.** Recommend *Comment*, and draft the suggestion to propose an ADR in `oda-ca-docs/Decision-Log` (or the future Architecture repo) before or alongside the PR. *Why:* architecture decisions are recorded and agreed, not settled by merging code.
- **Contradicts an ADR.** If the ADR is *Approved*, this is blocking. If the ADR is *Proposed* or *In progress*, raise a `question:` that links the ADR.
- **Vendor or product lock-in** in a core path where the design has a pluggable operator slot.
- **Components depending on Canvas internals**, or the reverse.
- **Production-hardening scope creep** (HA, autoscaling) in the Reference Implementation. It isn't wrong, but it's outside the objective. Suggest making it optional.
- **Standalone demos or tooling** that don't serve Canvas behaviour. They may belong in another repo.

## Criterion 2: good-enough quality

"Good enough" means **the PR improves the codebase overall and has no blocking problems**. Anything else becomes a follow-up issue.

**Blocking** (must be fixed before approval):
- incorrect behaviour or an obvious bug;
- failing required CI;
- a missing required version bump or prerelease-suffix clean-up (see `repos/<repo>.md`);
- security regressions: secrets, over-broad RBAC in a *new* default, `latest` tags;
- no test or BDD evidence for a behaviour change;
- files that shouldn't be there (AI planning files, stray artefacts);
- hand-edited generated files.

**Non-blocking** (approve, and suggest a follow-up issue where worth tracking):
- missing docs for a new capability;
- RBAC tightening of an existing, working feature;
- refactoring opportunities, such as duplication across segments;
- lint issues in code the PR didn't touch;
- style-guide nits;
- portability improvements that aren't regressions.

Typical weaknesses of AI-generated code are ordinary quality problems. Look for them without mentioning where the code came from:
- invented APIs or flags;
- tests that assert nothing;
- formatting churn that hides the real change;
- planning or scratch files committed;
- workflow files edited instead of regenerated.

## The approve-plus-follow-up pattern

When a PR is valuable, aligned and free of blocking problems, **recommend Approve and draft follow-up issues for the remaining points**. Don't hold the PR for them. *Why:* this is how Lester reviews (#603: approved while raising #609–611; #598; #602). It keeps contributors moving, which matters because response time is the strongest community-health signal. It also still gets the work tracked.

Deadlines are a legitimate factor. "It would be good to merge before the DTW demo" is a reason to approve now and follow up later, provided nothing blocking remains.

## Calibration: real decisions

| PR | Outcome | Lesson |
| --- | --- | --- |
| #602 Carbon Management operator | Approved, with portability follow-ups | A new operator fits the model; CR URL portability was non-blocking |
| #603 Canvas portal | Approved, with 3 follow-up issues | Docs, tests and over-broad RBAC went to follow-ups for a valuable feature |
| #573 Segment support | Merged after dropping the name-prefix change | Consistency aligned; breaking downstream naming assumptions did not |
| #581 Multiple API versions | Comment | CRD modelling question at standard level |
| #513 Resource Inventory chart | Approved, asking to remove MongoDB | Right layer: it translates the K8s API and stores nothing |
| #608 CTK AvailabilityPolicy fix | Approved, with an explanation of why it was correct | Small correctness fix from a first-time contributor: thank, explain, approve |

## Change log

- 2026-09-28 — changed — removed `sse` from the AI-Native examples, because `apiType` names protocols, not transports (see `repos/oda-canvas.md`) — Lester's #612 decision, approved in conversation
- 2026-09-28 — added — seed from `research/oda-objectives.md` and `research/review-norms.md`; AI-Native aligned by default and the ADR route confirmed by Lester
