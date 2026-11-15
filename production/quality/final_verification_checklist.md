# HOLOS Episode 1 — Final Verification Checklist

**Status:** NOT VERIFIED — no full episode is verified; every box below remains unchecked.
**Use:** Complete this gate for the exact assembled delivery candidate. This checklist defines required evidence; it records no completed checks.

## Completion rule

Mark `COMPLETE` only when every applicable check below passes, all required approvals are recorded, and every report, review, and approval refers to the same exact candidate SHA-256 and the same locked profile/version/hash. Any failed, missing, unresolved, or mismatched-hash check blocks `COMPLETE`. A changed input, profile, scene, render, or assembly creates a new candidate hash and invalidates affected evidence; revalidate and review the new candidate. Record `NOT APPLICABLE` with rationale and approver where a check truly does not apply; do not silently omit it.

Delivery dimensions, frame rate/timebase, codecs, color, audio track layout/sample rate, tolerances, and other delivery settings must be taken from an approved, versioned delivery profile. Do not assume or hard-code dimensions, FPS, or audio settings. Missing or ambiguous required profile values block acceptance; this checklist does not claim current compliance.

## 1. Canonical source, script, and approval

- [ ] Canonical complete screenplay/source and ending are identified by path, version, and SHA-256.
- [ ] Authorized approver has approved the exact screenplay/source version for this production purpose; approval record is available.
- [ ] Approved dialogue/script is linked to the canonical source; version, file SHA-256, stable turn/speaker identities, and per-turn text hashes are verified.
- [ ] Required editorial/storyboard/shot-plan authority is approved and hash-identified; any permitted derivation is documented.
- [ ] No unresolved script, pronunciation, performance, or editorial change remains; change control is recorded.

Evidence refs / notes: ______________________________

## 2. Audio selection and identity

- [ ] One authoritative audio source/take is explicitly selected by a named authorized owner for this purpose.
- [ ] Exact audio bytes are present, readable, and SHA-256 hashed; format, sample rate, channels, bit depth/codec, duration, and peak/clipping checks are recorded against the approved profile or applicable audio requirements.
- [ ] Provenance/export chain and selection record identify the exact audio hash; competing variants are resolved, not silently substituted.
- [ ] Audio used in the production scene and final assembly matches the selected hash; required track mapping and language/role are verified.

Evidence refs / notes: ______________________________

## 3. Transcript, alignment, and visemes

- [ ] Transcript is checked against the approved script and selected audio; turn order, speaker attribution, boundaries, and discrepancies are reviewed and dispositioned.
- [ ] Transcript/alignment provenance and authority are explicit; machine-generated verification output is not silently promoted to authoritative content.
- [ ] Word and phoneme/acoustic timeline artifacts are present, ordered, bounded, duration-checked, and linked to the exact selected audio SHA-256 and timebase/offset.
- [ ] Estimated or manually derived timing is identified as such, reviewed, and not represented as measured acoustic evidence.
- [ ] Authoritative viseme timeline is linked to the same exact audio hash; phoneme-to-viseme mapping, character/speaker assignment, timing, and event ranges pass validation and named review.
- [ ] Timeline files loaded by the production scene match the validated, approved hashes; no unapproved replacement or alternate timeline is active.

Evidence refs / notes: ______________________________

## 4. Character rigs and performance

- [ ] Each required production character rig, model, dependencies, and facial rig is the approved production version with source path, version, SHA-256, provenance, validation, and named approval.
- [ ] Skeleton, body/facial controls, required visemes, range of motion, deformation, and representative render tests pass for each actual production rig.
- [ ] Character-specific viseme bindings are verified against the actual rigs; no speaker drives the wrong character.
- [ ] Required dialogue, listening/reaction, gaze, blink, head, brow, gesture, and emotional performance is integrated and reviewed in rendered output.
- [ ] Lip articulation is reviewed against the authoritative audio at representative events and across the complete program; defects (including jitter, seams, pops, or continuity issues) are resolved or explicitly dispositioned by an authorized approver.
- [ ] Performance approval identifies the exact rig/animation/render hashes and named reviewer.

Evidence refs / notes: ______________________________

## 5. Scene integration

- [ ] Approved production scenes, environments, props, cameras, lighting, and dependencies are present and hash/manifests identify the exact inputs.
- [ ] Production scenes load the approved assets, selected audio, and validated timeline; shared transport/timebase drives all required synchronized events.
- [ ] Required integration tests exercise actual production assets and scenes, including play/pause/resume/stop/seek, actor mapping, timing boundaries, and end behavior as applicable; logs and versions are retained.
- [ ] Headless/runtime production check completes without errors or missing resources; test scenes and debug-only behavior are excluded from delivery output.
- [ ] Scene order, shot/frame ranges, transitions, and content coverage match the approved editorial manifest; no placeholder asset remains.

Evidence refs / notes: ______________________________

## 6. Locked profile, render, and automated technical checks

