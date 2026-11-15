# HOLOS Episode 1 — Final Render Verification

**Status:** Acceptance protocol; no full-body render has been verified.
**Applies to:** Each locked shot render and the assembled delivery master.
**Decision rule:** A render or delivery is not `VERIFIED`, `APPROVED`, or `COMPLETE` until every required automated check and every required human review below has passed and is recorded. A successful encode, passing CI, or passing metadata validator alone is not acceptance.

## 1. Evidence boundary and current status

The repository contains generic render/assembly infrastructure and automated media checks, but its documented production limitations remain: the actual Khaled and Kevin production rigs are not integrated, production safeguards and offline acceptance remain unverified, and the complete episode body and final render are absent. Existing title/credits bookend previews are **non-final placeholders**. They do not establish approved final title/credits, a completed episode, or body-render acceptance. **No full body render exists in the evidence reviewed for this protocol.** Do not describe the episode as fully rendered or final until a full-body master has been produced and passed this protocol.

This protocol defines required evidence; it does not assert that a check has already been run. The repository's validator currently checks configured width/height, FPS, container duration, required audio presence, stream start-time offset, and stream-duration difference. The frame assembler checks numbered frame presence. Those checks do not by themselves establish visual quality, frame uniqueness, perceptual A/V sync, subtitle correctness, rights clearance, or complete human review.

## 2. Authority and locked delivery profile

Before preflight, the producer and delivery owner must approve and lock one versioned delivery profile for the specific deliverable. Record the profile file/path, version, approval date, approver, and SHA-256 in the verification report. A profile must define, as applicable:

- Deliverable identity and scope (shot, sequence, bookends, body, or complete master), intended destination/platform, container, codecs, and required stream layout.
- Frame dimensions, display aspect ratio, pixel aspect ratio, frame rate (including rational/timebase and CFR/VFR policy), color primaries, transfer characteristics, matrix, range, bit depth, and pixel format.
- Expected frame range/count and editorial duration derived from the approved frame-accurate edit/shot manifest.
- Required audio tracks, channel layout, sample rate, bit depth/codec, language/role, and approved audio alignment and duration tolerances.
- Any delivery-specific loudness/true-peak target, measurement method, and tolerance. If no target is approved, loudness and peak compliance must be reported as **not specified / not judged against a target**; do not invent or inherit a target from a tool default.
- Subtitle/caption language, format, inclusion/sidecar or burn-in policy, and applicable timing/legibility requirements.
- Credits and rights/provenance requirements, plus named approvers and signoff roles.

Any absent or ambiguous required profile value blocks final acceptance. Do not assume 1920×1080, 30 FPS, a color space, codec, loudness target, or a tolerance unless the approved profile explicitly selects it. Any change to a locked profile requires documented change approval, a new profile version/hash, and revalidation of affected output.

### Preflight — automated and accountable

Before rendering, the render lead records the profile and source-manifest hashes and verifies the intended project/scene, shot order, frame ranges, assets, audio sources, subtitles, credits, render mode, and output destination. Confirm inputs are authoritative and approved, paths resolve, no required assets are missing, source files are protected, and the output path cannot overwrite a prior accepted master. Record exact toolchain versions and settings. A failed or incomplete preflight blocks rendering for delivery; debug samples must be clearly labelled and segregated from production output.

## 3. Render environment and reproducibility record

For each render attempt, including rejected attempts, record:

- Godot exact version/build (and relevant project version/commit), project configuration, renderer/backend, graphics device/driver where relevant, operating system, and render mode.
- FFmpeg and FFprobe exact versions/build configuration used for assembly and inspection; Python/controller version where used.
- Locked profile ID/version/hash; scene and shot manifest version/hash; source asset/audio/subtitle/credit manifest hashes; render and assembly commands/configuration; start/end time; operator; output path; and attempt identifier.
- Per-shot frame ranges, reported success/failure, warnings/errors, retries/resumptions, and output hashes. Preserve logs, machine-readable probe/validation reports, frame manifest, and any review notes.

Do not infer the renderer from a project setting alone: record the actual renderer/backend used for the accepted run. If a required environment detail cannot be established, document it and obtain delivery-owner disposition before acceptance.

## 4. Automated technical verification

Run checks against the exact assembled candidate and its source-frame/manifests. Store command output and machine-readable results with the candidate's hash. Automated checks are necessary but are not substitutes for human review.

### 4.1 Frames, order, and continuity

