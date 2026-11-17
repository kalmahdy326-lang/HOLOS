# HOLOS — Repository Evidence Criteria

**Purpose.** This document defines how repository claims are substantiated and how evidence is recorded. Repository evidence establishes only the artifact, check, or review actually observed; it must not be promoted into a broader production or episode-completion claim. Current classification remains **partially implemented with unresolved production dependencies**.

## Evidence classes

| Class | Meaning and acceptable proof |
|---|---|
| `SOURCE_ARTIFACT` | A specific tracked source/input artifact, identified by repository path, immutable content hash, version, and source/authority. A manifest that names a missing file is metadata, not the file itself. |
| `AUTOMATED_TEST` | A reproducible test or validator, including exact command, environment, scope, result, and captured output/log. A passing test proves only its assertions against the inputs it actually read. |
| `RUNTIME_INTEGRATION` | Evidence the intended application loaded and exercised the real integrated assets and runtime path, with engine/build version, scene/configuration, logs, and observed result. Static parsing or a generic adapter test is not production integration. |
| `VISUAL_AUDIO_REVIEW` | A named human’s review of identified image, video, or audio bytes against stated criteria, with asset hash/version, review date, reviewer, findings, and disposition. Automated metadata checks are not creative review. |
| `APPROVAL` | Explicit decision by the authorized role on a specific immutable version/hash and defined scope. A transcript status or author statement is not approval of a full screenplay or episode. |
| `PROVENANCE_LICENSE` | Origin, creator/source, chain of custody, rights/license and permitted use for the exact asset version, supported by the license/permission record. A filename or attribution alone does not prove rights. |
| `FINAL_ARCHIVE` | Verified delivery package and manifest covering required outputs, hashes, approvals, tool/config versions, validation reports, and archive integrity/location. A render command or an unverified file is not final archive evidence. |

## Required evidence record fields

Every evidence-register row must contain, at minimum:

- **ID and class**; concise claim or requirement supported.
- **Repository/path** (or clearly marked external immutable location) and exact artifact name.
- **Commit SHA** for repository content; for non-Git inputs, source/receipt identifier and custody record. Never use a branch name as the identity.
- **File SHA-256** of the exact bytes examined. For directories/packages, record a deterministic manifest hash plus per-file hashes where practical.
- **Version**: artifact/schema/release version and relevant tool, engine, or dependency version.
- **Status**: `PASS`, `FAIL`, `PARTIAL`, `NOT RUN`, `SUPERSEDED`, or `NOT PRESENT`; do not translate absence to pass.
- **Date/time** (UTC preferred) and **responsible role** (producer/operator who generated or supplied evidence).
- **Reviewer** (named person and role, or `none`); distinguish operator from independent reviewer.
- **Validation command and result**: exact command, exit/result, and durable log/report path/hash. For human review, give review criteria and decision instead of a command.
- **Scope and limitations**: what was exercised, excluded, assumptions, and what the result does not establish.
- **Links**: related claim/requirement IDs and predecessor/successor evidence IDs when applicable.

If a field cannot be established, enter `unknown` or `not recorded`; do not infer it. Evidence status must not be upgraded solely because a later document repeats the assertion.

## Evidence integrity, freshness, and supersession

1. Preserve original inputs as immutable raw evidence. Do not overwrite, normalize in place, transcode, or “fix” the only received copy. Create derived copies in separate paths and record the exact transformation command, tool/version, input hash(es), output hash, and operator. Preserve failed outputs/logs when relevant.
2. Evidence is fresh only for the exact bytes, commit, configuration, toolchain, and scope recorded. A source change, new commit, dependency/tool upgrade, changed settings, regenerated output, or altered input invalidates the affected evidence unless an explicit impact review demonstrates otherwise. Re-run impacted gates; do not silently carry forward a prior pass.
3. Supersede rather than erase: retain the old record and mark `SUPERSEDED`, point to its replacement, explain why, and identify the effective current version. Conflicting evidence remains visible until resolved by a documented owner/reviewer decision.
4. Hash evidence files with SHA-256 from their actual bytes. Record the hashing method/tool and date for external or archived evidence. Commit IDs identify repository state; they do not substitute for each artifact’s content hash.
5. A pointer, URL, path string, or metadata claim is not proof that the referenced bytes are present or identical. Verify availability and hash the bytes actually consumed.

## Git LFS and large-file validation

For every Git LFS asset relied on by a test or production claim, distinguish the committed LFS pointer from the resolved payload. Record the pointer file’s repository path, commit, and SHA-256 separately from the LFS object’s declared OID/size and the downloaded/materialized payload’s independently computed SHA-256 and byte size. Validate that checkout has materialized the payload (not merely the short `version https://git-lfs.github.com/spec/v1` pointer text), that its content matches the declared LFS SHA-256 OID and size, and that the test/runtime actually consumed those bytes. Capture `git lfs ls-files`/checkout or equivalent command and result where applicable. If only a pointer is available, mark payload validation `NOT PRESENT` and do not claim the media was tested, reviewed, or archived.

## CI evidence capture

A CI pass record must identify the provider/workflow file and workflow name, **run ID and URL**, event/PR and head commit SHA, job and step names, conclusion, start/completion date, and retained log/artifact references with hashes where available. Record runner/OS, Python version and relevant dependency versions, and engine version. Pin/version and verify downloaded tool binaries where the workflow does so.

For Godot checks, capture the exact Godot version/build and command for each relevant job. The repository workflow pins/downloads Godot **4.4.1**, checks the download archive checksum, runs headless project import/script parsing, a headless timeline self-test, and an offscreen render integration test under Xvfb/software rendering. CI evidence supplied for **PR #7, run `43707107185`, commit `211f404a`**, records a passed result using **Godot 4.4.1**. Retain/link the provider’s run record and logs; the short commit prefix must be resolvable to a full SHA in the run record.

