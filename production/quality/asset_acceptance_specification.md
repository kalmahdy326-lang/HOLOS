# HOLOS Episode 1 — Asset Acceptance Specification

**Status:** Governing acceptance specification. This document defines the evidence and gates required before an asset is used in a production scene, referenced by a shot, approved for a stated production purpose, or locked. It complements [Production Asset Intake](../../docs/episode1-production-asset-intake.md) and [Shared Audio Clock Integration Contract](../../docs/episode1-shared-audio-clock-integration.md).

## 1. Purpose, scope, and governing principles

Acceptance is specific to an identified asset revision, its exact working bytes, and a defined purpose and scope. It is not blanket approval for later edits, other uses, or episode completion. Repository presence, a successful generic validator, prototype behavior, placeholder functionality, or a render-command exit status does not by itself establish production acceptance.

Each accepted asset must have traceable provenance, verified bytes and dependencies, applicable technical validation, distinct required technical/creative/rights decisions, and a recorded approval of the exact version and SHA-256 for the stated purpose. Requirements below apply when the relevant asset is supplied; listing a gate does not assert that an asset exists.

Preserve authoritative originals. Keep source, editable project, derived, and rendered outputs distinguishable. Never silently overwrite or substitute an accepted or authoritative artifact. A material content or byte change is a new revision and must be reassessed.

## 2. Approval is exact-version and purpose-specific

Every approval record must bind together, at minimum:

- Stable asset ID and human-readable identity/type.
- Exact version/revision and SHA-256 of the bytes actually reviewed; include byte size.
- Approval decision, decision date, reviewer identity or assigned role label, and review notes/conditions.
- Explicit approval purpose and scope: intended production use, episode/scene/shot scope where applicable, platform or delivery scope where applicable, and any permitted limitations.
- References to the validation report, provenance/rights evidence, dependency inventory, and change-control record as relevant.

Approval of one version does not transfer to a changed file, a different hash, a derivative, a different purpose, or a downstream output. Reapproval is required when affected content, dependencies, configuration, or intended use changes. Technical validation, creative approval, and rights clearance are distinct gates: none substitutes for another. Required roles are role labels only until a person is assigned; no role label in this specification asserts that an approval occurred. Where independent review is required, the submitter cannot self-approve.

## 3. Asset manifest and required evidence

Maintain an asset manifest entry and linked records for every proposed production asset. Missing, contradictory, or unverifiable required evidence blocks acceptance. Use an appropriate structured record format, but retain the following information:

| Evidence area | Required record |
|---|---|
| Identity and intended use | Stable unique ID; name; type/subtype; episode and intended scene/shot or production role; explicit acceptance purpose and scope. Do not invent scene or shot identifiers. |
| Source and provenance | Authoritative source location or immutable repository/release reference; creator/vendor; source package/archive identity; acquisition or creation method/date; original-versus-derived designation; derivation steps and parent IDs for derivatives. Preserve originals and identify the exact source bytes. |
| Version and change history | Version/revision; creation and meaningful revision timestamps; accountable owner; change-request reference; supersedes/superseded-by links. Never overwrite accepted records. |
| Integrity | Exact working-byte size and SHA-256; separately identify hashes for source, archive, and derived files. Hash bytes actually used, not pointer text or an unverified archive listing. |
| Rights | Rights holder/author; license or other rights basis; supporting agreement/source reference or URL where applicable; attribution; permitted modification, synchronization, use, distribution and redistribution; territory, term, credit and other restrictions. Record original/public-domain status with supporting basis. Unclear rights block production use. |
| Dependencies | Complete direct and transitive dependency inventory with versions/hashes where available: linked resources, plugins/add-ons, fonts, codecs, scripts, external services, engine resources, import/runtime requirements and required configuration. Identify availability and any offline/network requirement. No undeclared or missing dependency may be required for approved use. |
| Validation | Dated reproducible report naming tools/versions, environment, target platform/settings, procedure or commands, inputs/hashes, results, exit codes, limitations, evidence locations and asset-type checks. Include integration tests at point of use where applicable. |
| Review and approval | Accountable asset owner, technical reviewer, and applicable creative and rights approvers; role/person, decision/date, exact reviewed version/hash, purpose/scope, notes, conditions, and evidence references. Record each gate separately. |
| Lifecycle and storage | Current lifecycle state, state-change history (date, actor, reason, evidence), repository/storage location, backup/archive reference as applicable, and whether source, editable, derived, or rendered output. |

