# HOLOS Episode 1 — Shot Production Planning Scaffold

**Document purpose:** planning scaffold only; this is not a shot list, storyboard, schedule, or production authorization.
**Real shot list status: BLOCKED** pending receipt and approval of the canonical screenplay, including its approved ending.
**Current evidence status:** the extracted screenplay is a working copy only and is not canonical.
**Register state:** no shot rows have been created.

## Evidence boundary and blocking notice

The user-pasted 53-shot table is **unverified**. It contains story beats not supported by the current canonical evidence, because no approved canonical screenplay and ending have been supplied. Do not use that table as a source for this plan: do not copy its plot, character actions, shot count, Region C material, or “Unknown Voice.” No item in that table is approved or scheduled by this scaffold.

The extracted screenplay at `docs/source_archive/2026-11-episode-1-the-moon-has-anger-issues-screenplay.extracted.md` is explicitly a consolidated, chat-derived working copy. It is not a certified recovery of the original screenplay and is **not canonical**. Its title, scenes, actions, dialogue, page markers, and ending must not be treated as approved production instructions. Existing four-turn dialogue/timeline artifacts and generic production infrastructure do not establish an approved complete screenplay, ending, shot list, or episode runtime.

Until the required approvals are recorded, leave the shot register empty. Do not infer, estimate, number, schedule, storyboard, or render real shots from working-copy text or the unverified table. Template placeholders below are schema fields only, not shot entries.

## Readiness gate: unblock creation of the real shot list

A producer or designated script authority must supply all of the following before shot breakdown begins:

- The canonical screenplay in its authoritative source format, with a stable version identifier and immutable file/hash or equivalent source identity.
- An explicit approval record naming the approver(s), approval date, and approved version; approval must cover the complete screenplay and ending.
- An explicit production instruction defining whether an approved storyboard/shot list already exists or whether the team is authorized to develop one from the approved screenplay.
- Any approved dialogue, timing, performance, pronunciation, editorial, and ending notes that constrain breakdown.

The script authority and producer must verify that the supplied source is complete and internally consistent. Record discrepancies and resolve them through formal change control; do not resolve ambiguities by inventing content. Only after this gate passes may the authorized team derive shot candidates from identified passages. Each candidate must remain unscheduled until the row-level evidence and asset gates below pass.

## Safe production stage workflow

Progression is evidence-based. A later stage cannot substitute for missing upstream approval. Record owner, reviewer, decision, date, and evidence for each applicable gate.

1. **Source intake and preservation:** inventory the supplied canonical script and production inputs; preserve originals; record paths, versions, hashes, provenance, and backup evidence. Mark the screenplay gate BLOCKED until explicit approval and ending are verified.
2. **Script authorization:** confirm canonical screenplay version, approval record, scope, complete ending, and permission to create a shot breakdown. Reject working copies and unverified pasted material as authority.
3. **Passage-linked breakdown:** draft a shot brief only from a cited, approved screenplay passage. Give each proposed shot a stable ID under the production naming convention; keep IDs stable across revisions and never recycle retired IDs. Record source passage/page and version. The director/editor reviews story coverage and shot intent.
4. **Asset identification and acceptance:** enumerate required assets by stable asset ID. Verify authoritative source, version, hash, provenance/license, technical validation, dependency status, and named acceptance. Placeholders, unknown assets, unapproved substitutions, or missing evidence block the shot.
5. **Scheduling authorization:** schedule a row only when its approved script passage is traceable and all required assets are accepted, with a named owner and approved duration/frame range. If either prerequisite changes or becomes uncertain, immediately BLOCK the row and remove it from the active schedule pending review.
6. **Preproduction:** approve shot brief, continuity context, layout, camera plan, acting/performance intent, dialogue/audio source and timebase, and timeline inputs. Resolve cross-shot dependencies before animation.
7. **Production:** create layout and camera blocking, animation blocking, then polish; preserve source links and record revisions. Do not fabricate dialogue, action, audio, or performance to fill gaps.
8. **Integration and technical QA:** integrate accepted assets and approved audio/timeline inputs. Validate dependencies, scene load, frame range, image/output settings, audio synchronization and continuity. Shared dialogue transport/timing must be linked to the selected exact audio bytes and corresponding timeline provenance; generic clock tests alone are not shot acceptance.
9. **Creative review and revision:** submit reviewable preview with versioned evidence. Named creative reviewer records approval or actionable notes. Revisions update the row and change log; re-review affected downstream work.
10. **Final render and lock:** verify final render completeness and technical metadata, check for missing/placeholder/debug artifacts and synchronization defects, obtain creative approval, archive evidence, then lock the shot. A locked shot may change only through approved change control.

## Row-level scheduling and acceptance gates

