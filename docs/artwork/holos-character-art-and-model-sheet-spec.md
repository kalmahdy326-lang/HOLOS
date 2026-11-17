# HOLOS — Character Artwork & Model Sheet Specification

**Project author:** Khaled AL-MAHDY  
**Status:** Production specification; not a character redesign  
**Applies to:** Khaled, Kevin, ORBIT visual interface where applicable, and any future approved character/entity designs.

## 1. Purpose and authority

This document defines how character artwork is to be inspected, documented, prepared, and validated. It does not authorize new designs.

The actual approved character-reference images are the visual authority. Text metadata in the repository, scripts, filenames, and old prompts must never override the images or a later explicit creator correction.

Before drawing, rigging, or animating:
1. Locate the original reference files.
2. Resolve Git LFS to actual image bytes.
3. Record SHA-256, dimensions, color profile, and source ref.
4. Inspect every sheet at full resolution.
5. Record all visible views, expressions, clothing, accessories, proportions, and labels.
6. Reconcile labels against creator corrections.
7. Produce a discrepancy report before changing any source-derived reference.

## 2. Character identity ledger

| Character | Canonical identifier | Established role | Notes |
|---|---|---|---|
| Khaled | Character B | Senior relational physicist/researcher | Analytical and controlled; visual authority is the approved Khaled reference |
| Kevin | Character A | Junior systems investigator | Impulsive and experiment-prone; visual authority is the approved Kevin reference |
| ORBIT | Station AI/system voice | Protocol-driven and literal | Distinct from the Moon; no human character design should be inferred |
| The Moon | Unidentified speaking presence | Communicates through station infrastructure | No established humanoid design; do not invent one |

Khaled and Kevin are not interchangeable. Preserve the A/B mapping in filenames, metadata, rig IDs, scene labels, and production notes.

## 3. Existing metadata — not a substitute for art

Project history records the following source-archive descriptions:
- Khaled: age 38, height 6'1", brown hair, blue eyes.
- Kevin: age 23, height 6'0", red hair, blue eyes.

Treat these as secondary metadata pending comparison with the actual source sheets. They do not establish skin tone, ethnicity, facial structure, body type, clothing, accessories, voice, or other unrecorded traits.

Creator correction already recorded:
- Two portraits labelled “Surprised” beneath Kevin were identified by the creator as Khaled. Keep this correction in the reference manifest and do not repeat the misattribution.

## 4. Required model-sheet views

Only create views that are needed and supported by the existing approved reference. If the source does not establish a feature, mark it UNKNOWN rather than designing it silently.

For each character, the desired model-sheet package is:

### A. Identity / hero reference
- One approved neutral or canonical view.
- Character name and identifier.
- Source image filename and checksum.
- Version and approval status.
- Notes on any visible design details that must not drift.

### B. Turnaround
Where original views exist or the creator approves additional drawing:
- Front.
- Three-quarter front.
- Side profile.
- Three-quarter rear.
- Rear.

All views must preserve the same head/body proportions, hair mass, clothing construction, accessories, and silhouette. Do not invent unseen rear details and then present them as established canon.

### C. Expression sheet
Use only expressions already shown in the source sheet or explicitly approved by the creator. Each expression needs:
- Exact label.
- Character identity.
- Source crop or source reference.
- Eyebrow, eye, mouth, and head-pose notes only where visible.
- Whether the expression is approved for animation.

Do not treat an expression label as proof that the image belongs to the character named by the sheet section; verify image identity.

### D. Mouth shapes / phoneme set
Only prepare after the source design and animation pipeline are confirmed. Record:
- Phoneme/viseme label.
- Jaw opening.
- Lip shape.
- Teeth/tongue visibility.
- Neutral/rest position.
- Timing assumptions.
- Whether the shape is drawn, rigged, or generated from existing source artwork.

No mouth shape may change the character's identity. Do not infer phoneme drawings from a low-resolution crop.

### E. Hands, props, costume details
Document only details visible in approved source art or screenplay-confirmed prop requirements. Include scale and handedness only when known. Unspecified details remain UNKNOWN.

