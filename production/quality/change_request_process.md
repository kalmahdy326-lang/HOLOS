# HOLOS Episode 1 — Change Request Process

## Purpose and scope

This process controls any proposed modification, replacement, withdrawal, or reinterpretation of an accepted or controlled production artifact. It prevents silent replacement and preserves the distinction between a proposal, implementation, validation, review, and acceptance of a specific version for a specific purpose. A change request does not itself establish that an asset exists, that a change was implemented, or that a test or approval occurred.

Use the companion record template at [`change_request.template.json`](change_request.template.json), validated against [`holos-change-request-v1.schema.json`](../../config/schemas/holos-change-request-v1.schema.json). Record exact versions and SHA-256 hashes when known; do not infer unknown assets, scenes, shots, roles, or evidence.

## Categories

| Category | Scope | Approval routing (roles, not assignments) |
|---|---|---|
| `EDITORIAL` | Screenplay, dialogue, text, timing, ordering, or editorial intent | Showrunner and affected leads |
| `AUDIO` | Audio masters, transcript, acoustic alignment, or viseme timeline | Audio Lead and Animation Lead |
| `ANIMATION` | Rig, performance, facial animation, gaze, gesture, or animation clips | Animation Director and Rigging Lead as applicable |
| `ART` | Environment, prop, texture, material, or set dressing | Art Lead and Environment Lead as applicable |
| `TECHNICAL` | Scene, transport clock, loader, project, or integration | Technical Director and QA Lead as applicable |
| `RENDER` | Render settings, rendered output, or assembly | Render Lead and Editorial Lead |
| `DELIVERY` | Subtitles, credits, archive, or final master | Production Lead and Localization Lead as applicable |
| `EMERGENCY` | Minimum change needed to prevent an immediate production failure | Production Lead and affected owner; use the narrow exception controls below |

These are routing labels only; no person is appointed by this table. Add affected discipline/rights/security reviewers when the change touches their responsibility. Rights, security, data integrity, preservation, and evidence requirements are not waivable.

## Lifecycle and status meanings

`DRAFT -> SUBMITTED -> UNDER_REVIEW -> APPROVED | REJECTED | DEFERRED -> IMPLEMENTING -> VALIDATING -> REVIEWING -> CLOSED`

A request may return to `DRAFT` for correction or move from an approved decision to `DEFERRED` if prerequisites arise. `APPROVED` authorizes the scoped implementation plan; it is not acceptance of the resulting artifact. `CLOSED` is permitted only after implementation, independent validation, required reviews/approvals, downstream re-review, and closure evidence are complete. Rejection/deferment reasons and decisions must be recorded. Do not skip states silently; retain a decision/history trail in the record or linked durable evidence.

## Required record and evidence

The record captures: stable request ID, project/episode, title, category, priority and status; requester and submission time; rationale; affected assets with current/proposed versions and hashes (unknown values remain null); affected scene/shot references only where known; impact by discipline; risks and mitigations; implementation, test, and rollback plans; approval decisions and conditions; implementation evidence/deviations; independent validation result/report; downstream re-review; and closure decision/evidence.

An `affected_assets` entry identifies the artifact and its exact current accepted revision/hash, and proposed revision/hash when available. Do not overwrite the prior accepted bytes. Scene/shot references are optional and must be listed only when actually known; absence does not mean no impact. Impact categories should explicitly identify whether review, update, rerun, or no impact is indicated, with rationale. Link evidence by stable repository path or other durable reference and identify its version/hash where applicable.

## Separation of duties

The requester, implementer, independent validator, and approver are distinct control roles. The validator must not be the implementer. The approver must be authorized for the category and scope and should not approve their own implementation. Record role labels and assigned person only when actually assigned; otherwise use null/unassigned placeholders. Record decisions against the exact proposed version/hash and purpose, with decision time, conditions, and evidence reference.

