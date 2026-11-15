# HOLOS Episode 1 — Asset Acceptance Checklist and Index

**Canonical requirements:** [Asset Acceptance Specification](asset_acceptance_specification.md). This page is a concise review index, not a separate or overriding standard. If a checklist item needs interpretation, apply the specification and its cited intake/integration contracts.

## Before proposing acceptance

- [ ] Identify the asset with a stable ID, type, exact revision/hash/byte size, and explicit intended purpose and scope.
- [ ] Record authoritative source, provenance, derivation/parent links, rights basis and restrictions.
- [ ] Inventory dependencies and verify availability, versions and required configuration.
- [ ] Validate the actual working bytes; distinguish Git LFS pointer metadata from fetched file contents.
- [ ] Produce reproducible, type-appropriate validation and point-of-use integration evidence where applicable.
- [ ] Obtain separate, applicable technical, creative and rights decisions for the exact same version/hash and purpose; roles are unassigned labels until assigned.
- [ ] Record lifecycle state, decision history, evidence references, conditions, storage/backup and limitations.
- [ ] Confirm there is no blocking defect, unresolved condition, rights issue, stale downstream reference or unreviewed post-approval change.

## Type-specific gate index

Consult the corresponding section in the [specification](asset_acceptance_specification.md#7-type-specific-gates) for detailed requirements:

- [ ] Screenplay and dialogue script — §7.1
- [ ] Audio masters, dialogue, music and stems — §7.2
- [ ] ASR, transcript, acoustic alignment and viseme timeline — §7.3
- [ ] Character rigs and animation-ready packages — §7.4
- [ ] Facial controls and visemes — §7.5
- [ ] Environments and props — §7.6
- [ ] Fonts, logos and title graphics — §7.7
- [ ] Godot project, scenes, scripts and plugins — §7.8
- [ ] Derived renders, previews and final outputs — §7.9
- [ ] Music and other third-party media — §7.10

## Lifecycle and lock

- [ ] Use only specified lifecycle states and record each transition (§4).
- [ ] Reject or quarantine failed/unverifiable submissions; document any permitted exception (§5).
- [ ] Lock only after the full lock gate; route all changes through revision, revalidation, reapproval and downstream impact review (§11).

## Configurable delivery and evidence boundary

Delivery settings must be specified for the actual intended output and verified from actual bytes. 48 kHz/stereo is only an intake target for the review WAV, not evidence of its measured format or a universal delivery rule. This checklist and the specification define requirements; neither demonstrates that assets exist, tests passed, approvals were granted, or production is complete. See specification §§7.2 and 12, plus the [Production Asset Intake](../../docs/episode1-production-asset-intake.md) and [Shared Audio Clock Integration Contract](../../docs/episode1-shared-audio-clock-integration.md).