## 5. Proportion and construction controls

For a future rig/model sheet, measure against the original reference:
- Total character height in head units.
- Head width/height.
- Shoulder width.
- Torso-to-leg ratio.
- Arm and hand proportions.
- Eye spacing and eye-line.
- Hair silhouette.
- Clothing silhouette and seam placement.

Measurements must be extracted from the actual image and include the method and image dimensions. Do not invent values from memory.

Any source-derived pose or crop must be checked against the unmodified reference at 100% scale. Avoid:
- Horizontal flipping if it changes asymmetrical details.
- Non-uniform scaling.
- Face reshaping.
- Hairline changes.
- Eye-color changes.
- Clothing redesign.
- Accessory additions or removals.
- Unapproved age or body-shape changes.

## 6. Color and material notes

Extract colors from the approved reference image, not from verbal descriptions. For each sampled color, record:
- Hex and RGB values.
- Color profile / color space.
- Sampling location and sample size.
- Whether it represents a flat region, shadow, highlight, or antialiased edge.
- Intended use.

Do not use a single sampled pixel from an antialiased edge as a canonical character color. Use representative interior regions and compare the resulting swatch sheet against the original.

## 7. Animation readiness and rig acceptance

A model sheet is not a rig. A rig is not an approved performance.

Before rigging:
- Verify the complete source reference set.
- Confirm the character's canonical identifier.
- Identify separate body, face, hair, clothing, and accessory layers only where present or approved.
- Record all manual separations and any reconstructed hidden pixels.
- Obtain creator approval for reconstructed areas.
- Keep the original reference untouched.

A rig is accepted only after:
- Neutral pose matches the reference.
- Front/three-quarter/side views do not drift.
- Facial expressions preserve identity.
- Limbs deform without obvious tearing or proportion shifts.
- Clothing and hair behave consistently.
- No substitute or placeholder assets remain in the production rig.
- A reproducible benchmark scene and comparison images are delivered.

**Current gate:** The original Khaled and Kevin rigs remain unverified under the 12 November reconciliation. Do not claim rig completion or use substitute rigs.

## 8. File naming and metadata

Recommended derived filenames:
- `khaled_characterB_model-sheet_v001.png`
- `kevin_characterA_model-sheet_v001.png`
- `khaled_characterB_expression-index_v001.csv`
- `kevin_characterA_expression-index_v001.csv`
- `character_reference_manifest_v001.json`

These are naming proposals, not claims that these files already exist. Preserve original filenames for source assets.

Each manifest record should include:
`asset_id`, `character_id`, `source_path`, `source_ref`, `source_sha256`, `derived_path`, `derived_sha256`, `dimensions`, `view`, `expression`, `status`, `creator_correction`, `notes`.

## 9. Character-specific prohibitions

### Khaled
- Always Character B.
- Use only verified Khaled reference imagery.
- Preserve the creator correction for the two misfiled “Surprised” portraits.
- Do not infer or invent appearance details not shown in the reference.

### Kevin
- Always Character A.
- Use only verified Kevin reference imagery.
- Do not absorb Khaled's misfiled portraits into Kevin's sheet.

### ORBIT
- ORBIT is the station AI/system voice, not the Moon.
- A visual interface design requires existing approved UI assets or a separate creator-approved design brief.
- Do not invent a humanoid avatar or treat ORBIT as a physical character without approval.

### The Moon
- The Moon is an unidentified speaking presence communicated through station infrastructure.
- No humanoid design is established.
- Do not draw a face, body, alien, deity, creature, or personification as if canonical.

## 10. Review and approval checklist

- [ ] Correct A/B identity mapping.
- [ ] Original image bytes and checksum verified.
- [ ] Creator corrections reflected.
- [ ] No invented features or hidden-side details.
- [ ] Proportions checked against source.
- [ ] Expression labels and identity verified.
- [ ] Color sampling documented.
- [ ] Source and derivative kept separate.
- [ ] Rig status accurately reported.
- [ ] Creator approval recorded before canonical use.
