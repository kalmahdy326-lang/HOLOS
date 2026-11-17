# HOLOS — Intro Sequence Build Brief

**Project author:** Khaled AL-MAHDY  
**Project:** HOLOS animated series  
**Scope:** Build the first real, reusable HOLOS series/episode opening sequence as a production prototype.  
**Priority:** Start here while the wider Episode 1 source-access gate remains blocked.

---

## 1. The assignment

Stop at a small, finished production unit rather than attempting the entire episode immediately.

Build a **watchable HOLOS intro sequence** using the real, already-recorded project assets and the existing local production pipeline wherever possible. Treat this as the first reusable episode component: a title/opening sequence that can later be called by Episode 1 and reused consistently in subsequent episodes.

This is a limited, GitHub-source-only task. It does **not** authorize or imply access to the blocked Project-space Library items. Do not wait for Library access if the required GitHub-branch assets and existing intro/bookend tooling are genuinely accessible. If a needed binary is only an LFS pointer and its real bytes cannot be retrieved, report that blocker and do not fake the asset.

**First objective:** produce a short intro preview that can actually be played and reviewed. Do not return only a plan or a report.

## 2. Keep the wider source-access gate separate

The full Episode 1 recovery/assembly gate remains blocked pending access to the original screenplay DOCX, three Library character-reference PNGs, and two Library ZIP packages.

This intro task may proceed only with assets already accessible in the GitHub repository and its relevant open PR branches, especially PR #9's docs/holos-series-bible branch and the production tooling recorded by the project.

Do not claim that the full source package, original character rigs, complete episode dialogue, or canonical screenplay have been recovered. Do not use this intro task to bypass the screenplay or rig acceptance gates.

## 3. Inspect and preserve the existing intro/bookend work first

The Episode 1 production asset-intake record says reusable title/credits bookend scene and generic renderer infrastructure exist.

The Milestone 6 local production-engine record also describes:

- tools/compose_episode_music_bed.py
- Locally synthesized HOLOS theme drafts: 12 seconds for the intro and 24 seconds for the credits outro.
- A workflow that composes separate opening and closing music into a duration-exact music bed.
- Existing Godot/Python/FFmpeg tooling for deterministic frame rendering and media assembly.

Before writing anything:

1. Inspect the current branch and PR dependencies.
2. Locate the actual reusable title/credits scene, its scripts, resources, fonts, renderer configuration, intro music draft, composer script, and any existing preview outputs.
3. Read the complete scripts and configuration before invoking them.
4. Record exact source paths, Git refs/commit SHAs, file sizes and SHA-256 values.
5. Determine which items are real files, Git LFS pointers, generated drafts, or documentation-only references.
6. Run the existing tooling as designed before modifying it.
7. Preserve all source files. Work in a separate output directory and use derived copies only.

Do not invent a path because a document mentions a feature. If the referenced title/credits scene or 12-second intro audio file cannot be located and read as actual bytes, report that fact and use only what is truly available.

## 4. Visual direction and title treatment

The user-approved key-art image is the official **series-wide visual style guide**:

production/character_references/episode1_key_art_reference.png

Its manifest records SHA-256:

ea065d17db8e3e16bb6dc07615641865ce8508e1b94cc7ecb4bc6c05daf31ab8

The key art is stored through Git LFS in the PR #9 branch. Resolve and inspect the actual image bytes; do not treat an LFS pointer as an image.

Use the approved key art as the visual foundation for the intro if the actual image is available. Preserve the original unchanged. All motion or layout changes must be made in a derived scene/project.

The visual result should feel like the opening of a thoughtful science-fiction animated series, not a generic corporate logo bumper:

- Deliberate, restrained pacing.
- Strong composition and readable title typography.
- A sense of scale, observation, structure, and the Moon/station setting only to the extent supported by the approved image and existing art.
- Subtle camera movement, parallax, light or depth treatment only if it can be achieved from existing approved material without inventing new character/environment art.
- Consistent with the approved key-art style.
- Clean transitions and a deliberate ending frame that can lead into an episode.

