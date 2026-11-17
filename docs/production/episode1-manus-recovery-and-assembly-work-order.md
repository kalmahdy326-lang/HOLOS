# HOLOS — Episode 1 Asset Recovery, Access Verification, and Assembly Work Order

**Project author:** Khaled AL-MAHDY  
**Project:** HOLOS animated series  
**Episode:** Episode 1 — *The Moon Has Anger Issues*  
**Prepared for:** Manus  
**Purpose:** A source-aware production handoff for recovering existing material and assembling the most complete, honest, reviewable Episode 1 artifact supported by the evidence.

---

## 1. Mission and required result

Recover and inspect the existing Episode 1 source material, then assemble as much of the episode as the verified assets genuinely support.

The objective is **not** to make the episode look complete by filling gaps with invented content. The objective is to find everything that already exists, establish what it is, preserve its provenance, and make a watchable review artifact from the real material.

Work in this order:

1. Verify that Manus can access both the private GitHub repository and the HOLOS Project-space Library.
2. Inspect the default branch, all relevant open pull-request branches, and the available Library packages.
3. Recover and checksum actual source files; open and inspect both ZIP packages rather than treating them as opaque files.
4. Reconcile the screenplay extraction, 65-item text storyboard, character references, audio records, Godot infrastructure, and episode configuration.
5. Build a text-only storyboard-card animatic if no actual panel images or usable production scenes can be recovered.
6. Integrate and render real character or environment assets only if their original source files and dependencies are actually recovered and verified.
7. Deliver the playable review video, editable working project, inventories, validation evidence, and a precise missing-assets report.

A partial, clearly labelled review animatic is a valid result. A fabricated full episode is not.

**Do not spend the entire task writing a report.** Produce the best real review artifact the available evidence supports, even if it is a silent, text-only storyboard-card reel.

## 2. Access gate — check this before production work

### 2.1 GitHub access

The repository is private:

- Repository: kalmahdy326-lang/HOLOS
- Default branch: main
- Default-branch snapshot inspected for this work order: ba0f6687c2c14045ef88541a717249adcc7be3da

Confirm Manus can actually read the private repository. Confirm that it can inspect branches and pull-request heads, not just the default branch.

Do not print, request, or expose credentials or tokens. Do not initiate an authentication flow on the user's behalf.

### 2.2 Project-space Library access

**Library access is a critical dependency.** The original screenplay DOCX, three original character-guide PNGs, and two ZIP packages are recorded as Project-space Library items outside the default GitHub branch.

Confirm that Manus can search, download/materialize, and inspect those exact Library items. A Library metadata entry, filename, or size is not proof that the bytes are accessible.

The following were recorded in the source archive:

| Library source | Recorded size | Current evidence |
|---|---:|---|
| HOLOS_Episode_1_The_Moon_Has_Anger_Issues_Complete_Screenplay.docx | 48,709 bytes | Reported in Library metadata; original DOCX binary not verified in the checked GitHub checkout |
| HOLOS Character Guide: Moonlit Investigators.png | 2,013,102 bytes | Reference artwork described in the Library inventory |
| HOLOS Character Reference Sheet.png | 1,949,860 bytes | Reference artwork described in the Library inventory |
| HOLOS: Khaled and Kevin Character Sheet.png | 2,085,157 bytes | Reference artwork described in the Library inventory |
| HOLOS_Model_Initialization_Package.zip | 64,530 bytes | Located by name/metadata; contents not yet inspected |
| HOLOS_Autonomous_Execution_Package.zip | 21,652 bytes | Located by name/metadata; contents not yet inspected |

The two ZIP files are the largest unresolved source packages. Open both. List their contents, inspect the files, and determine whether they contain original Godot projects, character scenes, models, animations, images, scripts, audio, or other production material. **Do not infer their contents from their filenames.**

Preserve the original ZIP bytes. Record each ZIP's SHA-256 before extraction. Extract only to a new temporary/work directory, never over the original. Hash each recovered file and record the archive member path from which it came.

### 2.3 Knowledge entry

The project knowledge entry is reported at:

knowledge://knowledge/holos/KNOWLEDGE.md

Read it if Manus has access to that knowledge source. Do not claim to have read it if the knowledge:// source is unavailable. The repository source records and the evidence inspected in this task remain the controlling technical references.

### 2.4 Stop condition

If Project-space Library access is unavailable, record that immediately as a blocker. Continue with the GitHub branches that are accessible and produce the best GitHub-only inventory and text-card preview possible. Do not claim that the ZIPs, DOCX, or Library-only PNGs were inspected.

## 3. Verified repository starting state

The repository has important material outside main. **The default branch is not the whole current project.** Several relevant branches are open draft pull requests. They are unmerged and must be inspected explicitly.

Before relying on any branch, refresh its current head SHA and the pull-request status. The branch names and head SHAs below are the snapshot checked while preparing this work order.

