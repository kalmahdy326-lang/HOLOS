# HOLOS Episode 1 — Production Asset Intake

**Owner / project author:** Khaled AL-MAHDY  
**Status:** Intake specification — selected source assets have been received; the complete production package has not been validated.
**Rule:** Preserve originals. Do not create substitute character rigs, voice tracks, screenplay pages, environments, or approval records.

This checklist separates verified repository materials from the source package required to produce the episode.

## 1. Existing repository evidence

- [x] Milestone 5.1 four-turn handoff is present on PR #6.
- [x] Absolute and review-relative JSON timelines are present (189 events each).
- [x] Approved four-turn transcript is embedded in the timeline documents.
- [x] Source MP3 SHA-256 is recorded as `e4b13c06a6c3fbca9449cffb9135d7259b62e059a3c2d1fa37085afae65b865f`.
- [x] Reusable title/credits bookend scene and generic renderer infrastructure exist.
- [x] User-supplied theme-song source is present at [`production/audio/holos_theme_song_source.m4a`](../production/audio/holos_theme_song_source.m4a); its local metadata and SHA-256 are recorded in the companion manifest. Creative approval, rights/credits, and final placement/mix remain unverified.
- [x] User-supplied 15-second animation-test WAV and Milestone 5.1 discrepancy report are present at [`production/audio/milestone_5_1_animation_test_audio_15s.wav`](../production/audio/milestone_5_1_animation_test_audio_15s.wav) and [`docs/source_archive/HOLOS_Milestone_5.1_audio_discrepancy_analysis.user-supplied.md`](source_archive/HOLOS_Milestone_5.1_audio_discrepancy_analysis.user-supplied.md). The report describes an extra opening “But” and a truncated fourth turn, but its cited original file path is unavailable, so byte identity to the uploaded WAV is not established.
- [x] User-supplied Episode 1 key art is explicitly approved as the official series-wide visual style guide; the image is at [`production/character_references/episode1_key_art_reference.png`](../production/character_references/episode1_key_art_reference.png), with provenance and approval recorded in the companion manifest. Separate final-poster, editable-logo-master, title-card, and distribution/rights approval remain unspecified.
- [ ] Full production dialogue-master WAV bytes and one authoritative review-WAV variant are not present in the repository.
- [ ] Original Khaled and Kevin production rigs/scenes and dependencies are not present in the inspected repository tree.
- [x] A 25-page consolidated screenplay text extraction and a 65-shot draft body breakdown are present on PR #8; the extraction explicitly says it has not been compared verbatim with the original DOCX.
- [ ] Canonical screenplay approval, original-DOCX reconciliation, and a locked shot list with authoritative timing remain outstanding.
- [ ] Complete episode body, production camera setup, environments, and final render are not present.

## 2. Required source package

### A. Canonical story and editorial authority

- [ ] Canonical screenplay file (PDF/DOCX/FDX/ Fountain/Markdown or original format).
- [ ] Version identifier, approval date, and explicit statement that this is the production-approved version.
- [ ] Complete scene headings, action, dialogue, speaker cues, transitions, and ending.
- [ ] Approved shot list/storyboard or explicit permission to develop one from the screenplay.
- [ ] Any pronunciation, performance, timing, or dialogue-change notes.

**Acceptance:** screenplay version and approved dialogue are unambiguous. Reconcile the original DOCX against the repository's consolidated extraction, then have the project author approve the production version. The PR #8 65-shot breakdown is a draft previs aid, not a substitute for this gate or the four-turn opening audio handoff.

### B. Dialogue and audio masters

- [ ] Original full-episode dialogue master, unmodified.
- [ ] File format, sample rate, channel count, bit depth/codec, duration, and SHA-256.
- [ ] Exact edit/export command or DAW session provenance.
- [ ] Selected four-turn review WAV with full SHA-256 and extraction command.
- [ ] Confirmation whether the Manus WAV (`4b8c1d78ac6ca233f9ae2ba3f31566baaa75a83802eac8257ba7cba48cd76730`) or Codex WAV (`e9d8a3a88f310b1558a884fcec87f8cf16741019ddbcede2a2db2cc2db74194f`) is authoritative, or supply a new canonical export.
- [ ] Separate music, ambience, and effects stems if they exist; identify approved versions and rights.

