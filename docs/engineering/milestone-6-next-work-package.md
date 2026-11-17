# HOLOS — Milestone 6 Next Work Packages

**Project author:** Khaled AL-MAHDY  
**Purpose:** Convert the current implementation and identified gaps into a testable engineering sequence.

## Status vocabulary

- **Implemented:** source code exists.
- **CI-covered:** automated repository tests exercise the behavior.
- **Source-integrated:** actual original project asset is connected.
- **Machine-accepted:** tested on the target production machine.
- **Production-ready:** all required gates have evidence and creator review.

These statuses are not interchangeable.

## Work package 0 — protect and establish baseline

- [ ] Run read-only source inventory.
- [ ] Create verified non-overwriting backup.
- [ ] Record Git branch/head and clean/dirty state.
- [ ] Record exact Godot, Python, FFmpeg, FFprobe and OS versions.
- [ ] Preserve all current CI and character benchmark artifacts.
- [ ] Record source and LFS hashes for every recovered asset.

**Exit:** complete inventory and verified backup.

## Work package 1 — reconcile configuration contract

Current finding: v1 validator does not require a shot `scene`, but rendering requires it. The starter example has no scene path and is explicitly placeholder-only. No per-line dialogue, voice or phoneme contract is present in the inspected v1 validator.

- [ ] Add a formal JSON Schema for v1 that matches the actual supported contract.
- [ ] Add a validation test proving missing shot scene fails before Godot starts.
- [ ] Add safe `res://` scene path validation.
- [ ] Document which example fields are currently informational/unused.
- [ ] Keep backward compatibility explicit; do not silently mutate v1 semantics.
- [ ] Design a versioned v2 proposal for dialogue, voice, alignment and character performance.

**Exit:** schema, validator and tests agree.

## Work package 2 — controller observability and fault recovery

Current finding: Python waits for the Godot subprocess to finish and captures stdout/stderr. The batch manifest tracks shot-level status, attempts, errors, recovered output paths and per-frame hashes. It does not provide live frame progress and does not resume halfway through a shot.

- [ ] Design and test a versioned JSON-lines event protocol.
- [ ] Stream and validate progress events from Godot.
- [ ] Persist progress checkpoints without treating incomplete shots as complete.
- [ ] Test crash, timeout, malformed event, disk-full and forced reboot cases.
- [ ] Preserve partial output in recovery archive.
- [ ] Add explicit run IDs and event sequence numbers.

**Exit:** recoverable batch with auditable progress and no false completion.

## Work package 3 — media validation hardening

Current finding: validator checks video stream presence, dimensions, frame rate, container duration and optional audio presence/A-V stream timing. It does not yet explicitly assert codec, pixel format, decoded frame count, audio format/loudness or full decode.

- [ ] Assert codec and pixel format.
- [ ] Verify decoded frame count.
- [ ] Verify audio codec, sample rate, channels and duration when present.
- [ ] Add full-file decode pass.
- [ ] Add black/frozen-frame diagnostics with explicit thresholds and false-positive handling.
- [ ] Add loudness/true-peak report when an approved audio master exists.
- [ ] Preserve the current silent-review path.

**Exit:** media validation report covers the configured delivery profile and full decode.

## Work package 4 — original character source integration

- [ ] Recover complete original Khaled and Kevin Godot source sets.
- [ ] Verify source bytes and create backups.
- [ ] Open original projects and resolve dependencies without editing originals.
- [ ] Build one wrapper adapter per character.
- [ ] Implement deterministic frame state mapping.
- [ ] Render neutral and known-good benchmark states.
- [ ] Add expression, gaze, body and viseme mapping only after inspecting actual rig controls.
- [ ] Run independent character regressions.
- [ ] Run two-character dialogue interaction after both independent adapters pass.

**Exit:** both original rigs pass integration contract. No generic test fixture or substitute character counts.

## Work package 5 — audio and voice pipeline

- [ ] Inventory all source audio and hashes.
- [ ] Resolve the five voice identities from authoritative source records.
- [ ] Resolve narrator identity/role separately; do not infer it from theme singer.
- [ ] Create approved speaker/voice registry.
- [ ] Link dialogue segments to source audio and timing/alignment records.
- [ ] Validate timing and preserve original recordings.
- [ ] Add phoneme/viseme data only after alignment is sourced and reviewed.
- [ ] Test separate dialogue/music stems and final mix controls.

**Exit:** all voice mappings are sourced, approved and reproducible.

## Work package 6 — disconnected-network acceptance

Follow `offline-acceptance-and-dependency-policy.md`. The test must include original character rigs, multi-shot batch, interruption recovery, audio/video assembly, validation, backup and restore. CI alone does not pass this gate.

**Exit:** signed target-machine test report with no external runtime dependency.

## Work package 7 — Episode 1 production

- [ ] Recover and verify original screenplay DOCX.
- [ ] Reconcile screenplay against text extraction and storyboard.
- [ ] Recover original character references and model packages.
- [ ] Confirm all 65 storyboard IDs/order and source status.
- [ ] Build shot timing from screenplay/audio evidence, not placeholders.
- [ ] Approve scene assets and character performance.
- [ ] Produce a real review animatic/episode in staged increments.
- [ ] Keep unresolved story questions visible.

**Exit:** source-faithful, reviewable Episode 1 production with provenance and QC.

## Current honest project state

The repository contains a meaningful local production engine implementation, including Python orchestration, a generic Godot runner, ordered resumable shot rendering, frame hashes, debug-overlay gating, FFmpeg assembly and FFprobe metadata validation. The current original Khaled/Kevin rig integration and target-machine offline acceptance remain unverified.

The silent intro v001 has been reported complete by the creator's production environment. Its independent package/rerender/offline verification remains outstanding.

The next engineering priority is configuration-contract reconciliation and controller observability, while the original rig source-access gate is pursued in parallel.
