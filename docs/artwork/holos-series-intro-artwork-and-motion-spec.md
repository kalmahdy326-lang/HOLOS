# HOLOS — Series Introduction Artwork & Motion Specification

**Project author:** Khaled AL-MAHDY  
**Deliverable target:** `HOLOS_Intro_Review_v001.mp4`  
**Status:** Review-production specification; silent visual version unless audio is separately approved.

## 1. Creative objective

Create a distinctive, reusable opening identity for the HOLOS animated series. The sequence should feel like a thoughtful science-fiction series: precise, atmospheric, curious, and visually controlled.

This is a series opening, not an Episode 1 recap, not a trailer, and not a generic logo animation. The first review should demonstrate the visual identity, title treatment, motion quality, and transition into an episode.

The approved key-art image is the primary visual source. Existing title/credits bookend infrastructure may be reused after inspection. Do not invent new artwork to fill gaps.

## 2. Approved content

Required series title:
**HOLOS**

Episode 1 title, if the opening is explicitly Episode 1-specific:
**The Moon Has Anger Issues**

Creator credit:
**Created by Khaled AL-MAHDY** may be used only if the existing approved title/credits design already supports this credit.

Do not add:
- A series subtitle or tagline.
- Additional cast or crew names.
- Studio or production-company marks.
- Rights or copyright lines.
- Unapproved episode summaries.
- Fictional scientific values or equations.
- A humanoid Moon or invented character designs.

The opening must remain reusable. If the episode title is included, keep the series title treatment separable from the episode-specific card/config.

## 3. Source and asset requirements

Before building:
1. Verify the approved key-art bytes and checksum.
2. Inspect the original image at full resolution.
3. Inspect existing Alternative B title-card v3 and credits-card v3 prototypes.
4. Locate and inspect their editable Godot scenes, scripts, fonts, configs, and render settings.
5. Compare existing title typography with the approved key art.
6. Record all source Git refs, paths, file sizes, and SHA-256 hashes.
7. Work only in a new derived project/output folder.

Do not confuse:
- Approved key art with a separate editable logo master.
- Existing bookend prototypes with a completed series intro.
- A test scene with a production scene.
- A static frame with an animated sequence.
- A locally synthesized music draft with approved final music.

## 4. Visual sequence — suggested shot architecture

The following is a **provisional layout plan**, not an already approved storyboard. Timing can be adjusted after actual playback. Keep it compact and purposeful; avoid padding the sequence to hit a duration.

### Shot 01 — Quiet arrival
- Begin from black or a restrained fade.
- Allow the first visible detail of the approved key art to emerge.
- Do not add a new starfield, Moon surface, station exterior, or environment.
- Motion: very subtle exposure/fade or source-derived camera move.
- Purpose: establish attention and atmosphere.

### Shot 02 — Reveal the artwork
- Reveal the full approved key art through a controlled crop or camera pullback.
- Preserve aspect ratio and all important character/title details.
- If using parallax, separate only regions that can be isolated without fabricating missing pixels.
- Do not invent depth behind occluded elements.
- Purpose: let the viewer recognize the actual approved series image.

### Shot 03 — Title emphasis
- Present **HOLOS** with strong legibility.
- Prefer the existing approved title treatment where available.
- If title lettering is embedded in the image, do not approximate it with a substitute font.
- Use clean spacing and safe margins.
- Purpose: make the series name unmistakable.

### Shot 04 — Hold / visual punctuation
- Hold the composed artwork long enough to read.
- A very subtle light or camera movement may continue if it does not alter character appearance.
- Avoid decorative HUD overlays, equations, fake interface readouts, or unrelated particles.
- Purpose: give the title visual weight.

### Shot 05 — Episode identification (optional)
- If using an Episode 1-specific opening, introduce **The Moon Has Anger Issues** as a separate, readable line/card.
- Keep the series title and episode title hierarchy clear.
- Do not add an explanatory subtitle.
- Purpose: identify the first episode without changing the series identity.

### Shot 06 — Exit / handoff
- End on a clean frame or fade that can transition into the first episode shot.
- Do not invent a station shot or story image to make the handoff more dramatic.
- Ensure the final frame is not clipped, overexposed, or text-incomplete.
- Purpose: provide a reusable transition point.

## 5. Motion design

Use restrained, intentional movement:
- Slow push-in or pull-back.
- Small source-derived pan.
- Gentle opacity transitions.
- Subtle, source-consistent illumination changes.
- Smooth easing with no sudden unintended jumps.
- A deliberate final hold.

Avoid:
- Fast zooms that distort faces.
- Rotations that make the artwork feel like a 3D card unless approved.
- Artificial mouth, eye, hair, or body animation.
- Parallax that exposes blank or fabricated regions.
- Excessive bloom, lens flare, chromatic aberration, glitch effects, shake, particles, or scanlines.
- Text movement that reduces readability.

For each shot, record start/end frame, duration, easing curve, source crop, camera transform, opacity, and transition overlap. Keep timing deterministic and reproducible.

## 6. Composition and typography checks

- Protect all important faces and silhouettes.
- Preserve the original title lettering and proportions.
- Keep all added text inside title-safe margins.
- Check that the title reads at phone size.
- Avoid placing the episode title over faces or other critical content.
- Use the existing project font only after confirming its identity and license/source.
- Do not claim an editable vector logo exists unless one is actually located.

## 7. Technical baseline

Review target:
- 1280 × 720.
- 24 frames per second.
- H.264 / libx264.
- yuv420p.
- MP4.
- Silent audio track policy: no audio stream unless a separately approved review soundtrack is explicitly authorized.

Render actual frames through the existing HOLOS Godot pipeline. Assemble with the existing FFmpeg workflow. Use FFprobe to verify:
- File exists and is non-zero.
- Duration and frame count match the render manifest.
- Resolution is 1280 × 720.
- Frame rate is 24 fps.
- Video codec is H.264.
- Pixel format is yuv420p.
- Audio stream is absent for the silent review.
- No truncated or duplicated final frames.

Inspect the first frame, each shot boundary, midpoint, and final frame. Also watch the entire exported MP4.

## 8. Soundtrack separation

For this review:
- Keep the 209-second user-supplied theme recording untouched.
- Keep the unapproved 12-second WAV untouched.
- Exclude both from the MP4.
- Do not add dialogue, test audio, temporary music, or synthesized replacement music.

Audio approval is a separate decision after the silent visual review. Record the two sources in the manifest as NOT USED / NOT APPROVED FOR THIS PREVIEW.

## 9. Editable project and handoff

Deliver:
- `HOLOS_Intro_Review_v001.mp4`
- Editable Godot project and intro scene.
- Intro-specific configuration.
- All derived artwork layers/crops with provenance.
- Rendered PNG frames.
- Source and derived asset manifests.
- SHA-256 checksums.
- Git refs and tool versions.
- Render and FFmpeg commands.
- FFprobe JSON report.
- Visual inspection report.
- Known limitations and decisions requiring creator approval.

The project must reopen and reproduce the render without relying on undocumented local paths.

## 10. Quality bar

The intro is ready for creator review when:
- The series identity is immediately recognizable.
- The approved key art remains visually faithful.
- The title is readable and correctly spelled.
- Motion feels deliberate and polished.
- No visual elements have been invented or misattributed.
- The opening and ending feel intentional.
- The video plays from beginning to end.
- The editable source and provenance are included.
- It is honestly labelled a silent review prototype, not a final master.

If the source image cannot support the proposed movement, simplify the movement. A restrained, clean composition is preferable to fake depth or invented artwork.