The received 15-second WAV is test material, not a verified complete four-turn source or the full-episode production master. Its metadata/hash are recorded separately; the discrepancy report’s content observations have not been independently re-established against these exact bytes.

**Acceptance:** one named source audio file is selected by the project owner; its exact bytes are hashed and the timeline timebase/offset is tied to that same file. The two known review WAV variants must remain distinct until this is resolved.

### C. Khaled character production source

- [ ] Original Godot character scene and all referenced resources.
- [ ] Scripts, skeleton/bone hierarchy, skin/mesh, materials, textures, shaders.
- [ ] Animation library, facial blend shapes/visemes, mouth/jaw controls, eye controls.
- [ ] Hair, clothing, accessories, collision/IK resources and imported-source files.
- [ ] Rig control map documenting exact node paths/property names for each supported viseme.
- [ ] Known-good idle, speaking, blink, turn, and expression benchmark scenes/renders.
- [ ] Source artwork/model files and licenses where applicable.

### D. Kevin character production source

Same complete package as Khaled, independently supplied and identified. Kevin must retain his own approved appearance, proportions, materials, voice/performance and rig mapping. Do not clone Khaled's rig or reuse Khaled's appearance as a placeholder.

### E. Episode world and production project

- [ ] Complete Godot project archive or repository snapshot, including `project.godot`, addons/plugins, import settings, scripts, scenes, resources, and project-specific settings.
- [ ] Godot version and renderer target used by the approved project.
- [ ] Environments, props, backgrounds, lighting, cameras, shaders, fonts, logos and source files.
- [ ] Scene/shot naming convention and any existing episode layout.
- [ ] Dependency inventory and a known-good project-open/render instruction.
- [ ] Backup/archive plus SHA-256 manifest before any integration changes.

### F. Delivery and credits

- [ ] Approved output resolution, frame rate, aspect ratio, color/audio requirements and target container.
- [ ] Approved episode title, series title, title-card wording, credits text, and contributor spellings/roles.
- [ ] Approval of draft bookend music or delivery of final licensed/owned music stems.
- [ ] Required captions/subtitles, accessibility and distribution deliverables.

## 3. Integration sequence after intake

1. Inventory the supplied archive without modifying it; record every file, size and SHA-256.
2. Make and verify a protected backup.
3. Open the original Godot project in its specified Godot version and run its existing benchmark.
4. Confirm the canonical screenplay against the selected audio master; resolve transcript conflicts before extending alignment.
5. Rebuild and validate the timeline against the exact chosen audio bytes and measured duration.
6. Inspect each real character rig and write a rig-specific semantic-viseme map from verified controls.
7. Connect both actors and the director to one audio transport clock; test play, pause, resume, seek and stop.
8. Build the shot list from approved screenplay/storyboard material, then integrate environments and cameras.
9. Render short debug samples; review acting, timing, facial deformation, continuity and scene transitions.
10. Render the full episode, assemble approved audio/music/credits, run media metadata checks, and watch the complete export.
11. Record final source hashes, tool versions, test results, approvals and export hash.

## 4. Current hard blockers

| Blocker | Why it blocks production |
|---|---|
| Original screenplay not reconciled/locked | The 25-page extraction is chat-derived and uncertified against the original DOCX; cannot yet lock all dialogue, ending, or shot timing |
| No selected authoritative review WAV | Cannot safely bind the 0.091-second-relative timeline to one exact review file |
| No supplied production audio master bytes | Cannot perform audio-clock integration or verify runtime against the master |
| No original Khaled/Kevin rigs | Cannot map visemes to actual controls or render the approved characters |
| No full production Godot project/environment assets | Cannot build the episode body or validate original dependencies |
| No approved final credits/music/delivery specification | Cannot prepare a release-ready final assembly |

**Acceptance boundary:** repository validators and generic adapter tests prove only the files/tooling they exercise. They do not constitute character-rig acceptance, visual lip-sync acceptance, or a completed Episode 1.
