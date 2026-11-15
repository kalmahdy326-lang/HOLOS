# HOLOS Episode 1 — Production Readiness Matrix

**Episode status: PARTIALLY IMPLEMENTED WITH UNRESOLVED PRODUCTION DEPENDENCIES**

This matrix separates repository/tooling evidence from production-asset acceptance and completed-episode acceptance. A timeline, generic adapter, placeholder bookend, CI pass, or synthetic test is not evidence that a production episode scene or final episode exists. Statuses below reflect evidence available in the inspected branch and the declared inputs; absence of evidence is not proof that an asset does not exist elsewhere.

## Status definitions

- **NOT STARTED** — No authoritative artifact or implementation evidence for the gate is present in the inspected evidence set.
- **UNKNOWN** — The available evidence cannot establish whether the criterion is satisfied; the underlying artifact, provenance, or verification is unavailable or ambiguous. Do not infer a pass or failure.
- **PARTIAL** — Some relevant artifact or implementation evidence exists, but required acceptance evidence or scope is incomplete.
- **BLOCKED** — Progress or acceptance is prevented by an identified unresolved prerequisite. This describes the dependency state, not necessarily the absence of all groundwork.
- **READY** — The required artifact(s) exist and pass the stated gate validation, but have not necessarily been integrated into the episode production scene.
- **INTEGRATED** — The accepted artifact is loaded and exercised in the relevant production scene or final pipeline; generic/unit tests alone do not qualify.
- **REVIEWED** — A named reviewer has approved the output against defined criteria, with a review record. A test pass or un-attributed visual inspection is not approval.
- **LOCKED** — The artifact has recorded approval/version/hash and changes are controlled through a documented change request.

A status may include more than one label where useful (for example, `PARTIAL; BLOCKED`). “Acceptance role” names a role only where a declared input actually names one; otherwise it is `TBD` and is not an assignment.

## Readiness matrix