### 3.1 Technical validation versus creative and rights decisions

Technical validation establishes that the specific files are intact, readable, configured, reproducible and compatible with the stated use. It does not approve story, performance, design, composition, branding, sound, or final output. Creative approval is a separate recorded decision by the appropriate authority. Rights approval/clearance is separate as well. Every applicable gate must pass; a test pass or creative sign-off cannot waive rights, integrity, or hard technical requirements.

## 4. Lifecycle states

Use these exact lowercase states in the manifest. Record every state transition with date, actor, reason and evidence reference. `integrated` records use in an exercised production context; it is not a substitute for acceptance. `locked` is a controlled state reached only under Section 11.

| State | Meaning and restrictions |
|---|---|
| `candidate` | Received or created and inventoried; evidence or review is incomplete. Not eligible for production scenes or final delivery. |
| `quarantined` | Isolated because provenance, hash, security, licensing, dependency, integrity or compatibility is uncertain or under investigation. Do not load into production. |
| `accepted` | Applicable evidence and technical checks pass; required exact-version, purpose-specific creative/rights approvals are recorded. Authorized only for recorded scope. |
| `integrated` | Accepted asset is loaded and exercised in the intended production context, with integration evidence recorded. Integration does not expand its approved purpose. |
| `locked` | Accepted (and, where applicable, integrated) revision has a recorded lock; changes require approved change control and impact review. |
| `rejected` | Fails a gate, is unfit/unauthorized, or is declined by a required approver. Retain decision and reason; do not use in production. A corrected submission is a new candidate revision. |
| `superseded` | Previously reviewed/accepted revision replaced by a separately identified revision. Preserve the old record/hash and check downstream references for staleness. |

Normal movement: `candidate` to `accepted`, `quarantined`, or `rejected`; `quarantined` to `candidate` after documented resolution or to `rejected`; `accepted` to `integrated` when point-of-use evidence is recorded; `accepted` or `integrated` to `locked` after the lock gate; and a replaced revision to `superseded` when a replacement is accepted or formally designated. A locked revision changed through an approved change request becomes a new candidate revision; preserve the prior locked record. Only `accepted`, `integrated`, or `locked` assets may be used, and only within their recorded authorization. Rejected and superseded revisions are not production-authorized.

## 5. Hold and rejection rules

Reject, or quarantine pending investigation, when any of the following applies:

- Placeholder, mock, proxy, demo, draft or unapproved variant is presented as final; authoritative source is missing; identity/version or derivation is ambiguous or untraceable.
- Required hash is missing, mismatched or unverifiable; bytes are corrupt/truncated; archive content differs from its manifest; or Git LFS pointer text is mistaken for asset bytes.
- License/consent is missing, unclear, expired, incompatible or unauthorized; attribution or other obligations are unmet.
- Required dependency is missing or undeclared, references are broken, import fails, format is unsupported, or target-version compatibility/load/render/test fails.
- Applicable technical criteria fail; an unresolved defect affects intended use; identity, timing or evidence conflicts remain unresolved.
- Required technical, creative or rights approval is absent; a conditional approval remains unresolved; or an approval refers to another version/hash/purpose.
- Content changed after review without a new revision, hash, validation and required reapproval.

A defect exception is allowed only when an authorized approver documents that it does not violate rights, integrity, safety or a hard technical gate. Record scope, risk, workaround, accountable owner, expiry/recheck condition, and exact-version approval. Exceptions cannot convert placeholders, unlicensed material or unverified bytes into accepted production assets. Otherwise reject or hold; do not disguise a failed gate as acceptance.

## 6. Git LFS pointer and working-byte verification

For LFS-intended files (including formats designated in `.gitattributes`), verify repository metadata and actual working content independently:

1. Inspect the committed object. When LFS is intended, confirm it is a valid pointer with the LFS version line, `oid sha256` and declared size. A pointer is metadata, not media/model content.
2. On a system with Git LFS installed, fetch and check out the required object. Confirm the working-tree file is not pointer text; compare actual byte size and SHA-256 with the manifest. Record the LFS OID separately from actual content SHA-256; do not assume they are interchangeable without verification.
3. Confirm all required LFS objects fetch from the configured remote and are durably available in the production archive/backup or another documented store. An apparently successful checkout with unresolved pointers fails this gate.
4. For non-LFS files, perform the same working-byte size/hash checks and confirm repository policy is appropriate for file size/type.
5. Retain command/tool version, object reference, hash/size results, and report. Do not mark an asset accepted based solely on `.gitattributes`, pointer files, or a source checkout.