Do not generate or commission new imagery. Do not draw substitute characters, Moon imagery, station environments, props, logos, or backgrounds. Do not use paid software, external AI services, or AI-generation credits.

### Title wording

Use **HOLOS** as the series title.

The Episode 1 title is **The Moon Has Anger Issues**. It may appear on the Episode 1-specific opening card if the existing approved title/bookend scene supports it.

Do not silently add a subtitle such as “The Fundamental Structure of Reality” to the series logo/title card. The screenplay provenance record lists the full series-title wording as an editorial question, not a settled approval.

Use the creator credit **Created by Khaled AL-MAHDY** only if a creator credit is part of the existing title-card/credits design. Do not invent additional cast, crew, studio, copyright, music, or rights credits. Keep any unconfirmed credits out of the rendered sequence and list them as awaiting author confirmation.

## 5. Audio policy

There are two distinct kinds of theme material in the records. Do not confuse them.

### A. User-supplied theme-song M4A

production/audio/holos_theme_song_source.m4a

Recorded metadata:

- SHA-256: aee4733881850f4a3a83be5ae6b69c94cdbbbebc4467916ad3aeec5b3e3bd09e
- Size: 1,307,950 bytes
- AAC, 48 kHz, stereo, 209 seconds

This is the user-supplied theme-song source. The manifest does not establish approval of lyrics, rights/credits, final mix, loudness, or placement. Do not assume the 209-second source is the approved 12-second intro edit.

### B. Existing locally synthesized 12-second intro draft

The Milestone 6 record describes a locally synthesized 12-second intro theme draft and a 24-second credits outro draft, used by the bookend composer.

Locate the actual draft files and inspect their metadata and hashes. These are **draft music**, not final mastered or rights-cleared audio. They may be used in a clearly labelled internal review preview if their bytes are accessible and the existing project record supports that use. Do not represent them as final approved music.

If the 12-second draft is not actually available, do not cut an arbitrary 12 seconds from the 209-second M4A and present it as the approved intro. Build a silent visual preview instead and report the missing music source.

Keep all original audio unchanged. Any gain, fade, trim, mix, or conversion must be a separately named derived file with its own hash and a record of the exact command/settings.

## 6. Technical implementation

Use the existing HOLOS production architecture:

- Godot for scene composition, frame stepping, and PNG capture.
- Python for config validation, asset resolution, scheduling, rendering orchestration, manifests and reports.
- FFmpeg/FFprobe for encoding and media validation.
- Existing title/credits bookend scene and composer where verified.

Do not create a parallel renderer or bypass the existing production architecture merely to get a quick result.

The current starter review profile is 1280×720 at 24 fps, H.264/libx264, yuv420p, MP4. Use this for the intro preview unless the existing bookend tool has a more specific validated preview profile. This is a review output, not a final locked series delivery profile.

### Required implementation steps

1. Run the existing title/credits scene in isolation and capture a baseline before edits.
2. Inspect title placement, typography, safe margins, image crop, background, animation hooks, and transition behaviour.
3. Make a separate intro-specific scene/configuration using the reusable bookend infrastructure.
4. Use the approved key art as the only visual source image unless other already-approved GitHub art is explicitly documented.
5. Build a short opening with readable title treatment and restrained motion.
6. If the actual 12-second intro draft is available, create a separate review mix using the existing composer or documented audio pipeline.
7. If no approved/available music draft exists, make the visual intro silent. Do not substitute the test WAV or dialogue audio.
8. Render actual frames using the existing Godot renderer in a rendering-capable environment.
9. Assemble the MP4 with FFmpeg.
10. Run FFprobe and visually inspect the exported video from beginning to end.
11. Confirm the output can be opened and played.
12. Save all project files, scripts, configuration, rendered frames, output video, logs and manifests in a new output folder.