| Area / gate | Current defensible status | Evidence required to pass | Blocking dependency / gap | Acceptance role |
|---|---|---|---|---|
| Story / canonical screenplay and ending | **UNKNOWN; BLOCKED** | Canonical complete screenplay, version/hash, all scenes and ending, explicit approval record, plus approved shot/storyboard authority or permission to derive it | Complete canonical screenplay and ending are not confirmed by the handoff; four-turn excerpt is not a complete episode | TBD |
| Dialogue script | **PARTIAL; BLOCKED** | Approved complete dialogue tied to approved screenplay; stable turn IDs, speaker/text hashes, and approval/change record | Four-turn transcript exists in handoff, but full script and story authority are unconfirmed | TBD |
| Audio master / review audio | **BLOCKED** | Exact authoritative audio bytes; format, duration, technical checks, SHA-256 and named selection/provenance record; no unresolved alternate | Audio bytes are not present; review-WAV hash conflict remains unresolved (manifest lists Manus `4b8c…6730`; intake also records Codex `e9d8…94f`); no selection | TBD |
| Transcript verification | **PARTIAL; BLOCKED** | Transcript compared to approved canonical script and authoritative audio; documented four-turn boundaries and review | Handoff manifest calls transcript approved after pronunciation review and contains four turns, but full screenplay is unconfirmed and audio bytes are unavailable; source transcript is not full-episode approval | TBD |
| Acoustic alignment / timeline | **PARTIAL; BLOCKED** | Validated timeline tied by hash to selected authoritative audio, timing/duration checks, provenance and review of estimates | Two handoff timelines each contain 189 events, `schema_version: 1`, and common source-MP3 SHA-256 `e4b13c06a6c3fbca9449cffb9135d7259b62e059a3c2d1fa37085afae65b865f`; relative handoff is offset by 0.091 seconds. Internal phoneme boundaries are dictionary subdivisions/estimates, and review WAV hashes conflict; audio bytes absent | TBD |
| Visemes / speaker mapping | **PARTIAL; BLOCKED** | Authoritative viseme timeline bound to selected audio hash; verified phoneme-to-viseme rules, Khaled/Kevin-specific bindings, timing test against real actors | Timeline events contain speaker/viseme fields, but no validated production WAV, actual rig mappings, or production-scene binding evidence | TBD |
| Khaled rig | **UNKNOWN; BLOCKED** | Original production rig package and dependencies, version/hash, skeleton/control and viseme inventory, deformation/range-of-motion checks, representative render, named approval | Original production rig/project assets are not available in this branch; repository README describes prototypes but explicitly says original rig scene/dependencies are absent | TBD |
| Kevin rig | **UNKNOWN; BLOCKED** | Same independent package, control/viseme map, validation and approval evidence as Khaled | Original production rig/project assets are not available in this branch; no evidence supporting production integration | TBD |
| Facial animation / performance | **NOT STARTED; BLOCKED** | Rig-bound lip-sync, blink/gaze/head/brow/emotion performance, rendered review, defect disposition and shot-level approval | Requires actual accepted rigs, authoritative audio/timeline, direction and episode shots; none is evidenced as integrated | TBD |
| Environments / props / set dressing | **NOT STARTED; BLOCKED** | Accepted source assets with IDs, hashes, provenance/license, technical validation, scene placement and continuity review | Full episode world/project assets are not available in this branch; no approved episode environment/prop package shown | TBD |
| Direction / layout / camera | **NOT STARTED; BLOCKED** | Canonical story/boards, shot briefs, layout and camera files, framing/continuity plan, direction notes and documented approvals | Canonical complete screenplay/approved shot plan, production environments and cameras are not established. Do not treat the user-pasted 53-shot list as canonical | TBD |
| Scenes / episode body | **NOT STARTED; BLOCKED** | Complete production scenes, dependencies and manifests; correct accepted assets/audio/timeline loaded; no missing assets/placeholders/debug UI; clean integrated run | Full episode body and original production project/assets are unavailable in this branch; no scene-level production integration evidence | TBD |
| Shared audio clock | **PARTIAL; BLOCKED** | One transport drives both actors; play/pause/resume/stop/seek and boundary/end tests; measured A/V tolerance; manifest links selected audio and timeline hashes | Contract and scaffold exist, but contract labels implementation scaffold not production-validated; no source audio bytes, original rigs, or successful production audio/rig integration | TBD |
| Godot compatibility / CI | **PARTIAL** | Reproducible project import, scripts, timeline and scene/asset integration tests using target production version and actual project/assets | PR #7 CI run `43707107185` passed with Godot 4.4.1. Separate local Godot 4.7.2 import/timeline/offscreen tests passed; those do not establish compatibility of absent original production project, rigs, or production audio integration | TBD |
| Render | **NOT STARTED; BLOCKED** | Full episode render with declared resolution/FPS/container/audio, complete-frame/media audit, sync and visual/audio checks, logs and output hash | No complete episode body or integrated production scenes/assets; intro/credits are placeholders and draft music, not final | TBD |
| Shot review | **NOT STARTED; BLOCKED** | Shot-level preview/final review records, criteria, named reviewer decisions, notes and lock/change control | No canonical shot plan/rendered production shots or approval records | TBD |
| Final assembly | **NOT STARTED; BLOCKED** | Verified ordered body + approved intro/credits/audio assembly, duration/transition checks, media metadata, final master hash | No episode body or approved final bookends/music; current intro/credits are placeholders and draft music, not final | TBD |
| Subtitles / captions | **NOT STARTED; BLOCKED** | Approved subtitle/caption file(s), full-master timing, legibility/accessibility review and inclusion verification | Requires canonical full dialogue and final assembled episode; neither is established | TBD |
| Credits | **PARTIAL; BLOCKED** | Approved complete contributor/asset credits, spelling/roles, rights attribution, final credits render and review | A reusable title/credits bookend scene exists, but current credits are placeholders; approved credits manifest and final episode body are absent | TBD |
| Licensing / provenance | **UNKNOWN; BLOCKED** | Per-asset source, stable ID/version/hash, rights/license records, required permissions and audit tied to delivered master | Production asset inventory/source package and final credits/music/assets not established; cannot infer rights from repository presence | TBD |
| Archive / reproducibility | **NOT STARTED; BLOCKED** | Protected source backup and verified archive manifest of final assets, reports, tool versions, approvals, hashes and delivery master | No final approved assets/master or completed acceptance package to archive | TBD |
| Episode acceptance | **NOT STARTED; BLOCKED** | Complete final acceptance report and archive; all upstream gates passed; named approvals and final master verification | Multiple unresolved hard dependencies above; no named episode approver or acceptance record in inspected evidence | TBD |

## Asset readiness

Statuses below describe evidence in the inspected branch, not whether materials may exist elsewhere. “Unavailable” means not present in the inspected branch/evidence set, not proven nonexistent globally. No project-specific environment, prop, or shot names are inferred from unverified pasted material.

