# HOLOS Animation and Render Acceptance Standard

This document defines how production quality is judged. Passing a technical render test does not mean a shot is artistically accepted.

## 1. Creative quality acceptance

Every final shot must be reviewed for:

### Character design and continuity
- Correct approved character design, proportions, colors, costume, props, and silhouette.
- No model drift between shots or camera angles.
- Consistent deformation and anatomy.
- Character identity and acting remain readable at intended viewing size.

### Animation and performance
- Clear poses, readable silhouettes, intentional timing, and convincing weight.
- Smooth, controlled transitions without unintended pops, jitter, sliding, or deformation.
- Expressive body language, facial animation, gaze, blinking, and reactions.
- Believable contact, interaction, anticipation, follow-through, and secondary motion where appropriate.
- Speaking and listening performances are both animated; non-speaking characters do not become lifeless.
- Lip-sync matches the approved recording and remains visually convincing at normal playback speed.

### Staging and cinematography
- Clear composition and focal hierarchy.
- Consistent screen direction, eyelines, geography, entrances, exits, and spatial continuity.
- Camera motion is intentional, motivated, and free of unwanted shake or clipping.
- Lighting supports readability, mood, and continuity.
- Environments and props are coherent and do not distract through errors or missing detail.

### Finish and sound
- Clean compositing, edges, shadows, effects, and transitions.
- No unintended placeholders, debug overlays, missing textures, or test assets.
- Dialogue is intelligible and synchronized.
- Sound effects and ambience support the scene.
- Music is included only when explicitly approved and correctly licensed/provenanced.

## 2. Technical render acceptance

The currently documented starter target is 1280×720 at 24 fps, H.264/libx264 MP4 with yuv420p. Confirm against the approved delivery specification before final mastering.

For each render, record and validate:
- File existence, byte size, and SHA-256.
- Container and video codec.
- Pixel format.
- Width and height.
- Frame rate and decoded frame count.
- Duration and expected frame count for the intended timeline.
- Full-file decode without errors.
- Audio stream presence or absence as intended.
- Audio codec, sample rate, channel layout, duration, and start offset where applicable.
- Audio/video synchronization.
- No black, frozen, corrupted, duplicated, or missing frames unless deliberately authored.
- Playback inspection at normal speed and frame-level inspection of representative critical moments.

Automated checks must be reproducible and their logs retained. FFprobe metadata alone is not proof that the entire file decodes or looks correct.

## 3. Per-shot review record

Each final shot should have:
- Shot ID and source panel ID.
- Scene and episode.
- Exact source screenplay/storyboard references.
- Character and asset versions.
- Animation/rig version.
- Audio and dialogue source IDs, if applicable.
- Render settings and engine revision.
- Output path, size, and SHA-256.
- Automated QC report.
- Visual review notes.
- Reviewer and decision.
- Open defects and retest evidence.

## 4. Review outcomes

Use only:
- **PASS** — all required criteria met.
- **FAIL** — one or more criteria failed; correction required.
- **HOLD** — missing source, approval, or prerequisite prevents a fair review.
- **NOT TESTED** — no acceptance test has been performed.

A shot cannot be called final because it rendered successfully. A complete episode cannot be called accepted until all required shots, editorial, audio, technical checks, and project-author review pass.

## 5. Quality policy

Do not trade away character acting, visual consistency, or storytelling clarity to increase shot count. Do not hide gaps with still images, generic rigs, unapproved generated artwork, or placeholder animation. If the quality standard cannot yet be met, identify the missing asset, tool, skill, or implementation and create a concrete task to close that gap.