- Reconcile expected frame count from the locked frame ranges/edit manifest with rendered frames and encoded video metadata. Record expected and observed counts and any inclusive/exclusive frame-range convention.
- Verify sequence order and continuity: every expected frame index appears once, indices are consecutive across the defined range, no gaps or unexpected extras exist, and shot concatenation/order matches the approved edit manifest.
- Verify each referenced frame exists, decodes, and has the profile dimensions. Compare frame-manifest identities/hashes to the exact inputs assembled. Detect byte-identical duplicate frames automatically where possible and report repeated-frame candidates; identical images can be intentional holds, so disposition requires human review rather than automatic rejection solely on equality.
- Decode/scan the complete encoded video for corrupt packets/frames and report decode errors. Automated black/frozen/near-duplicate heuristics may flag candidates, but cannot decide whether a cut, fade, intentional hold, or black frame is editorially intended.

A missing, corrupt, out-of-order, or unexplained duplicate frame is a failure. Every intentional exception must be identified in the approved edit/profile and confirmed during review.

### 4.2 Metadata, frame rate, color, and duration

Inspect the assembled file with FFprobe or an equivalent recorded tool. Compare observed width/height, display and pixel aspect ratios, frame rate/timebase, CFR/VFR behavior, color metadata, pixel format/bit depth, codecs, and container against the locked profile. Record both declared metadata and measured/decoded facts where available; absent or contradictory metadata is a failure when the profile requires it. Metadata tags do not prove perceptual color correctness.