An unavailable Git LFS tool or inaccessible remote means working-byte validation could not be performed; it is an environment limitation and blocks acceptance of affected assets, not proof that objects or production binaries exist.

## 7. Type-specific gates

Each applicable subsection supplements—not replaces—the universal manifest, provenance, rights, dependency, validation and approval requirements. Delivery settings must be explicitly configured for the project/use and recorded with the asset or deliverable. Do not treat example values as universal production specifications.

### 7.1 Screenplay and dialogue script

- Record the canonical screenplay source format, complete approved content, version, hash and explicit production-approved designation by the story authority. A partial draft or extracted excerpt is not a canonical complete screenplay.
- Trace dialogue scripts to the screenplay. Record stable turn/line IDs, speaker IDs, exact text and ordering, per-turn text hashes and whole-file hash; document pronunciation, performance, timing and approved editorial deviations.
- Validate encoding/schema, required fields, stable IDs, hash consistency, speakers and consistency against the approved source. Edits create a new version and require story approval; audio-affecting edits also require audio/alignment review.
- Partial or four-turn material does not prove approval of a complete episode screenplay, full edit or shot-by-shot plan.

### 7.2 Audio masters, dialogue, music and stems

- Identify each master/stem, role, channel layout, sample rate, bit depth/codec, loudness/peak policy, measured duration, start/timecode/offset, edit/export provenance, DAW/session version as applicable, and SHA-256. Preserve source masters; document processing and derive a new version.
- Explicitly select one authoritative dialogue file for the stated purpose. Validate decodability, measured format/duration, expected turn structure, channel mapping, peak/clipping, silence/gaps and alignment to approved script. Record measured facts from actual bytes.
- **Final delivery audio target:** The user-provided Episode 1 specification requests 48 kHz stereo final audio. The versioned delivery profile must confirm that value or document an approved change; the request is not a measurement or acceptance result.
- **Source WAV evidence:** The four-turn review-WAV manifest claims 48 kHz and two channels, but the WAV bytes are not supplied here and those claims are not independently verified. Measure the selected exact WAV, record actual channel mapping, and do not treat manifest metadata as proof. Other masters/stems must meet their applicable approved profile and may require documented conversion.
- Stems identify source mix/version, names, synchronized start/end, format, intended summing behavior and sample alignment. Render/sum test for offsets, polarity/phase issues, clipping, missing content and unauthorized substitution.
- Record performer/recording provenance, voice consent, composition/master rights and scope of distribution. A prototype's inclusion does not establish clearance.
- Bind downstream alignment/timeline metadata to the exact authoritative audio hash and measured duration. If competing variants exist, keep them distinct until an authorized selection is documented; this specification selects no file.

### 7.3 ASR, transcript, acoustic alignment and viseme timeline

- Distinguish non-authoritative ASR/intermediate output from approved transcript and authoritative acoustic alignment/viseme data. Record tool/model/version, procedure/configuration, language, source audio ID/hash, measured duration, timebase, offsets and parent transcript/script version/hash.
- Validate schema, monotonic and in-range timestamps, event order/overlap rules, duration boundaries, complete turn/speaker mapping, IDs and deterministic hash linkage to exact audio bytes. Check representative word/phoneme boundaries against listening or waveform evidence; record method and tolerance/results.
- Compare ASR text to approved script. Review/version corrections; never silently promote machine recognition or manual guesses to authoritative alignment.
- Viseme events must use an approved phoneme-to-semantic-viseme mapping and verified controls for the correct character/speaker. Test start/end, gaps, seeking, boundaries, pause/resume and end-of-stream in integrated playback.
- Apply the [Shared Audio Clock Integration Contract](../../docs/episode1-shared-audio-clock-integration.md): one active dialogue transport, both actors query the same position, and timeline provenance matches the audio actually played. Generic timeline tests do not establish two-character integration or visual lip-sync approval.

### 7.4 Character rigs and animation-ready packages