| Asset / gate | Current status | Required evidence to pass | Blocking dependency / gap | Acceptance role |
|---|---|---|---|---|
| Canonical screenplay and ending | **UNKNOWN; BLOCKED** | Complete approved screenplay, version/hash, and explicit approval for the exact version, including its ending | Canonical complete screenplay and ending are not established by inspected evidence | TBD |
| Approved dialogue script | **PARTIAL; BLOCKED** | Complete approved dialogue linked to approved screenplay, stable turn IDs and text hashes, approval/change record | Four-turn transcript/timeline handoff is not full-episode script or screenplay approval | TBD |
| Authoritative WAV selection | **BLOCKED** | Supplied exact WAV bytes, format/duration/peak validation, SHA-256, and named selection record | WAV bytes absent; competing Manus and Codex review-WAV hashes unresolved | TBD |
| Transcript and alignment groundwork | **PARTIAL; BLOCKED** | Transcript verification against approved script and selected audio; word/phoneme timelines linked to exact audio hash and validated | Timeline groundwork exists (189 events per timeline; source-MP3 hash metadata agrees); audio bytes absent, WAV selection unresolved, and internal phoneme subdivisions are estimates | TBD |
| Authoritative viseme timeline | **PARTIAL; BLOCKED** | Validated viseme timeline tied to selected audio hash, with verified speaker/rig mapping and review | Handoff fields exist, but no accepted audio selection or actual-rig production binding evidence | TBD |
| Production character rigs and body assets | **UNKNOWN; BLOCKED** | Original production rig packages, dependencies, versions/hashes, control/deformation validation, representative render, and approval | Original production rigs/scenes/body assets are unavailable in the inspected branch; prototype descriptions do not establish production assets | TBD |
| Production environments, props, and episode scenes | **NOT STARTED; BLOCKED** | Identified source assets with provenance, hashes, validation, scene integration, and continuity review | Full production project/environment assets and integrated episode scenes are unavailable in the inspected branch | TBD |
| Final render asset | **NOT STARTED; BLOCKED** | Render file, hash, media/frame/audio validation, and named review/acceptance records | No final renders or integrated production body are evidenced | TBD |

## Integration readiness

| Integration area | Current status | Required evidence to pass | Blocking dependency / gap | Acceptance role |
|---|---|---|---|---|
| Shared audio-clock scaffold | **PARTIAL; BLOCKED** | One transport drives both actors through play/pause/resume/stop/seek and boundary/end tests; measured A/V tolerance and manifest linkage | Contract and scaffold exist, but are explicitly not production-validated; no selected WAV bytes, actual rigs, or production-scene integration | TBD |
| WAV and timeline production loading | **BLOCKED** | Selected WAV and matching verified timeline load in the actual production project with recorded runtime test | Authoritative WAV selection unresolved; production project/assets unavailable | TBD |
| Two-character rig binding | **NOT STARTED; BLOCKED** | Each actor uses verified rig-specific mapping from the same transport position; integration test on production rigs | Production rigs and production scene are unavailable in inspected branch | TBD |
| Episode scene / body integration | **NOT STARTED; BLOCKED** | Production scenes load required accepted assets and run cleanly with manifests and runtime logs | Production scenes and episode body unavailable in inspected branch | TBD |
| Godot CI checks | **PARTIAL** | Reproducible tests against target production project/version and real production assets | PR #7 CI run `43707107185` passed with Godot 4.4.1 for configured checks only; it does not establish integration of absent production assets/scenes | TBD |
| Local Godot session checks | **PARTIAL** | Durable, reproducible report tied to commit, inputs, command, logs, and target production project | Local Godot 4.7.2 checks were session-level only; not durable acceptance or production integration evidence | TBD |

## Review readiness

| Review area | Current status | Required evidence to pass | Blocking dependency / gap | Acceptance role |
|---|---|---|---|---|
| Screenplay and ending review | **UNKNOWN; BLOCKED** | Named approval of the exact complete screenplay version, including ending | Canonical screenplay/ending and approval record not established | TBD |
| Dialogue/audio/alignment review | **PARTIAL; BLOCKED** | Review record tied to approved script, selected WAV hash, validated transcript/timelines, and named reviewer | Four-turn groundwork exists, but no selected audio bytes or complete screenplay authority | TBD |
| Rig, performance, and scene review | **NOT STARTED; BLOCKED** | Actual-rig rendered review against defined criteria with named reviewer and defect disposition | Production rigs, scenes, and body are unavailable in inspected branch | TBD |
| Final render / shot review | **NOT STARTED; BLOCKED** | Identified render bytes/hash, technical checks, visual/audio review, and named decision | No final renders or review records evidenced | TBD |
| Episode acceptance review | **NOT STARTED; BLOCKED** | Complete final acceptance report covering passed upstream gates and named approvals | No episode acceptance evidence; acceptance owner remains unassigned | TBD |

