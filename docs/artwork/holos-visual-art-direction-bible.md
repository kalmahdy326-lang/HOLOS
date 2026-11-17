# HOLOS — Visual Art Direction Bible

**Project author:** Khaled AL-MAHDY  
**Project:** HOLOS animated series  
**Document status:** Production specification — working baseline  
**Purpose:** Give artists, animators, layout designers, and production agents one consistent visual standard while protecting the approved source artwork.

> **Authority rule:** The user-approved key-art file `production/character_references/episode1_key_art_reference.png` is the series-wide visual style authority. This document explains how to inspect, preserve, extend, and apply that authority. It does not replace the image or authorize redesign.

## 1. Evidence and approval labels

Every visual decision must carry one of these statuses in the asset register or review notes:

- **APPROVED SOURCE:** A creator-approved existing asset. Preserve it unchanged.
- **SOURCE-DERIVED:** A crop, layout, grade, animation, or compositing treatment made from an approved source. Record its source and settings.
- **PROVISIONAL:** A reversible proposal awaiting creator review.
- **REFERENCE ONLY:** Useful for understanding, but not approved as production artwork.
- **BLOCKED / UNKNOWN:** Required information or source material is unavailable. Do not fill the gap by inventing it.

If this document conflicts with an approved source image or a later explicit creator instruction, the approved source or later instruction wins. If two approved sources conflict, flag the conflict; do not silently choose.

## 2. Core visual identity

HOLOS is a thoughtful science-fiction animated series concerned with observation, relationships, evidence, uncertainty, and the structure of reality. Its visual language should communicate intelligence and mystery without turning the series into generic space fantasy, a technology advertisement, or a horror spectacle.

The approved key art is the primary reference for:
- Character rendering and proportions.
- Line quality and edge treatment.
- Shape language.
- Color relationships and contrast.
- Lighting logic.
- Texture, shading, and finish.
- Overall emotional register.
- The relationship between figures, typography, and negative space.

**Do not invent numeric color values from memory or from a text description.** Sample colors directly from the actual approved image. Record sampled values, color space, sampling region, and intended use in a derived palette file. A sampled palette is a technical extraction, not permission to recolor the characters.

## 3. Visual principles

### 3.1 Clarity before spectacle
A shot must communicate one primary visual idea. Avoid layering so many effects, glows, particles, grids, scanlines, lens flares, and HUD elements that the subject or title becomes hard to read.

### 3.2 Controlled mystery
Use framing, pacing, negative space, and selective information to create curiosity. Do not add unexplained symbols, alien glyphs, fictional equations, or ominous imagery as decoration.

### 3.3 Scientific restraint
Interfaces and scientific displays must look purposeful. Any displayed value, graph, waveform, equation, station label, or measurement must come from approved story/technical material or be explicitly marked as non-diegetic design placeholder during internal layout tests. Never fabricate a measurement and present it as story fact.

### 3.4 Character readability
Characters must remain recognizable across close, medium, and wide framing. Preserve their approved facial structure, hair, clothing, body proportions, silhouette, and expression vocabulary. Do not mirror, stretch, reshape, or re-proportion a character to solve a layout problem.

### 3.5 Restraint in motion
Motion should reveal the composition, not distract from it. Prefer subtle camera drift, slow parallax, gentle light changes, and clean transitions when those can be derived from existing art. Avoid unapproved facial animation, lip-sync, body movement, or implied character actions.

### 3.6 Continuity
The same character, room, station, device, and graphic element must remain visually consistent across shots unless a documented story event changes it. Track changes in a continuity log.

## 4. Color and lighting workflow

1. Resolve the original key-art bytes and verify the recorded SHA-256.
2. Open the image without destructive edits.
3. Record image dimensions, embedded profile, and color space.
4. Sample representative colors from background, dominant forms, highlights, shadows, and typography only where those regions are clearly present.
5. Create a palette proposal with swatches and hex/RGB values, each tagged SOURCE-SAMPLED.
6. Do not use the palette to recolor character skin, hair, eyes, or clothing unless the approved art itself establishes that treatment.
7. For every new scene, record key-light direction, fill level, rim-light use, background luminance, and contrast against the approved reference.
8. Compare final frames against the source image at normal viewing size and at thumbnail size.

No exact palette, light temperature, or lighting direction is declared by this document; those must be measured from the approved image.

## 5. Composition and camera

- Maintain a clear focal hierarchy: subject first, title or story information second, atmosphere third.
- Protect negative space around faces and important silhouettes.
- Avoid placing text across faces, eyes, hands, or story-critical objects.
- Use intentional headroom and look room; do not crop at joints or through important props accidentally.
- Use slow, stable moves for scientific observation and title sequences.
- Use faster movement only when supported by the screenplay and shot intent.
- Camera movement must not imply a character action that is absent from the source.
- Record framing, lens/camera approximation, start/end position, duration, and easing for each animated move.