- Intake complete original project/scene and referenced resources: skeleton/bones, mesh/skin, materials, textures, shaders, animation library, facial controls, hair/clothing/accessories, IK/collision resources, import settings, source art/models and licenses. Identify each character and rig revision independently; never substitute one character's appearance/rig for another.
- Document hierarchy/control inventory, semantic node/property paths, units/scale/orientation, retargeting assumptions, supported animation states and limitations. Validate resource integrity, controls/ranges, deformation, weighting, intersections, IK, eye/mouth behavior and reproducible import in exact target Godot version/renderer.
- Demonstrate representative rest, speaking, blink, gaze, turn, gesture, walk and reaction poses/motions; test range/deformation at representative camera distance/lighting; retain benchmark scene and review evidence.
- Rigging/technical animation readiness approval is separate from character/design and animation-direction approval of appearance/performance. Functional prototype or placeholder is not a final production rig.

### 7.5 Facial controls and visemes

- Document every facial control/blend shape, exact name/path, neutral value, range, combination rules, symmetry/asymmetry and semantic viseme/emotion mapping.
- Validate required mouth shapes, transitions/blends, jaw/teeth/tongue, blink, brows, gaze/saccades, emotional poses and rest behavior. Inspect rendered output for jitter, clipping, seams, intersections, hair pop and unintended deformation.
- Run automated binding/range checks and visual playback using authoritative audio and timeline; test speaker isolation, pause/seek/end and approved A/V offset across the complete dialogue. Capture reviewed close and wide evidence appropriate to intended use.
- Technical mapping approval does not replace creative approval of acting, expression or lip-sync.

### 7.6 Environments and props

- Identify source scene/model and dependencies, dimensions/units/scale, coordinate/origin conventions, intended use, LOD/collision needs, materials/textures/shaders and provenance/license.
- Validate geometry, normals/topology as applicable, UVs, references, material/shader compatibility, scale, collision behavior, import settings, performance budgets and missing resources. Open in exact target engine version; test intended lighting, framing and representative characters/action.
- Record art/design approval separately from layout/continuity review of usability, camera clearance, placement and continuity. No unresolved blocking defect.

### 7.7 Fonts, logos and title graphics

- Fonts: record exact family/foundry/version, file hash, license and embedding/redistribution rights; test required glyph coverage, fallback, shaping/kerning, weight/style and readability at configured delivery resolution. Package the licensed font or document reliable availability; do not silently substitute a system font.
- Logos/title graphics: identify authoritative vector/source, version, clear-space/color/monochrome rules, safe area, minimum size, aspect ratio and trademark/brand approval. Validate export/render fidelity, transparency, color profile, legibility and animation as applicable. Record rights and brand/creative approval separately.
- Re-render representative use at configured output dimensions; inspect clipping, substitutions, raster artifacts, wording and attribution.

### 7.8 Godot project, scenes, scripts and plugins

- Record project snapshot/repository commit, project configuration, exact target Godot editor/runtime version and renderer, platform, import settings, plugin/add-on names and exact versions/commits, license notices, export templates and complete dependency/resource inventory. Preserve an untouched source backup before integration.
- Open/import in exact production target version; parse scripts, resolve resource paths, audit dependencies, and run required headless/offscreen tests. Test actual integration with supplied assets, not only scaffold scenes. Validate startup, scene loading, expected bindings, missing-resource/errors and target rendering.
- Review every plugin for provenance/license, compatibility, security and necessity. No undeclared network download/service may be a hidden prerequisite for an offline production use case.
- Run unit, integration and representative scene/render tests in target version; retain logs, exit codes, commit, asset hashes and environment. CI's pinned Godot 4.4.1 check is evidence only for the checked project revision and does not accept unavailable production assets or prove compatibility with another target version.
- Technical director role approves integration; project/technical owner role approves engine/version configuration. Lock requires successful tests against actual target project and assets.

### 7.9 Derived renders, previews and final outputs

- The user-provided Episode 1 specification requests **1920×1080 at 30 FPS** and **48 kHz stereo final audio**. Treat these as requested project targets; lock them in a versioned profile only after delivery-owner approval, or document an approved change. The bookend preview setting of 1280×720 at 24 FPS is a separate preview configuration and is not final-delivery evidence. No target value proves that source media or a render conforms.
- Record parent IDs/hashes, intended scene/shot and frame range when defined, renderer/tool and exact version, project commit, configured settings (resolution, frame rate, color/audio, codec/container), command/configuration, render date, output hash/size and preview/WIP/final designation. Do not invent shot identifiers.
- Validate decodability and actual metadata, configured dimensions/FPS/duration/frame count, complete/nonduplicated frames, required audio track/channel/duration, sync, color, and unintended black frames/gaps/debug UI/watermarks/placeholders/missing assets. Retain logs and media/frame audit reports.
- Technical render validation is separate from visual/audio review. Creative authority reviews performance, continuity, composition and story intent; audio/editorial reviewer checks mix and sync. Record each applicable decision against exact render hash and purpose. Final episode delivery requires separate assembly, subtitle, credits, rights and final-master acceptance.
- Incomplete renders and unreviewed previews are not final or accepted production shots.