A row may not enter an active schedule unless all of these are true:

- It has a stable shot ID and an exact reference to an approved screenplay passage (scene and page/line or equivalent locator), with the source approval/version recorded.
- Its shot brief has the required creative approval and is consistent with that passage; no unsupported story beat or action has been introduced.
- Every required asset has a stable ID and is accepted with verifiable provenance, version/hash, technical validation, rights/provenance status, and named approval.
- Duration and frame range are explicitly approved, compatible with the project frame rate/timebase, and recorded as unambiguous inclusive/exclusive frame conventions.
- Required camera, acting, dialogue, audio, timeline, and continuity inputs are identified or explicitly marked not applicable by an authorized reviewer; unknown or unresolved inputs block scheduling.
- A responsible owner, technical QA owner, and creative reviewer are assigned, and the required evidence paths are present or have a documented pre-schedule exception approved by the production authority.

A row can be marked **SHOT APPROVED / LOCKED** only after its applicable workflow stages pass, technical QA evidence is attached, final-render verification is complete, creative approval is named and recorded, and all changes are closed or explicitly accepted. “Not applicable” requires a reason and reviewer; it is not a shortcut around a gate.

## Blank shot register

**No shot rows are populated.** Add a row only after the readiness and scheduling gates above pass. Duplicate the blank template as needed; do not assign placeholder IDs to represent speculative shots.

| Stable shot ID | Screenplay scene / page or passage reference | Source approval record / version / hash | Duration / frame range / timebase | Location (source-backed) | Characters (source-backed) | Required asset IDs and acceptance references | Camera inputs / approval | Acting or performance inputs / approval | Dialogue reference / approval | Audio source, hash, offset and sync inputs | Timeline inputs, provenance and version | Continuity references / checks | Responsible roles (owner, departments) | Technical QA criteria / evidence / status | Creative reviewer / decision / date | Evidence paths | Status | Change-control record |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

### Blank row field guidance

- **Stable shot ID:** assigned only to an authorized breakdown item; never infer IDs or count from the unverified table.
- **Screenplay scene / page or passage reference:** precise locator in the approved canonical source; include enough quotation/context in the evidence record to audit the derivation without replacing the source.
- **Source approval record / version / hash:** named approval and exact source identity used for the row.
- **Duration / frame range / timebase:** approved duration plus start/end frame convention, frame rate, and any source-audio timebase/offset where applicable.
- **Location, characters, dialogue, camera, acting:** only as authorized by the cited passage and approved creative direction; explicitly mark unresolved information BLOCKED.
- **Required asset IDs and acceptance references:** stable IDs only; link acceptance manifests/reports and exact versions/hashes.
- **Audio and timeline inputs:** exact selected audio file identity/hash, format/duration and approval; linked timeline identity/version/hash and timebase/offset. Do not silently select between competing audio variants.
- **Continuity:** preceding/following approved shot or scene references, state/prop/costume/lighting/audio continuity needs, and reviewer signoff; do not invent adjacent shots.
- **Responsible roles:** named or assigned accountable roles for production, departments, technical QA, and review.
- **Technical QA:** project-specific checks, expected output settings, integration/test/render evidence, and pass/fail owner.
- **Creative reviewer:** named authority, review artifact/version, decision, date, and notes/disposition.
- **Evidence paths:** repository-relative or controlled archive paths to source, approvals, assets, scene files, logs, previews, renders, and QA records.
- **Status:** use controlled values such as `BLOCKED`, `PROPOSED—NOT SCHEDULED`, `READY TO SCHEDULE`, `SCHEDULED`, `IN PRODUCTION`, `IN REVIEW`, `REVISE`, `TECHNICALLY ACCEPTED`, `CREATIVELY APPROVED`, `LOCKED`, or `CANCELLED`; status changes require recorded evidence and owner.
- **Change control:** change request ID, reason, requester, impacted source/asset/shot versions, approvals, affected downstream work, and revalidation/re-review evidence.

## Change control and audit trail

Any change to the canonical screenplay, ending, dialogue/audio source, accepted asset version, timing, frame range, camera/performance direction, continuity, or final render invalidates affected approvals until impact is assessed. Record the prior and new values, reason, request/approval identities and dates, affected shot IDs, downstream dependencies, and required re-tests/reviews. Preserve superseded evidence; do not overwrite approval history. If the screenplay source or approval is revoked or superseded, block all dependent rows and rescope them against the newly approved version before rescheduling.

## Current disposition

**Real shot list: BLOCKED.** No approved canonical complete screenplay and ending are established in the supplied evidence. The extracted screenplay is a working copy only. The user-pasted 53-shot table is unverified and must not be copied or used to populate this register. This document contains zero invented shot rows and authorizes no production scheduling.