A green workflow proves only that those workflow steps passed against that checkout and CI environment. It does not prove that absent WAV bytes, full production assets, actual character rigs, approved screenplay, visually acceptable performances, final episode renders, or delivery archive exist or pass. The repository’s local Godot **4.7.2** checks were session-level checks, not committed formal evidence artifacts; do not represent them as a durable CI result or as committed formal acceptance.

## Claims-to-proof rules

- Every material readiness, quality, or completion statement must link to one or more evidence IDs that directly test its acceptance criterion. State the claim at the narrowest level supported.
- Separate **artifact exists**, **automated check passed**, **runtime integration passed**, **human review approved**, and **production acceptance**. None implies the next.
- Link derived evidence to its exact inputs and transformations. For timeline claims, link both timeline artifacts, the manifest, validator/version, and the source identity/hash recorded in them. A source hash in JSON proves that metadata agrees across those files; without source bytes it does not independently verify the source file’s content.
- Label estimates, assumptions, missing dependencies, and unverified authority explicitly. Do not describe estimated internal phoneme subdivisions as measured phoneme alignment or timeline tests as lip-sync review.
- A CI status badge, PR merge, code presence, test name, or planned command is not proof without the run record/result and scope.
- No claim may exceed the least complete evidence on which it depends. Episode-level `COMPLETE` requires the full set of screenplay/audio/rig/scene/render/review/approval/archive gates, not merely passing repository checks.
- Do not cite or describe any draft 53-shot list as evidence.

## Current evidence examples and boundaries

| Example / supported claim | Evidence class and result | What this proves | What this does not prove |
|---|---|---|---|
| Absolute and review-relative Milestone 5.1 timeline JSON files and manifest are committed under `handoffs/milestone-5-1-2026-11-15/`. Both timelines contain 189 events and share source-MP3 SHA-256 metadata `e4b13c06a6c3fbca9449cffb9135d7259b62e059a3c2d1fa37085afae65b865f`; the recorded source offset is `0.091` seconds. | `SOURCE_ARTIFACT`; `AUTOMATED_TEST` via `python tools/validate_milestone_5_1_handoff.py` (also invoked in CI). | The validator checks schema, exact four-turn transcript/speaker order, event counts and bounds/order/visemes, matching source-MP3 hash metadata, manifest offset, and corresponding absolute-vs-relative event offsets. | The original MP3 or review WAV bytes were not supplied in the repository evidence inspected; metadata agreement does not prove those source bytes or WAV bytes match. It does not establish full screenplay approval, measured phoneme boundaries (internal subdivisions are dictionary-based estimates), runtime Godot integration, actual-rig behavior, or visual/audio lip-sync quality. |
| PR #7 CI run `43707107185` on commit `211f404a` passed using Godot 4.4.1. | `AUTOMATED_TEST` / CI. Capture the provider run and logs as described above. | That the workflow’s configured checks passed on that commit in the CI environment, including its stated Python/media, handoff, inventory/resource-audit and Godot checks as reflected by the actual run logs. | It does not prove production WAV bytes, full screenplay approval, actual production rigs, visual review, completed scenes/episode, final render, or acceptance/archive. A Godot offscreen test is not a human creative review. |
| Local Godot 4.7.2 checks were performed at session level. | `AUTOMATED_TEST`, session-level only; no committed formal report identified. | At most, the checks performed in that session against their then-current inputs. | Without durable command/log, commit, hashes, and results, this is not reproducible repository acceptance evidence and cannot replace the CI run or a production integration record. |
| Production WAV bytes; full screenplay approval; actual rigs; visual/audio review of production renders; and final render evidence are absent from the evidence inspected. | `SOURCE_ARTIFACT`, `APPROVAL`, `RUNTIME_INTEGRATION`, `VISUAL_AUDIO_REVIEW`, and `FINAL_ARCHIVE` are `NOT PRESENT` for these items. | Only that these acceptance artifacts are currently absent from the inspected repository/evidence set. | Absence does not prove the assets do not exist elsewhere; it means no positive repository-backed acceptance claim can be made until they are supplied, hashed, validated, and reviewed. |

The timeline validator itself states its limitations: review-WAV bytes are absent, conflicting WAV hashes remain unresolved, internal phoneme subdivisions are estimates, and the check does not validate the full episode, Godot runtime, rigs, or rendered lip-sync. Keep those limitations attached to any citation of its `PASS` result.

## Compact evidence register template

Copy one row per independently verifiable item; use `unknown`/`not recorded` instead of invented values.

| ID | Class | Claim / requirement | Repo path or immutable location | Commit SHA | File SHA-256 / package manifest | Version / toolchain | Status | Date | Responsible role | Reviewer | Validation command/result or review decision | Scope / limitations | Supersedes / related IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E-___ |  |  |  |  |  |  |  |  |  |  |  |  |  |

**Example row (recorded metadata, not source-media byte verification):** `E-TL-01 | SOURCE_ARTIFACT + AUTOMATED_TEST | Four-turn paired timelines preserve events and recorded offset | handoffs/milestone-5-1-2026-11-15/{timeline files, manifest}; tools/validate_milestone_5_1_handoff.py | full SHA: resolve from checked-out commit/run | timeline/manifest file hashes: compute from checked-out bytes | schema 1; Python stdlib | PASS (scope-limited) | 2026-11-15 handoff; run date per log | unknown/not recorded | none recorded | python tools/validate_milestone_5_1_handoff.py; capture exact exit/log | 189 events each, metadata hash agrees, offset 0.091 s; does not verify absent source MP3/review WAV bytes, actual phoneme acoustics, runtime, rigs or visual result | handoff/CI run evidence`.