Derive expected video duration from the approved frame count and rational frame rate (or the locked edit's authoritative timebase and boundaries), not from an assumed standard. Define and record the permitted tolerance in the approved profile before rendering. Compare observed video duration and final assembled duration to that expectation; also reconcile shot/sequence boundaries and any approved handles, fades, or padding. If the profile has no justified duration tolerance, obtain approval before delivery rather than choosing one after seeing the result.

### 4.3 Video and audio streams

Verify that the candidate contains exactly the required video/audio/subtitle/data streams and no unintended streams. Confirm codec, dimensions, frame rate, track order, channel count/layout, sample rate, language/role tags, and required metadata against profile. Ensure required audio is present, decodable, mapped to the correct track, and not silently replaced by another source. Confirm audio duration and stream start times are measurable; compare audio/video start offset and stream-duration difference to the approved tolerances. Missing required streams, unapproved extras, undecodable media, or unmeasurable required timing fails automated validation.

### 4.4 A/V synchronization evidence

Provide both:

1. **Automated stream-timing evidence:** measured video/audio start times and durations, signed deltas, profile tolerances, tool/version, and pass/fail result. The current pipeline supports configurable sync tolerance and reports stream-level start and duration differences; its documented default is not an approval and must not override the locked profile.
2. **Human perceptual evidence:** independent review of synchronization at representative dialogue/transient events across the full program, including beginning, middle, end, scene/shot transitions, and any known risk points. For lip-synced material, inspect visible articulation against the authoritative audio and note the reviewed timecodes/events. Record reviewer, playback conditions, observations, measured/estimated offset if used, and pass/fail.

Stream timestamp agreement alone does not prove lip sync or perceptual synchronization. Any perceived drift, incorrect speaker/track pairing, or unexplained mismatch blocks acceptance pending investigation and retest.

### 4.5 Loudness and peaks

Measure integrated loudness, loudness range, sample peak and/or true peak only when the locked profile specifies a target, tolerance, and measurement standard/method. Record the tool/version, measurement window, track(s), results, and target comparison. If no approved target exists, report measurements only as descriptive diagnostics or mark them not measured; do not claim compliance and do not impose a target. Clipping, distortion, dropouts, unintended silence, or destructive mix errors remain subject to human listening review regardless of target status.

## 5. Human review — mandatory independent gate

A named reviewer who did not operate or assemble the candidate must review the exact hash-identified candidate. The reviewer must have authority and suitable playback/display conditions for the deliverable. Record reviewer name/role, date, file hash, profile version, playback setup, review range, findings, defect references/timecodes, decision, and signature/approval record. Reviewer independence and any conflicts must be disclosed.

### 5.1 Complete start-to-finish playback

Play the entire candidate continuously from its first frame through its final frame and audio tail, without skipping, at the intended delivery playback behavior. Verify opening, every transition and shot, body, ending, audio continuity, and credits/post-credit material as applicable. Record start/end confirmation and playback method. Scrubbing, spot checks, a contact sheet, automated scan, or reviewing only previews cannot substitute for full playback.

### 5.2 Visual and audio inspection

During full playback and targeted second-pass inspection as needed, review:

- Unintended black/frozen frames, flashes, missing/duplicated frames, gaps, cadence judder, corrupt images, abrupt transitions, and continuity errors. Confirm automated flags as intentional or defects.
- Image framing, focus/readability, exposure, color consistency, compression artifacts, clipping, geometry/material defects, character/prop continuity, performance, facial animation, and visible lip sync against approved references/profile.
- No debug overlays, diagnostics, editor controls, test labels, temporary filenames, watermarks, placeholder text/assets, missing textures, error messages, or other non-delivery UI. Confirm production mode and inspect transitions/edge frames where overlays can appear intermittently.
- Audio intelligibility and continuity, correct track/speaker assignment, dropouts, clicks, distortion, unintended silence, and audible A/V sync. Judge loudness/peak compliance only against a profile-approved target.

Any placeholder, debug artifact, unapproved black frame, unexplained freeze/duplicate, missing content, technical defect, or unresolved reviewer note blocks approval.

### 5.3 Subtitles, captions, credits, and rights

For required subtitles/captions, verify correct approved text, language, speaker attribution, spelling, cue order, timing, synchronization, safe placement, legibility, contrast, and absence of truncation/overlap. Confirm the locked policy for sidecar versus burn-in is met; inspect both the master and sidecar files and verify their hashes when applicable.

Check title cards and credits against approved copy and contributor spellings/roles; verify required music, asset, and rights acknowledgements appear as specified. The producer or delegated rights owner must independently confirm that every included asset, font, music/audio recording, performance, logo, and third-party contribution has documented provenance and permission/license for the intended distribution. Record the rights manifest and approval. A render review cannot itself establish rights clearance. Missing/unclear rights or unapproved credits blocks release.

## 6. Acceptance record and signoff

The verification report for each candidate must include the candidate filename, byte size, SHA-256, profile/version/hash, source and edit manifests, toolchain/renderer record, expected versus observed frame count and duration, stream and color metadata, automated reports/logs, sync evidence, subtitle and rights records, full-playback confirmation, defect/exception log, and named approvals.

Required approvals include the render/technical owner for automated results, an independent visual/audio reviewer, and the designated delivery/producer or rights approver for profile, credits, and clearance. Each role records an explicit pass/fail or approved exception with rationale. No unresolved critical or delivery-blocking defect may be waived informally.

**Completion prohibition:** Do not claim a shot, master, or episode is final, verified, accepted, or complete until automated checks pass **and** independent human review/signoff passes for the exact same output hash. If either side is missing, failed, or refers to a different candidate hash, status remains `NOT VERIFIED` (or the applicable in-progress/rejected state).

## 7. Re-render, retest, and change control

Any change to frames, edit/order, source assets, audio, subtitles, credits, profile, render settings, renderer/toolchain, or assembly invalidates affected verification. Create a new attempt/candidate and hash; never silently replace an accepted file. Re-run all relevant automated checks and human review against the new candidate. For a changed final master, repeat complete start-to-finish playback. For a localized shot correction, rerender and validate the shot plus inspect affected boundaries/transitions and the reassembled master; repeat full playback of the master before final delivery. Re-run rights and subtitle checks whenever their sources or presentation change.

On any failed check or review, record the finding and affected timecode/frame/stream, reject or quarantine the candidate, correct the cause, preserve prior evidence, and retest. A resumed/partial render is not accepted until the final assembled candidate has the complete expected frame sequence and passes the same gates. Do not reuse a previous signoff for a changed hash.

## 8. Archive and integrity

Archive read-only copies of the locked profile, source and edit manifests, scene/project identity, tool/version report, render/assembly configuration and commands, logs, source-frame manifest, final candidate, automated probe/validation reports, review and signoff records, subtitles/sidecars, credits/rights evidence, and defect/change history. Generate SHA-256 hashes for the final master and every archived acceptance artifact; include relative path, size, hash, and role in a machine-readable archive manifest. Verify hashes after copying to the archive and record verification results, archive location/date, and custodian. Preserve rejected attempts and their reason separately where retention policy permits; do not label them final. Archive hash verification establishes file integrity, not creative approval.

## 9. Related pipeline documentation

- [Milestone 6 — Local Production Engine](../../docs/milestone-6-local-production-engine.md): implemented pipeline capabilities, known boundaries, media validation, A/V tolerance configuration, and acceptance evidence.
- [Episode 1 — Shared Audio Clock Integration Contract](../../docs/episode1-shared-audio-clock-integration.md): authoritative audio/timeline linkage and required synchronization tests.
- [HOLOS Episode 1 — Production Asset Intake](../../docs/episode1-production-asset-intake.md): missing source dependencies, delivery profile inputs, current blockers, and acceptance boundary.