Do not use the generic adapter test scene as the finished intro. It is a test fixture, not the title/credits scene.

## 7. No character animation is required for this first intro

The original Khaled and Kevin rigs remain unverified under the 12 November reconciliation. This task does not authorize substitute rigs.

Do not create animated character stand-ins, silhouette doubles, AI portraits, puppet rigs, or false representations of Khaled or Kevin. If the intro design depends on character animation, defer that part and produce the strongest title/key-art-based opening the verified material supports.

The first intro should establish the series identity and atmosphere. It does not need to pretend the episode body is already animated.

## 8. Suggested output package

Create a new output folder without modifying source assets:

~~~text
HOLOS_INTRO_BUILD/
  00_SOURCE_INVENTORY/
    source_inventory.csv
    sha256_manifest.txt
    git_refs_and_versions.md
  01_BASELINE/
    baseline_scene_render/
    baseline_notes.md
  02_EDITABLE_PROJECT/
    godot_intro_project_or_scene/
    intro_config.json
    scripts/
    assets/
  03_AUDIO/
    source_audio_manifest.csv
    derived_intro_mix/
    mix_commands_and_settings.md
  04_RENDER/
    frames/
    render_manifest.json
  05_DELIVERY/
    HOLOS_Intro_Review_v001.mp4
    ffprobe_report.json
    visual_review.md
  06_REPORTS/
    build_log.md
    blockers_and_author_decisions.md
~~~

The editable project must include everything needed to reopen and render the intro from the verified source assets, subject to clearly documented dependencies.

## 9. Acceptance criteria

Call this a successful **intro prototype** only if all applicable conditions are met:

- The actual reusable bookend/title scene was located and inspected, or the report clearly explains why it could not be reused.
- The approved key art's actual bytes were resolved and inspected if used.
- No original source file was overwritten or altered.
- The title and all on-screen wording are supported by approved project records.
- The intro is rendered through the existing Godot/HOLOS pipeline, not represented by a mockup or static screenshot.
- The exported MP4 was probed and watched.
- Audio is either an identified, separately hashed 12-second draft explicitly labelled unapproved, or absent.
- The editable scene/config and all derived assets are included.
- The output is clearly labelled as a review prototype, not a final series master.
- Missing dependencies and author decisions are listed honestly.

If the title scene or key art cannot be retrieved, do not fabricate a substitute. Deliver a precise blocker report and, if possible, a simple typography-only layout preview using the exact title wording and existing fonts—clearly labelled as a layout test, not the finished intro.

## 10. Do not do these things

- Do not wait for or pretend to have Project-space Library access.
- Do not claim full Episode 1 recovery has started.
- Do not change the Series Bible, screenplay, storyboard, canonical episode JSON, audio manifests, source assets, or production engine.
- Do not generate new artwork or use AI-generation credits.
- Do not create substitute character rigs or animate fictional versions of Khaled/Kevin.
- Do not claim the 209-second M4A is an approved intro master.
- Do not use the 15-second animation-test WAV as intro music or dialogue.
- Do not invent credits, taglines, subtitles, or story material.
- Do not commit, push, merge, or modify GitHub from the Manus build task. Return the output package for review.

## 11. Final handoff

Return:

1. A playable HOLOS_Intro_Review_v001.mp4, or an exact explanation of the source/tool blocker preventing it.
2. The complete editable Godot intro project/scene and configuration.
3. The source inventory and SHA-256 manifest.
4. The exact source Git refs and tool versions.
5. The FFprobe report and visual-inspection report.
6. The exact audio source used, or confirmation that the preview is silent.
7. A short list of decisions still requiring Khaled's approval.

**Priority:** make the first real HOLOS opening sequence. Keep it small, honest, reusable, and renderable. Then use the same proven workflow as the foundation for the episode itself.