## 6. Typography and graphic design

The approved key art and existing title/bookend prototypes are the typography authorities until a separate logo/font master is confirmed.

- Use the exact title spelling: **HOLOS**.
- Episode 1 title: **The Moon Has Anger Issues**.
- Do not add a series subtitle, tagline, slogan, or explanatory phrase without creator approval.
- Do not recreate the logo by typing a similar font if the approved lettering is available as artwork.
- If the title exists only as part of a raster image, preserve it or create a carefully documented derived treatment; do not claim it is an editable logo master.
- Do not invent a typeface name. Identify fonts from project files and record exact family, weight, version, license/source, and fallback.
- Keep text within title-safe and action-safe areas appropriate to the 16:9 delivery frame.
- Check readability on a phone-sized display as well as a desktop monitor.
- Use restrained hierarchy and avoid unnecessary labels or decorative microtext.

## 7. Backgrounds, environments, and props

Existing approved environment and prop art takes precedence. A location mentioned in a story summary is not by itself an approved visual design.

For every new environment or prop, require:
- A screenplay or production reference.
- A design brief describing function and story relevance.
- A scale reference.
- A front/side/three-quarter or other needed views.
- Material and surface notes grounded in existing visual direction.
- Lighting and palette relationship to the approved key art.
- Approval status and source provenance.

The Episode 1 setting is a heavily shielded lunar research station in Mare Umbrae. This is story context, not permission to invent a detailed station exterior, lunar landscape, control room, equipment, insignia, or architecture without source/approval. The Moon is an unidentified speaking presence; no humanoid Moon design is established.

## 8. Effects and compositing

Effects are allowed only when they preserve the source identity and remain technically reversible.

Potential source-derived treatments:
- Layer separation and restrained parallax, if the source supports it.
- Slow camera push/pull.
- Subtle exposure or illumination shift.
- Soft transition masks.
- Controlled fades and dissolves.
- Depth-of-field simulation only when it does not obscure important source details.

Do not:
- Generate replacement or missing visual content.
- Paint over faces or redesign character features.
- Add fake film damage, heavy chromatic aberration, excessive bloom, or noisy overlays that degrade the approved art.
- Add HUDs, symbols, equations, or data readouts without a documented story/design purpose.
- Use AI image-generation services or paid assets without explicit authorization.

## 9. Character art rules

Character model sheets and approved reference images govern character appearance. Text descriptions are secondary metadata only.

Known reference metadata recorded in project history:
- **Khaled — Character B:** source-archive description lists age 38, height 6'1", brown hair, blue eyes.
- **Kevin — Character A:** source-archive description lists age 23, height 6'0", red hair, blue eyes.

These are metadata notes, not substitutes for the reference sheets. Do not infer facial shape, ethnicity, skin tone, body type, clothing, accessories, or other appearance details from names or metadata. Inspect the actual reference images.

Specific continuity constraints:
- Khaled is Character B.
- Kevin is Character A.
- Two portraits labelled “Surprised” under Kevin were previously identified by the creator as Khaled; preserve this correction in manifests and derived sheets.
- Do not use unverified rigs or substitute rigs.
- Do not treat the theme singer/narrator as a character.
- Do not assign the separate “God” voice/reference to a character without creator confirmation.
- ORBIT and the Moon are distinct entities.
- The Moon has no approved humanoid appearance.

## 10. Output and review standards

For every artwork deliverable, include:
- Asset ID and title.
- Status label.
- Original source path and Git ref/commit.
- Original checksum and derived checksum.
- Dimensions, format, color profile, and transparency status.
- Software/tool version and processing settings.
- Artist/agent and creation date.
- Intended use and excluded uses.
- Review notes and outstanding approvals.

Review at:
1. Full resolution.
2. Actual delivery size.
3. Thumbnail size.
4. Dark and light surrounding UI where relevant.
5. Motion playback, not only still frames.

## 11. Prohibited shortcuts

- No invented or AI-generated character likenesses.
- No unapproved redesigns.
- No replacing a missing approved asset with a convenient approximation.
- No silent changes to source artwork.
- No false claims that a draft is approved or final.
- No unapproved credits, logos, typography, symbols, or story details.
- No changes to the canonical Series Bible, screenplay, or storyboard under the guise of art cleanup.

## 12. Approval checklist

Before an artwork is promoted to APPROVED SOURCE:
- [ ] Creator has reviewed the actual image or rendered sequence.
- [ ] Source provenance is recorded.
- [ ] No unapproved design elements are present.
- [ ] Character identity and continuity are correct.
- [ ] Text is exact and approved.
- [ ] Technical specifications are recorded.
- [ ] Original files remain unchanged.
- [ ] Any remaining uncertainty is explicitly listed.

**Guiding rule:** extend the visual language that already exists; do not pretend an unmade design was always part of HOLOS.