If a small team cannot fully separate roles, document the specific constraint, which roles are combined, why, the additional compensating review/control, and who performs it. Never represent combined duties as independent. At minimum, the implementation must receive a documented review by someone other than the implementer before acceptance/closure; if that cannot be achieved, keep the change unaccepted and open pending independent review.

## Approval, implementation, and validation gates

1. **Submit:** provide rationale, exact known affected artifacts, impact, risk/mitigation, implementation/test/rollback plans, and requested scope. Return incomplete requests for completion; do not authorize work based on an undocumented verbal request.
2. **Review and approve:** confirm category, scope, affected owners, rights/provenance and security implications, downstream dependencies, rollback feasibility, and required reviewers. Approval must precede ordinary implementation and apply to the specific proposed scope/version. A request approval does not substitute for asset acceptance or downstream approvals.
3. **Implement:** follow the approved plan; preserve original accepted source bytes; create a separately versioned candidate and new hash for changed bytes; record commands/changes, timestamps, evidence, and deviations. Obtain new validation evidence and update references/manifests without erasing history.
4. **Validate independently:** a non-implementer runs the approved tests on the actual candidate bytes and records methods, results, failures, report references, and hashes. Rerun every check impacted by the change, including relevant unit/integration checks and representative render or visual/audio review when applicable. A generic test or repository presence is not proof of production integration or creative acceptance.
5. **Downstream re-review:** identify all downstream artifacts, uses, approvals, renders, manifests, and deliveries whose assumptions or hashes changed. Mark prior reviews/approvals stale where applicable; re-review and reapprove each affected downstream artifact against its new exact version/hash and purpose. Do not carry forward approval by implication.
6. **Close:** close only when implementation is complete, all required independent checks pass or have explicitly resolved dispositions, required approvals and downstream reviews are recorded, the candidate is accepted for a defined purpose, rollback disposition is known, and no blocking failure remains. Record closure status, reviewer, time, and evidence. Otherwise remain open or reject/defer.

## Rollback and preservation

Before implementation, identify how to restore the exact previously accepted bytes and their recorded SHA-256, source location/backup, and references. Preserve that prior version immutably; do not overwrite it with a candidate. On rollback, restore the prior accepted bytes, verify the restored hash against the pre-change record, restore compatible references/configuration, and rerun all checks impacted by the attempted change. Record the rollback, evidence, failures, and resulting status. A rollback does not erase the change history and does not automatically revalidate downstream outputs; re-review downstream consumers as needed. If exact prior bytes/hash cannot be preserved and verified, do not claim rollback success or acceptance.

## Emergency exception

An emergency exception is limited to the smallest reversible, time-critical action necessary to contain or prevent an immediate production failure. Record the specific hazard, scope, affected artifacts, temporary nature, rationale, risks, containment, rollback, who authorized it, and required validation/review evidence. Obtain authorization by the applicable production authority and affected owner before action where practicable; if immediate containment makes prior authorization impossible, document why and seek prompt producer-directed review after containment. An emergency label is not blanket approval, and the change remains unaccepted until normal evidence, validation, approvals, and downstream re-review are complete.

Emergency handling never waives rights/licensing, security, integrity, source preservation, independent evidence/validation, or accurate reporting. Do not use emergency status to ship an unreviewed change or bypass protections. Any retrospective review window or deadline must be explicitly set by the producer; this process invents no time window.

## Rejection, deferral, and closure criteria

Reject or defer a request that lacks a clear rationale, affected-asset identification, impact/risk assessment, test or rollback plan, required authorization, provenance/rights basis, or a viable preservation path; would silently replace accepted bytes; or would invalidate an approved downstream result without re-review. Record the reason and decision. A failed check must be recorded, not omitted; unresolved blockers prevent acceptance and closure.

## Evidence boundary

This process, schema, and blank template specify controls and provide a recording format only. They do not demonstrate that any production asset, scene, shot, change, reviewer, approval, test, validation report, backup, rollback, or completed episode exists. Record only observed evidence and actual decisions. Unknown facts remain unknown, roles remain unassigned until assigned, and no request is evidence of completion by itself.