## Delivery readiness

| Delivery area | Current status | Required evidence to pass | Blocking dependency / gap | Acceptance role |
|---|---|---|---|---|
| Final episode master | **NOT STARTED; BLOCKED** | Final master file/hash, technical and frame/audio verification, and approval | No final render, assembly, or completed episode body evidenced | TBD |
| Captions, credits, and delivery package | **NOT STARTED; BLOCKED** | Approved complete materials, validation, rights/provenance records, and final-master linkage | Full episode master and approved delivery inputs not established | TBD |
| Archive and reproducible delivery | **NOT STARTED; BLOCKED** | Verified archive manifest of exact deliverables, reports, tool/config versions, approvals, hashes, and archive integrity | No accepted final deliverables or complete acceptance package evidenced | TBD |
| Episode delivery acceptance | **NOT STARTED; BLOCKED** | Named acceptance decision for the exact delivered master and complete evidence package | No final renders, reviews, or episode acceptance; no acceptance owner assigned | TBD |

## Repository evidence and scope boundary

The following exact repository paths are relevant evidence, but do not by themselves establish production readiness:

- [`README.md`](../../README.md) — describes the project and prototype milestones; specifically says original Khaled/Kevin rig scenes and dependencies are not in the repository and production-engine validation against actual rigs remains required.
- [`docs/episode1-production-asset-intake.md`](../../docs/episode1-production-asset-intake.md) — records the source-asset intake boundary and hard blockers: no canonical complete screenplay, no selected authoritative review WAV or supplied audio bytes, no original production rigs, and no full production project/environment assets.
- [`docs/episode1-shared-audio-clock-integration.md`](../../docs/episode1-shared-audio-clock-integration.md) — integration scaffold/contract, explicitly not production-validated; requires project-specific node paths and actual audio/timeline/rig validation.
- [`handoffs/milestone-5-1-2026-11-15/HOLOS_Milestone51_WhisperX_Acoustic_Phoneme_Timeline_Aligned.json`](../../handoffs/milestone-5-1-2026-11-15/HOLOS_Milestone51_WhisperX_Acoustic_Phoneme_Timeline_Aligned.json) — absolute timeline; schema version 1, 189 events, source-MP3 hash metadata, four-turn transcript and estimated internal phoneme subdivisions.
- [`handoffs/milestone-5-1-2026-11-15/HOLOS_Milestone51_FourTurn_Review_Phoneme_Timeline_Relative.json`](../../handoffs/milestone-5-1-2026-11-15/HOLOS_Milestone51_FourTurn_Review_Phoneme_Timeline_Relative.json) — review-relative timeline; schema version 1, 189 events, common source-MP3 hash metadata and relative offset of 0.091 seconds.
- [`handoffs/milestone-5-1-2026-11-15/HOLOS_Episode1_four_turn_review_manifest.json`](../../handoffs/milestone-5-1-2026-11-15/HOLOS_Episode1_four_turn_review_manifest.json) — manifest records a 48 kHz, stereo review WAV specification/hash, 0.091-second offset and `godot_integration: not performed`; the actual audio bytes are not in this branch, and the competing review-WAV hashes remain unresolved.
- [`.github/workflows/python-tests.yml`](../../.github/workflows/python-tests.yml) — defines Python/media, handoff validation, inventory/resource audit, Godot 4.4.1 import/timeline self-test and offscreen-render CI gates. The reported PR #7 run `43707107185` passed, which validates those CI checks only—not absent production audio, rigs, episode scenes, or final output.

A local Godot 4.7.2 import/timeline/offscreen test pass and one-off synthetic-stream probe are not equivalent to production integration or durable acceptance evidence. Production audio/rig integration was not performed; no production-integration pass or failure result exists. The handoff timelines contain real alignment groundwork; their metadata and event counts do not substitute for the source audio bytes, authoritative WAV selection, or visual validation on production rigs.

## Completion gate

Do not mark Episode 1 `COMPLETE`, `REVIEWED`, or `LOCKED` until the canonical approved screenplay/ending, approved full dialogue, selected exact audio bytes, validated transcript/alignment/visemes, accepted production rigs and mapped facial controls, integrated episode scenes/environments/cameras, reviewed complete renders, final assembly/subtitles/credits, licensing/provenance, archive, and named acceptance evidence are all present. No owner, reviewer, approval, asset, or canonical 53-shot list is inferred by this matrix.