| PR | Branch | Relevant contents | Boundary |
|---|---|---|---|
| [PR #6](https://github.com/kalmahdy326-lang/HOLOS/pull/6) | docs/milestone-5-1-four-turn-acceptance | Four-turn handoff records, absolute and review-relative timelines, alignment JSON, timeline builder, schemas and validation material | Alignment/timeline evidence is not the source audio master; no full-episode source MP3 is committed in this handoff |
| [PR #7](https://github.com/kalmahdy326-lang/HOLOS/pull/7) | feat/episode1-production-integration-scaffold | Shared audio transport adapter, asset-intake records, quality/acceptance records, and a character-design image | Integration scaffolding is not a recovered character rig |
| [PR #8](https://github.com/kalmahdy326-lang/HOLOS/pull/8) | feat/episode1-screenplay-storyboard-breakdown | Text-only 65-shot body storyboard, structured JSON breakdown, its JSON Schema, tests and screenplay-provenance gate | Draft previsualization material; no shot timing or panel artwork is supplied by the 65-item text breakdown |
| [PR #9](https://github.com/kalmahdy326-lang/HOLOS/pull/9) | docs/holos-series-bible | Series Bible, detailed text storyboard, source manifests, key-art image, Expression Sheet 1.1, theme M4A and 15-second test WAV | Open draft branch; its files are not part of main until merged |
| [PR #10](https://github.com/kalmahdy326-lang/HOLOS/pull/10) | docs/milestone-recovery-skill | Milestone recovery skill, Godot offscreen-CI reference and read-only CI status script | Useful existing recovery guidance; do not duplicate it or treat it as proof that production assets exist |
| [PR #12](https://github.com/kalmahdy326-lang/HOLOS/pull/12) | docs/episode1-screenplay-source-verification | Status pointer for the original-screenplay comparison blocker | Status-only companion; the detailed editorial/source protocol is in PR #9 |

PR #9 is stacked on PR #8; PR #8 is stacked on PR #7; PR #7 is stacked on PR #6. Confirm the actual current branch graph before fetching. Do not assume any of these changes have merged to main.

### 3.1 Important correction about media availability

The inspected main tree contains the production infrastructure and text/source records but no Episode 1 production audio or character-art binaries.

That does **not** mean there are no binary assets in the repository's current review branches:

- PR #7 contains production/character_references/episode1_character_design.png.
- PR #9 contains:
  - production/character_references/episode1_key_art_reference.png
  - production/character_references/holos_expression_sheet_1_1.webp
  - production/audio/holos_theme_song_source.m4a
  - production/audio/milestone_5_1_animation_test_audio_15s.wav

Inspect those exact files on their PR branches. Do not search only main and then report that no GitHub media exists.

The three separately listed Library character-guide PNGs are not automatically identical to the images in PR #7 or PR #9. Compare actual bytes, hashes, and visible content before treating them as duplicates.

## 4. Screenplay authority and story continuity

### 4.1 What exists

The repository contains a 25-page consolidated screenplay text extraction:

docs/source_archive/2026-11-episode-1-the-moon-has-anger-issues-screenplay.extracted.md

The extraction records the original filename as:

HOLOS_Episode_1_The_Moon_Has_Anger_Issues_Complete_Screenplay.docx

The extraction is useful and detailed, but it identifies itself as a consolidated chat-derived working copy that was not compared verbatim against the original DOCX. The DOCX's 48,709-byte Library metadata is reported; the original binary has not been verified in the inspected GitHub checkout.

### 4.2 Required source comparison

If Manus can retrieve the actual DOCX:

1. Preserve the original bytes, including comments and tracked changes.
2. Record exact filename, file size, known revision/date, and SHA-256.
3. Work from a separate read-only copy.
4. Compare the original against the GitHub Markdown extraction and all 65 storyboard items.
5. Preserve the original DOCX unchanged.
6. Record evidence by page/paragraph/panel and identify exact wording, omissions, additions, and ambiguities.
7. Do not settle disputed wording or tracked changes without project-author direction.

Use only the established dispositions:

- SUPPORTED
- MISSING_OR_ALTERED
- UNSUPPORTED
- AMBIGUOUS — AUTHOR DECISION

The 65-panel screenplay comparison is currently blocked until the authoritative DOCX bytes and revision authority are established. Do not claim screenplay fidelity, approval, or a completed comparison merely because the extraction exists.

If the DOCX cannot be accessed, keep the screenplay comparison marked **BLOCKED** and proceed only with a preview explicitly based on the unverified extraction.

### 4.3 Episode continuity summary

Use the extracted screenplay as the detailed source. The current project summary describes this broad progression:

- Khaled disconnects Region C.
- An earlier-timestamped transmission appears despite that disconnection.
- In the lower array, Kevin bypasses an authorization warning and connects a processor, creating an uncontrolled feedback path.
- The station destabilizes and Kevin is injured.
- Khaled and Kevin investigate and intervene, preserve raw observations, restore the original partition, and disable the feedback layer.
- The geometry readings move toward baseline, but the characters do not establish a general information–geometry law or identify the source of the Moon's voice.

This summary is a navigation aid, not a replacement screenplay. Confirm every beat against the actual available script before assembling dialogue or changing scene order.

Project continuity identifies the setting as a heavily shielded lunar research station in Mare Umbrae. The investigation involves observation regions A, B and C, binary records, and anomalous geometric/gravitational readings. Keep correlation separate from causation. Do not turn a fictional observation into a claim that real physics has been demonstrated.

The Moon's origin remains unresolved. Preserve the mystery. Do not add a backstory or explanation.

## 5. Storyboard: 65 text items, not 65 finished shots

The structured storyboard is on PR #8:

- Markdown: docs/episode1-body-storyboard-draft.md
- JSON: config/episode1/episode1_storyboard_breakdown_v1.json
- Schema: config/schemas/holos-storyboard-breakdown-v1.schema.json
- Detailed panel breakdown on PR #9: docs/episode1-detailed-storyboard-panel-breakdown-v1.md

The JSON was inspected and contains:

- schema_version: 1
- approval_status beginning with DRAFT
- 8 scene groups
- 65 shot rows in total
- 8 string fields per shot row
- Seven main narrative scenes plus the post-credit scene
- No assigned frame ranges or shot durations

The 8 group titles in the structured breakdown are:

1. Nothing Exists Alone
2. The Voice of a Whole
3. Four Explanations and One Very Bad Idea
4. The Boundary Problem
5. When the Whole Bites Back
6. The Test
7. The Thing We Didn’t Find
8. Post-Credit Scene

The terms **65-shot** and **65-panel** refer to this same 65-item text storyboard/previsualization inventory in the current records. They do not mean that 65 image panels have been recovered, that 65 scenes are animated, or that 65 finished shots exist.

Preserve every existing shot/panel ID and sequence exactly. Do not silently reorder, merge, split, delete, rename, or invent storyboard entries. Use the structured JSON and schema as the source for exact IDs and field content. Keep all eight fields and their original association with each ID.

### 5.1 If no panel images exist

The text storyboard is not a collection of panel images. If Manus cannot recover actual panel art from the Library archives or another verified source:

- Build 65 clean, readable **text-only storyboard cards**.
- Each card must display its exact original panel/shot ID.
- Copy the actual storyboard description and other relevant fields without changing their meaning.
- Preserve the eight scene groups and their order.
- Use typographic hierarchy, neutral backgrounds, and simple layout only.
- Do not draw, generate, synthesize, or source substitute character portraits, environments, props, station imagery, or fake storyboard artwork.
- Do not present a text card as an original storyboard image.
- Do not label the cards as animation.

The approved key art may be consulted as a style reference. It is not permission to invent new art or alter the original key-art image.

## 6. Characters and visual authority

### 6.1 Character identity mapping

The project-author-confirmed mapping is:

- **Character B = Khaled**
- **Character A = Kevin**

The source archive describes the character references as follows:

| Character | Reference description | Story role |
|---|---|---|
| Khaled (B) | Age 38; 6'1"; brown hair; blue eyes; senior researcher; restrained and analytical presentation | Senior relational physicist/researcher |
| Kevin (A) | Age 23; 6'0"; red hair; blue eyes; junior investigator; more expressive and rebellious presentation | Junior systems investigator |

Use the actual supplied reference sheets as the visual authority. Do not invent additional facial, clothing, body, or rig details from filenames or memory.

### 6.2 Approved key art and expression correction

The PR #9 key-art manifest records the user-approved image as the **official HOLOS series-wide visual style guide**.

- Key-art repository file: production/character_references/episode1_key_art_reference.png
- Manifest SHA-256: ea065d17db8e3e16bb6dc07615641865ce8508e1b94cc7ecb4bc6c05daf31ab8
- Recorded size: 2,654,633 bytes

That approval applies to its role as the series-wide style guide. It does **not** by itself approve a final release poster, official editable logo master, final title-card master, or distribution/rights use.

Expression Sheet 1.1 is separately preserved:

- Repository file: production/character_references/holos_expression_sheet_1_1.webp
- Manifest SHA-256: 245ae91beaede1e2fdc42c299c08ecea477d0fdeb97333aed4ccfc1d257d08ad
- Recorded size: 182,186 bytes

The project author confirmed that the two portraits in the **“Surprised”** panels placed under Kevin (A) actually depict **Khaled (B)**.

Therefore:

- Map those two portraits to Khaled, not Kevin.
- Preserve the supplied original sheet unchanged.
- Correct their placement/labels only in an explicitly identified working derivative.
- Do not infer rig controls, visemes, animation timing, or performance from an expression-sheet picture.

### 6.3 Character and voice separation

Keep the in-story identities distinct. Khaled, Kevin, ORBIT, the Moon/Lunar Interface, and the Fourth Signal must not be casually collapsed into one another. The external theme singer/narrator is not automatically a character voice. A separate “God” reference in other audio material is unconfirmed; do not assign it to a character or storyline without source evidence.

The Moon is an unidentified speaking presence communicating through station infrastructure in the current story concept. The screenplay does not specify a humanoid Moon character. Do not create one.

ORBIT is the station AI/system voice and must remain distinct from the Moon's presence.

## 7. Audio: recover and document; do not silently select

### 7.1 Theme-song source

PR #9 contains the user-supplied theme-song M4A:

- File: production/audio/holos_theme_song_source.m4a
- Original supplied filename in manifest: HOLOStheme.m4a
- SHA-256: aee4733881850f4a3a83be5ae6b69c94cdbbbebc4467916ad3aeec5b3e3bd09e
- Size: 1,307,950 bytes
- Observed: AAC, 48 kHz, stereo, 209 seconds, M4A container

The user identified this as the HOLOS theme song. The manifest says no subjective listening/lyrics approval, rights/authorship/credits review, loudness review, final placement, or final-mix approval has been completed.

Preserve it as a source asset. Do not assume it is the final intro, outro, recurring score, episode dialogue bed, or approved distribution master. Do not edit or transcode the original.

### 7.2 Fifteen-second animation-test WAV

PR #9 contains:

- File: production/audio/milestone_5_1_animation_test_audio_15s.wav
- Supplied filename in manifest: holos_animation_test_audio_15s.wav
- SHA-256: 1c352af5c428e01fb6205071127c27b85e0f259bc6506d181cd47a864095e1da
- Size: 2,880,078 bytes
- Observed: PCM signed 16-bit little-endian, 48 kHz, stereo, 15 seconds

This is test material, not the full-episode dialogue master. Its content, transcript, and approval have not been independently verified.

A supplied discrepancy report describes an extra leading “But” and a truncated final line after “380,000.” The original path cited by that report was not available in the earlier inspection. Matching filename, format, and duration do not prove that the report analyzed these exact WAV bytes. Do not claim byte identity unless the source report and file are independently reconciled.

### 7.3 Four-turn handoff and competing review WAV variants

PR #6 contains a real alignment/timeline handoff. Its records describe:

- 189 events in each of the absolute and review-relative timelines.
- A 0.091-second absolute/relative offset.
- Alignment material reporting 317 segments and 33 aligned words in the reviewed interval.
- Source-MP3 hash recorded as e4b13c06a6c3fbca9449cffb9135d7259b62e059a3c2d1fa37085afae65b865f.

The source MP3 bytes are not committed in the inspected handoff. The existence of the alignment JSON does not mean the source audio is available or that the full episode has been synchronized.

The asset-intake record names two competing review-WAV variants:

- Manus WAV SHA-256: 4b8c1d78ac6ca233f9ae2ba3f31566baaa75a83802eac8257ba7cba48cd76730
- Codex WAV SHA-256: e9d8a3a88f310b1558a884fcec87f8cf16741019ddbcede2a2db2cc2db74194f

**Do not choose between these variants.** Keep them separate, record which files are actually accessible, and report the discrepancy for project-author selection.

### 7.4 Audio search instructions

Search all accessible GitHub PR branches, Library locations, ZIP members, local handoff folders, and connected project locations for:

- Full-episode dialogue master.
- Four-turn dialogue sources and review WAVs.
- Theme and bookend music.
- Separate music, ambience, sound effects, and stems.
- WhisperX transcripts, acoustic alignment, phoneme/viseme timelines, manifests, DAW sessions, and export scripts.
- Animation test clips and their matching source audio.

For every actual audio file, record source location, filename, size, SHA-256, container/codec, sample rate, channels, bit depth where applicable, duration, and provenance. Use FFprobe or an equivalent tool. Keep byte-identical originals read-only and derived files in a separate work directory.

Do not invent dialogue, repair a missing line by writing it, choose a review WAV, or treat a 15-second test as the full episode.

**Default review-video audio policy:** if no approved, full-episode audio master is recovered and selected by the project author, make the text-card review MP4 silent. Do not use the theme M4A or the test WAV as a substitute dialogue track.

## 8. Godot and production-engine reality

### 8.1 What the default branch actually contains

The default branch contains a minimal Godot project and generic production infrastructure:

- godot/project.godot
- godot/holos_shot_runner.gd
- godot/holos_timeline.gd
- godot/test_scenes/adapter_test.tscn
- godot/test_scenes/adapter_test.gd
- godot/test_scenes/timeline_selftest.gd

The two test scenes must not be mistaken for production scenes:

**Adapter test:** adapter_test.tscn loads a generic Node2D script that draws a dark test background, a moving circle, and a test label in a 320×180 viewport. It proves the generic shot-hook/rendering fixture can draw frames. It is not Khaled, Kevin, an environment, or a production scene.

**Timeline self-test:** timeline_selftest.gd builds synthetic event arrays and tests timeline acceptance/rejection, speakers, visemes, duration, ordering, and state-at-time behaviour. It requires no source audio, images, or character rigs. It is not an animation test of a real character.

The generic shot runner loads a PackedScene and optionally calls:

- holos_apply_shot(config)
- holos_set_frame(frame_index, fps)

It owns deterministic frame stepping and PNG capture. It does not define character animation, dialogue, scene composition, or character artwork.

PR #7 adds a shared audio transport adapter for future actor adapters. It is integration scaffolding only. It does not provide rigs, choose an audio master, or prove lip-sync.

### 8.2 Actual rig status — the 12 November reconciliation controls

Read:

- docs/rig-source-reconciliation-2026-11-12.md
- docs/character-rig-integration-contract.md
- docs/milestone-6-local-production-engine.md

The 12 November rig-source reconciliation is the controlling status record. It identifies conflicting earlier records, including an 8 November report of a completed Khaled rig and a Milestone 6 preservation list referring to both rigs and an interaction prototype.

The current defensible status is:

- Reference/concept artwork exists.
- No original Khaled or Kevin production rig scene and full dependency set is verified in the inspected GitHub tree.
- The earlier Khaled rig-completion claim does not substitute for an available, inspectable original scene.
- Kevin's original scene and dependencies are also unverified.
- The two-character interaction prototype is claimed in one record but its actual source scene/benchmark is not present in the inspected repository tree.
- The generic adapter is not a character rig.
- Both original rig handoffs remain blocked pending recovery and source evidence.

**Do not generate substitute rigs.** Do not clone one character's rig for the other. Do not infer which rig to load from filenames, portrait appearance, or folder names. Do not describe a new test character as Khaled or Kevin.

If a ZIP actually contains a candidate rig, treat it as a candidate until its origin, completeness, dependencies, character mapping, and benchmark are verified. Work from a separate copy after hashing and backing up the archive.

### 8.3 Godot version and CI caveat

The project context targets Godot 4.7.2. Confirm the actual version installed in Manus's workspace with the executable itself. The PR #8 CI record reports a successful run using Godot 4.4.1; that is not proof of compatibility or acceptance under 4.7.2.

Do not declare the target runtime validated unless it was actually run and recorded. Distinguish script/import/headless logic checks from pixel-producing frame capture and visual inspection. A headless test pass is not a rendered video.

### 8.4 Render pipeline

The existing architecture is:

- Python: config validation, asset resolution, scheduling, resumable shot rendering, backups, reporting and output validation.
- Godot: scene loading, frame stepping, animation and PNG capture.
- FFmpeg/FFprobe: image-sequence and audio assembly, encoding and media validation.
- JSON: episode, scene, shot, character, audio and render settings.

The CLI includes validate, preflight, render, render-episode, and assemble-episode commands. Episode assembly requires a complete verified per-shot manifest and exact frame sequences. The media assembler refuses to overwrite an existing output and validates the resulting media.

Important implementation detail: each rendered shot must specify a Godot scene using a res:// path. The renderer passes the shot ID and render settings into the generic scene hooks. A static text-card scene can use the shot ID to look up its card text in a separate card-data JSON file.

The engine's render capture is not genuinely pixel-producing in a pure headless session. Use a rendering-capable display or a correctly configured virtual display/capture method. Follow the existing PR #10 Godot offscreen-CI guidance rather than relying on a test name that says “render.”

## 9. Episode JSON and storyboard JSON are different contracts

Do not conflate the 65-item storyboard data with the engine's episode configuration.

### 9.1 Engine episode configuration

The current default-branch example is:

examples/episode_01.json

It contains:

- schema_version: 1
- Episode ID and title
- Render: 1280×720, 24 fps, production mode, libx264, yuv420p
- Audio: dialogue path assets/audio/dialogue.wav, music null, 80 ms sync tolerance
- One scene, Opening
- One shot, S01_B01, frames 0–240, with placeholder timing and no asset declarations

Its description explicitly says it is a starter configuration and that placeholder paths/timing must be replaced with verified production data.

The episode configuration is validated in holos_engine/config.py. No separate formal JSON Schema for this engine episode config was found in the inspected default branch. The validator enforces version 1, episode identity/title, positive render dimensions and FPS, non-empty scenes/shots, unique scene/shot IDs, valid frame ranges, character arrays, and audio path/tolerance types.

**Additional render requirement:** the current renderer requires each shot to contain a scene value beginning with res:// and pointing to an existing Godot PackedScene. The basic Python config validator does not check this. The starter examples/episode_01.json has no scene path, so passing validate alone does not make that example render-ready.

### 9.2 Storyboard breakdown JSON

The separate PR #8 storyboard file is:

config/episode1/episode1_storyboard_breakdown_v1.json

Its separate schema is:

config/schemas/holos-storyboard-breakdown-v1.schema.json

It uses JSON Schema draft 2020-12 and records the storyboard document ID, source provenance, DRAFT approval status, delivery reference, timing policy, eight scene groups, and 65 eight-field shot rows.

This JSON is the text storyboard inventory. It is not a drop-in replacement for examples/episode_01.json and is not itself sufficient to render the episode.

### 9.3 Required editable preview configuration

Create a separate working configuration such as:

output/HOLOS_EPISODE_1_ASSEMBLY/episode_01_review_animatic.json

Requirements:

- Use engine config schema_version: 1.
- Preserve all 65 original storyboard IDs and their order.
- Preserve all eight scene groups.
- Do not modify the source storyboard JSON or the starter examples/episode_01.json.
- Use the existing Python config validator.
- Read the renderer implementation and provide a valid scene path for every shot.
- Use a generic text-card PackedScene in the isolated working project if no real production scene is available.
- The text-card scene must implement the existing holos_apply_shot and holos_set_frame hooks.
- Use the shot ID passed by the runner to look up exact card text in a separate JSON data file.
- Do not change the generic runner or production engine just to make the preview look animated. If a production-code change appears necessary, document it as a proposed change and keep it separate for review.

For the text-card read-through only, use a **provisional six-second card display hold** at 24 fps (144 frames per card). This is a temporary readability/display choice for the review reel, not an editorial shot duration, not screenplay timing, and not an approved production frame range. Record it explicitly as review-only metadata. Never copy these holds back into the canonical storyboard breakdown or treat them as final shot timing.

## 10. Review render profile

For the text-card **review animatic**, use the existing starter profile:

- Resolution: 1280×720
- Frame rate: 24 fps
- Video codec: H.264 via libx264
- Pixel format: yuv420p
- Container/output: MP4, with fast-start metadata where supported
- Default audio: none; create a silent MP4 unless a full-episode audio source is verified and explicitly selected by the project author

This is the review-animatic profile recorded in the starter config and storyboard delivery reference. It is not a locked final delivery profile.

The Series Bible records a separate requested final-delivery target of 1920×1080 at 30 fps with 48 kHz stereo audio, also not yet locked by a versioned delivery-profile approval. Keep the review profile and final-delivery target distinct. Do not silently resolve that difference by changing either source record.

If a user-approved full audio source becomes available later, preserve its original bytes, make a separately identified derived mix, and validate the resulting streams. The engine's default A/V sync tolerance is 80 ms; use it only as a technical validation threshold, not as proof that any source track is approved.

## 11. Assembly stages

### Stage A — access and read-only inventory

- Confirm repository and Library access.
- Record Git status, checked-out refs, PR heads, exact commits and uncommitted changes in Manus's workspace.
- Search all relevant sources; do not limit the search to main.
- Search archives, ZIP packages, Project-space Library files, source handoffs and connected project directories.
- Inventory every relevant file with source location, filename, size and SHA-256.
- For media, add format/codec, resolution, duration, sample rate, channel count, and other relevant metadata.
- Separate originals, derivatives, exports, test fixtures, manifests, and generated outputs.
- Make a verified backup before any integration activity.

### Stage B — source recovery

- Retrieve the original DOCX if accessible and preserve it unchanged.
- Open both ZIP packages and inspect their complete contents.
- Recover original Godot projects, scenes, rig scripts and transitive resources if present.
- Recover original source artwork, environments, props, backgrounds, logos, fonts, dialogue and audio stems if present.
- Record where every file came from, including ZIP member path or Library item identity.
- Hash source files before processing and hash extracted/copy files after recovery.
- Never assume a file is authoritative simply because its name sounds correct.

### Stage C — storyboard reconciliation and mapping

- Load the eight scene groups and 65 rows from the structured JSON.
- Check the Markdown and JSON shot IDs for exact ordered parity.
- Check that all IDs are unique and preserve the source order.
- Build a per-ID map from storyboard fields to recovered artwork/audio/assets.
- Identify missing source files per ID.
- Do not invent durations, dialogue, actions, camera moves, or continuity corrections.
- Use the four screenplay-comparison dispositions if the DOCX is available; otherwise mark comparison blocked.

### Stage D — build the text-card animatic when necessary

If no usable panel images, production scenes or original rigs are recovered:

1. Build one text card for each of the 65 storyboard items.
2. Show the exact ID and the original text from the structured source.
3. Use the eight group titles as section labels only; do not add narrative or scene content.
4. Use neutral typography and simple layouts.
5. Make a separate card-data JSON indexed by exact shot ID.
6. Create a generic static-card scene in an isolated working copy, not a character replacement.
7. Create a separate version-1 episode review config that points to that scene.
8. Validate the config, render frames, assemble the review MP4, and inspect the result.
9. Label it clearly as a **TEXT-ONLY STORYBOARD REVIEW ANIMATIC — NOT CHARACTER ANIMATION OR A FINAL EPISODE**.

Do not create AI-generated or hand-drawn substitute character/environment imagery. No paid software, subscription, or AI-generation credits are authorized by this work order.

### Stage E — integrate real production assets only if recovered

If actual original rigs and source dependencies are found:

- Verify the complete source project, rig dependencies, Godot version, backups and benchmark files.
- Follow the character-rig integration contract.
- Keep Khaled and Kevin as independent rigs and adapters.
- Do not rename or alter original source resources during intake.
- Do not connect a rig based only on an image or a filename.
- Render an isolated neutral benchmark for each character before attempting a full scene.
- Compare against the preserved character reference/benchmark and record differences.
- Run a two-character interaction only after both independent rigs pass their checks.
- Do not claim Milestone 6 or a character milestone complete from a generic fixture render.

If only some original scenes are recovered, assemble only those verified scenes and use clearly labelled text cards or black/neutral placeholders for the remaining storyboard items. Do not conceal gaps.

### Stage F — audio integration

- Map every recovered audio asset to its actual source and intended use.
- Keep theme, dialogue, effects, ambience, review WAVs and alignment files separate.
- Do not select the Manus or Codex review WAV.
- Do not use the 15-second test WAV as a full-episode master.
- Do not assume the 209-second theme M4A is approved final music.
- If no approved full-episode audio exists, render the review animatic silently.
- If a source is found but not approved, create a separately labelled candidate only if it can be done without changing originals; do not make it the default/final track.

### Stage G — validate and inspect

At minimum:

- Validate the version-1 episode config using the repository's Python validator.
- Confirm each shot's res:// scene path actually resolves.
- Confirm scene and shot counts, IDs, order and frame counts.
- Confirm the expected number of non-empty PNG frames per shot.
- Check output frame dimensions and frame rate.
- Run FFprobe on the assembled MP4 and record actual codec, pixel format, duration, stream count and metadata.
- If audio is present, record its source hash and validate start offset and duration against the configured tolerance.
- Inspect the beginning, middle, end, scene transitions, text clipping, readability, blank frames, and any missing sequence.
- Confirm no debug overlays appear in production mode.
- Distinguish a headless logic pass from actual pixel-producing render evidence.
- Record exact tool versions and commands.

Do not call a video “complete” merely because FFmpeg produced a file. The file must be probed and viewed, and its limitations must be stated.

## 12. Output folder and deliverables

Create all Manus work in a new output directory. Do not overwrite any existing project, repository, or asset folder.

Suggested structure:

~~~text
HOLOS_EPISODE_1_ASSEMBLY/
  00_ACCESS_AND_SOURCE_STATUS/
    access_report.md
    repository_refs.md
    library_access_report.md
  01_SOURCE_INVENTORY/
    asset_inventory.csv
    sha256_manifest.txt
    archive_contents/
    media_metadata/
  02_SCREENPLAY_AND_STORYBOARD/
    screenplay_provenance_report.md
    screenplay_comparison/
    storyboard_id_map.csv
    storyboard_mapping_report.md
  03_VISUAL_ASSETS/
    character_reference_map.md
    visual_asset_manifest.csv
  04_AUDIO/
    audio_asset_map.md
    audio_manifest.csv
    audio_candidate_reports/
  05_REVIEW_PROJECT/
    episode_01_review_animatic.json
    storyboard_cards.json
    godot_review_project/
    scripts/
  06_STORYBOARD_CARDS/
    png/
    contact_sheet/
  07_VIDEO/
    HOLOS_Episode_1_Text_Storyboard_Review.mp4
    ffprobe_report.json
    visual_inspection_report.md
  08_PARTIAL_PRODUCTION/
    verified_shot_renders/
    partial_assembly.mp4
    per_shot_manifest.json
  09_MISSING_ASSETS_AND_REPORTS/
    missing_assets.md
    final_status_report.md
~~~

Required deliverables:

1. **Access report** stating exactly which GitHub refs and Project-space Library sources Manus could access.
2. **Complete asset inventory** with source locations, sizes and SHA-256 hashes.
3. **ZIP inspection report** listing every archive member and identifying useful, irrelevant, missing, corrupt or inaccessible contents.
4. **Screenplay/source status report** with original DOCX availability, file hash, revision/date if known, and comparison status.
5. **65-item storyboard map** preserving all IDs, field values and order.
6. **Visual reference map** separating approved key art, expression sheet, other character references, actual production assets and missing assets.
7. **Audio map** separating theme, test WAV, dialogue candidates, alignment files and unverified sources.
8. **Editable review project** using the existing version-1 episode-config contract and a separate generic text-card scene if needed.
9. **Watchable MP4 review animatic**, even if it must be text-only and silent.
10. **Partial production assembly**, only where real source assets and scenes support it.
11. **Validation and visual-inspection evidence**, including commands, tool versions, reports and exact output metadata.
12. **Missing-assets and blockers report** with the evidence needed to proceed.

## 13. Preservation, safety and approval rules

These rules are mandatory:

- Never overwrite, delete, move, or rename original files.
- Never edit the original screenplay DOCX, original reference PNGs, original theme M4A, test WAV, or source ZIP archives.
- Do not change the existing Series Bible while performing this task.
- Do not silently update the canonical storyboard, screenplay extraction, audio timeline, manifests, acceptance records, or episode JSON starter.
- Do not create substitute Khaled/Kevin rigs.
- Do not create substitute character/environment art or use AI image generation.
- Do not invent dialogue, scenes, panel descriptions, camera directions, audio content, scientific explanations, or approvals.
- Do not turn a storyboard into an approved shot list.
- Do not turn placeholder display holds into official shot durations.
- Do not treat the generic test scene as character animation.
- Do not select the competing Manus/Codex WAV variants.
- Do not promote the theme M4A or 15-second WAV to final episode audio.
- Do not commit, push, merge, close, or retarget any repository PR.
- Do not commit Manus output into the project repository. Return it as a separate package for project-author review.
- Do not claim that offline acceptance, final render acceptance, rights approval, screenplay approval, or Milestone 6 completion occurred unless the required test and approval evidence exists.
- Never include access tokens, secrets, personal credentials, or authentication files in inventories or outputs.

The project is local-first. Manus is an optional development/recovery assistant, not a production runtime dependency. No paid software or AI credits are authorized.

## 14. Series Bible review notes — context, not a request to edit the Bible

A separate content review of the relocated Series Bible copy found that its claims generally align with the source records, but its new location breaks 28 relative links and its document-name field still names the root source. The review also identified two decisions recorded in manifests that should be marked resolved in a future approved Bible revision:

- The key-art image is approved as the series-wide style guide.
- The two “Surprised” portraits placed under Kevin belong to Khaled.

Production application of those decisions remains distinct from the approvals themselves.

The same review confirmed that the original DOCX is reported in metadata, not verified byte-for-byte; that the 65-shot/65-panel wording needs a same-inventory clarification; and that theme/test-audio metadata does not equal final lyrics, rights, transcript, or mix approval.

**Do not edit or relocate the Bible during this assembly task.** Its review corrections belong in a separately approved Bible revision. The root source is to remain untouched.

## 15. Final report — answer each question directly

At the end, answer these with numbers, filenames, hashes, links and evidence where available:

1. Could Manus access the private HOLOS repository and which exact branches/PR heads were inspected?
2. Could Manus access the Project-space Library? Which of the DOCX, three PNGs and two ZIPs were actually opened?
3. What did each ZIP contain? Which files were extracted and hashed?
4. Was the authoritative original DOCX recovered? What is its size/hash/revision, and was the comparison completed?
5. Were all 65 storyboard IDs found, in order? Were all eight groups preserved?
6. Did any real storyboard panel images exist? If not, were all 65 text cards created?
7. Were original Khaled and Kevin rig scenes and dependencies recovered? Identify exact paths and hashes, or state that each remains blocked.
8. What did the two Godot test scenes actually test? What target Godot version was run?
9. Which audio assets were recovered? Was a full dialogue master found? Were competing WAV hashes kept separate?
10. Was the version-1 review episode config validated? Did every shot resolve to a real res:// scene?
11. How many shots were rendered from real production assets, and how many were text-only cards?
12. Was an MP4 actually produced and inspected? Give exact path, size, duration, resolution, frame rate, codec, pixel format and audio status.
13. What CI, Godot, FFmpeg/FFprobe and visual-inspection checks were run, and what passed/failed?
14. What is the exact list of remaining blockers and the next source item required from the project author?
15. What can honestly be called complete, partial, draft, blocked, unverified, or awaiting approval?

Use evidence-based status language. If something was not accessible, say so. If a file was merely listed in metadata, say it was listed, not inspected. If an MP4 is text-only, call it a text-only storyboard review animatic. If no real character rigs are recovered, say so directly.

---

## 16. Primary repository references

- [HOLOS Series Bible on PR #9](https://github.com/kalmahdy326-lang/HOLOS/blob/docs/holos-series-bible/HOLOS_SERIES_BIBLE.md)
- [Source archive README](https://github.com/kalmahdy326-lang/HOLOS/blob/main/docs/source_archive/README.md)
- [Extracted Episode 1 screenplay](https://github.com/kalmahdy326-lang/HOLOS/blob/main/docs/source_archive/2026-11-episode-1-the-moon-has-anger-issues-screenplay.extracted.md)
- [Episode 1 production asset intake on PR #9](https://github.com/kalmahdy326-lang/HOLOS/blob/docs/holos-series-bible/docs/episode1-production-asset-intake.md)
- [Episode 1 body storyboard draft on PR #8](https://github.com/kalmahdy326-lang/HOLOS/blob/feat/episode1-screenplay-storyboard-breakdown/docs/episode1-body-storyboard-draft.md)
- [65-item storyboard JSON on PR #8](https://github.com/kalmahdy326-lang/HOLOS/blob/feat/episode1-screenplay-storyboard-breakdown/config/episode1/episode1_storyboard_breakdown_v1.json)
- [Storyboard JSON Schema on PR #8](https://github.com/kalmahdy326-lang/HOLOS/blob/feat/episode1-screenplay-storyboard-breakdown/config/schemas/holos-storyboard-breakdown-v1.schema.json)
- [Detailed storyboard panel breakdown on PR #9](https://github.com/kalmahdy326-lang/HOLOS/blob/docs/holos-series-bible/docs/episode1-detailed-storyboard-panel-breakdown-v1.md)
- [Screenplay provenance and editorial gates](https://github.com/kalmahdy326-lang/HOLOS/blob/docs/holos-series-bible/docs/episode1-screenplay-provenance-and-editorial-gates.md)
- [Rig-source reconciliation — 12 November](https://github.com/kalmahdy326-lang/HOLOS/blob/main/docs/rig-source-reconciliation-2026-11-12.md)
- [Character-rig integration contract](https://github.com/kalmahdy326-lang/HOLOS/blob/main/docs/character-rig-integration-contract.md)
- [Milestone 6 local production engine](https://github.com/kalmahdy326-lang/HOLOS/blob/main/docs/milestone-6-local-production-engine.md)
- [Episode starter configuration](https://github.com/kalmahdy326-lang/HOLOS/blob/main/examples/episode_01.json)
- [Episode config validator](https://github.com/kalmahdy326-lang/HOLOS/blob/main/holos_engine/config.py)
- [Godot shot runner](https://github.com/kalmahdy326-lang/HOLOS/blob/main/godot/holos_shot_runner.gd)
- [Milestone 5.1 four-turn handoff — PR #6](https://github.com/kalmahdy326-lang/HOLOS/pull/6)
- [Production integration scaffold — PR #7](https://github.com/kalmahdy326-lang/HOLOS/pull/7)
- [Storyboard breakdown — PR #8](https://github.com/kalmahdy326-lang/HOLOS/pull/8)
- [Series Bible and supplied audio/assets — PR #9](https://github.com/kalmahdy326-lang/HOLOS/pull/9)
- [Milestone recovery skill — PR #10](https://github.com/kalmahdy326-lang/HOLOS/pull/10)
- [Screenplay comparison status pointer — PR #12](https://github.com/kalmahdy326-lang/HOLOS/pull/12)

**Project principle:** We are not trying to make our theory right. We are trying to find out what is right. Apply the same standard to the production record: preserve what exists, test what can be tested, and label everything else honestly.