### 7.10 Music and other third-party media

For music, sound effects, footage, textures, stock/reference-derived elements and other external content, record creator/rightsholder, exact source/vendor/item reference, acquisition date, license/contract proof, file hash, edit/derivative history, attribution and scope/term/territory/monetization/redistribution restrictions. Record releases/consents for identifiable voices, performances, likenesses or locations where required. Confirm permission for intended editing, synchronization, public distribution, archive and reuse; credit as required. Rights/producer reviewer role must clear each item for the planned release. Unclear, expired, incompatible or unverifiable permissions require quarantine/rejection and a separately documented replacement. Presence in a render, demo or repository is not permission.

## 8. Integration evidence

When acceptance requires production-context integration, record the exact scene/project revision and dependencies, asset hashes actually loaded, configuration, test procedure/environment, logs/results, and review evidence. Test the intended use, not merely a generic loader or scaffold. For shared dialogue playback, verify one active transport, shared position for both actor queries, correct speaker isolation, pause/resume/seek/stop/end behavior and approved A/V offset across the complete intended dialogue. Integration proves exercised behavior only for the tested versions/configuration; it does not automatically confer creative approval or broaden authorized scope.

## 9. Evidence and claim boundary

A source artifact supports presence, not quality. Provenance supports traceability, not creative approval. A validation report supports only the checks and inputs it identifies. Integration evidence supports exercised behavior in that context, not general readiness. A render proves an output was produced, not that it was reviewed or that an episode is complete. Higher-level claims require all applicable underlying evidence and named decisions. State limitations explicitly; do not infer missing artifacts, approvals, test outcomes, or production completion.

## 10. Approval record minimum

For every accepted asset, retain a record with:

- Record type/ID; asset ID, type, version, exact SHA-256 and byte size.
- Intended purpose, use scope and restrictions.
- State and decision; date; role and assigned person when applicable.
- Separate technical, creative and rights decisions as applicable, each bound to the exact version/hash and purpose.
- Validation, provenance, rights, dependency, integration and review evidence references as applicable.
- Conditions, unresolved nonblocking notes, exception/expiry/recheck data if authorized, and change-control reference.

Use unassigned role labels until individuals are actually assigned. Never populate a record with fictional names, paths, dates, hashes, approvals, outcomes or shot IDs. An incomplete record is not an approval.

## 11. Lock gate and change control

An asset may be locked only after it is accepted; required technical, creative and rights approvals all refer to the same exact version/hash and purpose; target-version tests pass where applicable; dependencies and actual working bytes are verified; integration evidence exists where required; and manifest/reports are archived. Record accountable asset owner, technical reviewer, applicable creative approver, producer/rights approver when relevant, decision/date/scope/version/hash, test/report references, known nonblocking notes and change-control route. A lock is never implied by file presence, test pass, prior approval, or placeholder use.

Any proposed edit, replacement, re-interpretation, dependency/configuration change that affects validity, or change in use/scope requires a documented change request before implementation where practicable. The record identifies requester, reason, affected assets and downstream references, risk, impact assessment, test/validation plan, rollback/preservation plan, required role approvals, implementation evidence and closure decision. Keep accepted bytes and records immutable; create a separately identified revision with a new version and hash. Re-run impacted validation and integration, renew applicable creative/rights approvals for the changed exact version/purpose, assess downstream assets/scenes/renders for stale references, and record supersession. Emergency handling does not waive evidence or retrospective review. Do not silently substitute an accepted asset or alter a locked one.

## 12. Current evidence boundary

This specification defines gates; it is not evidence that any missing asset has been supplied, validated, approved, integrated or locked. The accompanying intake document reports that production WAV bytes, original character rigs/scenes and dependencies, a canonical complete screenplay, complete episode environments/body and final renders are not present in the inspected repository. Treat that as the intake document's reported inspection boundary, not an assertion about other locations or later changes. The shared audio-clock document labels its implementation scaffold as not production-validated. No production acceptance or LFS working-byte verification may be inferred from these documents alone.
