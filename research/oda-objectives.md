# What "aligns with the objectives of the ODA" means (task 1.5)

Alignment is one of only two approval criteria (spec §5.6). This file distils it from the `oda-canvas` `origin/main` documents (read 2026-09-28):

- `README.md`
- `Canvas-design.md`
- `AI-Native-Canvas-design.md`
- `SecurityPrinciples.md`
- `usecase-library/README.md`
- `AGENTS.md`

It also uses the architectural points Lester raises in real reviews (`review-norms.md` §1). It seeds `guidance/approval-criteria.md`.

## The objectives, as the project states them

1. **The Canvas exists to serve ODA Components.**
   - The *standard* is the **ODA Component Specification**. There is no separate Canvas standard.
   - The Canvas reads Component metadata and executes whatever lifecycle process meets it.
   - The Canvas "should be able to support any Component that meets the Component standard".
2. **It is a Reference Implementation used for certification.**
   - The Reference Implementation of the ODA Canvas "will be used for ODA Component certification".
   - Behaviour is defined implementation-agnostically, at Level 2, in the **use-case library** and the **BDD features**.
   - The Reference Implementation (Level 3) implements and tests that behaviour.
   - Other Canvas implementations, such as public cloud offerings, are expected to show the same behaviours.
3. **It is modular and extensible through Software Operators.**
   - Capabilities are delivered by independent operators following the Kubernetes Operator Pattern.
   - Operators should be re-usable, extendable or replaceable, for example the matching API Management operator for whichever gateway or mesh is in use.
4. **It is technology-independent at the Component interface.** Components declare *requirements* in a technology-independent way, and the Canvas maps them onto concrete services such as the gateway, identity provider and observability.
5. **Standards first; the Reference Implementation informs the standard.**
   - "Conformance with the ODA standards is paramount."
   - When the Reference Implementation needs something the standard lacks, the change is *proposed to the Component standard*. It does not diverge quietly.
6. **Security principles:**
   - automated security controls tested on every PR;
   - a failed test is a bug;
   - "run in production, but not ready for production" (hardened and safe to deploy, but not built for scale or resilience);
   - layered security with defined boundaries (identity lives outside the Canvas);
   - bootstrap everything from a single identity.
7. **AI-Native direction** (Epic 4):
   - Components can expose **MCP** interfaces, declaratively, as another `apiType`;
   - AI agents are packaged as composable ODA Components;
   - Canvas services support AI at scale: AI gateway, observability, and evaluation of non-deterministic systems;
   - the model is multi-vendor and multi-agent, with governance and responsible AI.

## Alignment tests for a PR or issue

A change **aligns** when it does most of these, and none of the red flags below applies:

- **Serves the Component contract.** It implements, or makes more correct, behaviour that the Component Specification or a use case already describes, or it extends the Canvas in the direction of an agreed design epic.
- **Declarative, not special-cased.** Components get capabilities by *declaring* them in their spec, and an operator acts on the declaration. There is no per-component or per-vendor hard-coding.
- **Portable across Canvases.** Custom Resources and components don't embed installation-specific details such as Canvas-internal service URLs or namespaces. Fixed, well-known Canvas endpoints are used instead, for example `info.canvas.svc.cluster.local` (Lester, #602).
- **Consistent across the component model.** A change to one segment (`coreFunction`) considers `managementFunction` and `securityFunction` too (#581, #573). A change to one API or operator considers its siblings.
- **Operator-shaped.** New capability arrives as an operator, or an extension to one, that is independently deployable and replaceable. It does not arrive as logic baked into an unrelated operator.
- **Backward-compatible.** It respects N-2 support of the Component spec (`v1`, `v1beta4`, `v1beta3`), with webhook conversion and deprecation warnings rather than breaking changes. It doesn't break reasonable downstream assumptions (#573).
- **BDD-traceable.** Behaviour changes trace to a use case and a BDD feature, or bring them. Level 2 artefacts stay implementation-agnostic.
- **Keeps the base Canvas lean.** Heavyweight or optional capabilities are opt-in charts, not default installs (#518).
- **Secure by default** in the sense of the Security Principles:
  - least-privilege RBAC;
  - no bootstrap secrets;
  - tests for security controls.

## Red flags: likely misalignment (raise, don't auto-reject)

- **Changes the Component Specification's meaning**, such as CRD fields or semantics, without a linked issue or discussion. This needs **ratification**, not just review. Recommend *Comment* and point to the standards route.
- **Vendor or product lock-in** in a core path, for example assuming one gateway, identity provider or cloud when the design has a pluggable operator slot.
- **Components depending on Canvas internals**, or the Canvas depending on a specific component's internals.
- **Production-hardening scope creep** (HA, scaling) that the Reference Implementation explicitly doesn't aim for. This isn't *wrong*, but it's outside the objective. Suggest keeping it optional.
- **Standalone tooling or demos inside `oda-canvas`** that don't serve Canvas behaviour. These may belong in another repo, such as the workshop, prerequisites or reference-example-components repos.

## Calibration from real decisions

| Case | Decision | Why |
| --- | --- | --- |
| #602 Carbon Management operator | Approved, with portability follow-ups | A new operator fits the modular model and the Carbon Control use case. CR URL portability was non-blocking and moved to a later fix |
| #603 Canvas portal | Approved, with 3 follow-up issues | Valuable, and aligned as tooling for Canvas operation. Docs, tests and RBAC went to follow-ups |
| #573 Segment support | Merged after dropping the `-c-/-m-/-s-` renaming | Consistency across segments aligned; renaming broke downstream assumptions |
| #581 Multiple API versions | Comment, questioning the CRD semantics | Standard-level modelling question: one `ExposedAPI` per version, or an array? |
| #513 Resource Inventory Helm | Approved, asking to remove MongoDB | Right layer: it translates the K8s API and doesn't store data |
| #448 Multi-namespace components | Judged in scope | "It should be part of the Canvas reference implementation" |

## Decisions from Lester (2026-09-28)

1. **Delivering an AI-Native Canvas is itself an ODA objective.** AI-Native work is **aligned by default**: MCP and A2A `apiType`s, agent components, AI gateway, Model-as-a-Service and evaluation. It is not flagged as a standards change just for adding capability, such as CRD enum values. The normal quality checks still apply, including backward compatibility (N-2), webhook conversion and BDD evidence.
   - Example: PR #613 re-adds the `a2a` apiType. It is aligned (see ADR-0019 below), and it is reviewed on quality. `sse` was deliberately *not* re-added: on #612, Lester ruled that `apiType` names semantic-layer protocols, not transports.
2. **Architecture decisions live in Architecture Decision Records (ADRs).** Today they are in the [`oda-ca-docs/Decision-Log`](https://github.com/tmforum-oda/oda-ca-docs/tree/master/Decision-Log). A dedicated Architecture repository will replace it later. This is both:
   - **an alignment source.** A PR that implements an accepted or in-progress ADR is aligned. A PR that contradicts an ADR is a red flag;
   - **the ratification route.** A change that alters architecture or the standard and isn't covered by an ADR should be proposed as a new ADR (a PR to the Decision-Log) before or alongside implementation. It shouldn't just be merged.

### ADR index snapshot (2026-09-28)

There are 22 ADRs. The ones most relevant to reviews:

| ADR | Topic | Status |
| --- | --- | --- |
| 0003 | Reference API gateway | Approved |
| 0009 | Monorepo Helm and container versioning | Pending board |
| 0010 | AI4Canvas operator scope | Proposed |
| 0011 | Uniform Canvas-to-Component information transfer | Proposed |
| 0012 | Handling of ExposedAPIs by different operators | Proposed |
| 0013 | No certification for Canvas implementations | Pending board |
| 0014 | Multiple component namespaces | Pending board |
| 0015 | AI Gateway for LLM access | In progress |
| 0016 | MCP server for TM Forum Open APIs | In progress |
| 0017 | Strategy for AI agents | In progress |
| 0018 | AI Model operator for agentic components | In progress |
| 0019 | Adopt A2A for agent skill exposure | In progress |
| 0020 | ML model integration via MLOps | In progress |
| 0021 | Optimise the ODA Canvas repo for AI coding agents | In progress |
| 0022 | Modular and independent operators | In progress |

Many ADRs are *In progress* or *Proposed*. For review purposes, treat those as the current agreed direction, not as settled law. When a PR conflicts with a *Proposed* ADR, raise it as a `question:`, not a blocker.

**Correction to the objectives above.** ADR-0013 records "no certification for Canvas implementations". That qualifies objective 2: the Reference Implementation is used to *certify Components*, not to certify other Canvases. The skill fetches the live ADR index at review time, because it changes.