- [ ] Approved delivery profile is locked and identified by ID/path, version, SHA-256, approver, and approval date; every required output setting and tolerance is specified.
- [ ] Candidate identity, source/edit manifests, exact input hashes, render/assembly commands, renderer/backend, software/tool versions, environment, operator, attempt ID, and logs are recorded.
- [ ] Every expected frame exists exactly once and in order; expected and observed counts/ranges reconcile to the approved manifest. Missing, corrupt, out-of-order, or unexplained duplicate frames fail.
- [ ] Full encoded video decodes without errors; dimensions, aspect ratios, frame rate/timebase/CFR-VFR, color metadata, pixel format/bit depth, codecs, and container are compared to the approved profile.
- [ ] Measured duration and frame count reconcile with the approved edit/timebase; approved tolerance is applied, not invented after rendering.
- [ ] Required streams, track order/layout, codec, audio sample rate, language/role tags, start times, and durations match the approved profile; no unintended stream is present.
- [ ] Automated A/V stream start-offset and duration-difference results are recorded with tool/version and compared to profile-approved tolerances.
- [ ] Loudness/true-peak compliance is claimed only if the locked profile specifies target, method, and tolerance; otherwise report not specified/not judged against a target.
- [ ] Automated reports, probe outputs, frame manifest, and candidate SHA-256 are retained and mutually identify the same exact candidate and inputs.

Evidence refs / notes: ______________________________

## 7. Independent full-playback review

- [ ] Named independent reviewer, not the render operator/assembler, is authorized and reviews the exact candidate SHA-256 and locked profile version under suitable playback conditions.
- [ ] Reviewer watches and listens to the entire candidate continuously from first frame through final frame and audio tail, without skipping; start/end and method are recorded. Spot checks, samples, previews, and automated scans do not substitute.
- [ ] Visual review covers all scenes, shots, transitions, opening/body/ending, credits and post-credit material as applicable; unintended black/frozen/flash/duplicate frames, cadence issues, continuity errors, framing, focus, color, exposure, compression, materials, geometry, and performance are checked.
- [ ] Review confirms no debug overlays, diagnostics, editor controls, temporary/test text, placeholders, missing assets/textures, unintended watermarks, or non-delivery UI.
- [ ] Listening review confirms intelligibility, continuity, correct speaker/track, no unintended gaps/clicks/distortion/silence, and perceptual A/V/lip synchronization at beginning, middle, end, transitions, and risk points.
- [ ] All defects and exceptions are recorded with timecodes/frame references, severity, owner, disposition, and retest evidence; no blocking or unresolved critical item remains.
- [ ] Independent reviewer records explicit pass/fail, findings, date, hash, profile version, setup, scope, and approval/signature.

Evidence refs / notes: ______________________________

## 8. Subtitles, credits, and licensing

- [ ] Subtitle/caption deliverables match the approved language, text, speaker attribution, format, and sidecar/burn-in policy; exact files are hashed.
- [ ] Timing, order, synchronization, safe placement, contrast, legibility, spelling, truncation, and overlap are reviewed on the final candidate; sidecars are independently verified where applicable.
- [ ] Title cards and credits match approved copy, contributors, names, and roles; final presentation is reviewed and tied to the candidate hash.
- [ ] Rights/provenance inventory covers every included asset, font, music/audio recording, performance, logo, and third-party contribution; permissions/licenses cover intended distribution and exact versions.
- [ ] Named producer/rights owner approves the credits and rights manifest; unresolved rights or attribution questions block release.

Evidence refs / notes: ______________________________

## 9. Final assembly and archive integrity

- [ ] Final assembly contains the approved ordered components and intended complete scope; all required body content and approved bookends/credits are present.
- [ ] Final duration, frame/shot boundaries, transitions, audio continuity, subtitle policy, and stream layout pass against the locked profile and approved edit manifest.
- [ ] Final master has a recorded filename, byte size, SHA-256, profile hash, and matching automated and human acceptance evidence.
- [ ] Archive includes the locked profile, source/edit/asset manifests, project/scene identity, toolchain/configuration, commands, logs, renders/master, reports, subtitles, credits/rights evidence, defect/change history, and all approval records.
- [ ] Machine-readable archive manifest records path, size, SHA-256, and role for each required artifact; copied archive hashes are rechecked and verified, with location/date/custodian recorded.
- [ ] Archive evidence and delivery copy identify the same exact accepted master hash; rejected attempts are segregated and not labelled final.

Evidence refs / notes: ______________________________

## 10. Named final acceptance

- [ ] Technical/render owner records pass for automated checks and exact candidate hash.
- [ ] Independent visual/audio reviewer records pass for full-playback review and exact candidate hash.
- [ ] Delivery/producer/editorial approver records pass for profile, assembly, subtitles/credits, and intended scope/hash.
- [ ] Rights approver records pass for provenance, licensing, and credit obligations, or a documented authorized disposition where appropriate.
- [ ] Named final acceptance authority: ____________________  Role: ____________________
- [ ] Final acceptance decision, date, scope, candidate SHA-256, locked profile version/hash, evidence-register/report location, and signature/approval record are complete.
- [ ] All applicable checks above pass on the same exact hashes; no blocking defects, open exceptions, or unresolved dependencies remain.

**Final status:** ☐ NOT VERIFIED  ☐ REJECTED  ☐ COMPLETE
(Select exactly one only after completing the evidence record. `COMPLETE` is prohibited unless the completion rule above is satisfied.)

## Evidence boundary

This is a blank acceptance checklist, not evidence that its checks have run. No full episode is verified, and all boxes remain unchecked at issuance. The repository evidence and intake record describe missing or unresolved production inputs and do not establish a full-body render, final master, independent full-playback review, or named final acceptance. See [Final Render Verification](final_render_verification.md) for the detailed protocol and [Production Readiness Matrix](production_readiness_matrix.md) for current evidence status.
