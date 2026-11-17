# HOLOS — Artwork Asset Provenance & Review Workflow

**Project author:** Khaled AL-MAHDY  
**Purpose:** Ensure every image, model sheet, crop, graphic, and rendered frame can be traced to an actual source and an explicit approval state.

## 1. Asset lifecycle

Use this sequence for all artwork:

1. **DISCOVERED** — file or reference located; content not yet verified.
2. **RETRIEVED** — actual bytes obtained.
3. **INSPECTED** — image opened and reviewed; metadata recorded.
4. **SOURCE-VERIFIED** — provenance and checksum match the recorded source.
5. **DERIVED** — a non-destructive derivative created.
6. **INTERNAL REVIEW** — checked by production for technical and continuity errors.
7. **CREATOR REVIEW** — presented to Khaled.
8. **APPROVED** — explicit creator approval recorded.
9. **SUPERSEDED** — replaced by a later approved version; retain history.
10. **REJECTED / BLOCKED** — not approved or cannot be completed with available evidence.

Do not skip a state. A file existing in a repository does not make it approved.

## 2. Source authority hierarchy

When resolving an artwork question, use this order:
1. Latest explicit creator instruction.
2. Creator-approved original artwork/reference sheet.
3. Canonical Series Bible or screenplay for story facts.
4. Approved production specs and manifests.
5. Existing prototypes and derived artwork.
6. Unapproved drafts, old prompts, filenames, or agent assumptions.

If two high-authority sources disagree, record the conflict and ask for author resolution. Do not silently reconcile it.

## 3. Required manifest fields

Every asset should have a manifest record with at least:

| Field | Meaning |
|---|---|
| asset_id | Stable unique identifier |
| title | Human-readable name |
| asset_type | Key art, character sheet, expression, prop, environment, logo, title card, frame, etc. |
| status | One of the defined approval states |
| source_path | Exact repository or project path |
| source_ref | Branch, commit, or source system |
| source_sha256 | Hash of original bytes |
| derived_path | Exact path of derivative, if any |
| derived_sha256 | Hash of derivative |
| dimensions | Width × height |
| format | PNG, WebP, SVG, etc. |
| color_profile | Embedded profile / color space |
| transparency | Alpha-channel details |
| character_ids | Canonical IDs, if relevant |
| creator_correction | Relevant correction or none recorded |
| intended_use | Explicit production use |
| excluded_use | What the asset must not be used for |
| toolchain | Tool and version used for derivation |
| notes | Uncertainty, review comments, dependencies |

Do not put invented or estimated values into required fields. Use UNKNOWN and explain.

## 4. Git LFS and file integrity

For every LFS-backed image:
- Retrieve the actual object bytes.
- Confirm the file opens as the expected format.
- Compare the actual SHA-256 against the manifest.
- Record both Git blob/LFS pointer identity and actual file hash where possible.
- Reject pointer text masquerading as an image.
- Do not rewrite the original file to make it easier to use.

For every downloaded or copied file:
- Record byte size.
- Compute SHA-256.
- Confirm dimensions and format using an image inspection tool.
- Keep original and derived paths separate.

## 5. Derivative rules

Every derivative must state:
- Exact parent asset.
- Parent checksum.
- Crop coordinates or layer boundaries.
- Scale and transform.
- Color operations.
- Alpha/compositing settings.
- Tool and version.
- Output checksum.
- Reason for derivative.

Do not use generative fill or AI reconstruction. If an image lacks pixels needed for a camera move, reduce the move or stop; do not synthesize missing content.

## 6. Character and continuity checks

Before approving a character image:
- Confirm canonical character ID.
- Confirm it matches the correct reference sheet.
- Check face, hair, silhouette, clothing, proportions, and color.
- Check that expression labels belong to the correct character.
- Apply recorded creator corrections.
- Compare against prior approved scenes for continuity.

Known mapping:
- Khaled = Character B.
- Kevin = Character A.
- The two “Surprised” portraits filed beneath Kevin were identified by the creator as Khaled.
- ORBIT and the Moon are separate.
- No humanoid Moon design is established.

## 7. Review package

For creator review, provide:
- Contact sheet or side-by-side comparison.
- Full-resolution source and derivative.
- A short note describing exactly what changed.
- Source and derivative hashes.
- Approval state.
- Known limitations.
- Specific decision required, if any.

Do not ask for approval of a large batch without identifying each meaningful design decision.

## 8. Folder conventions

Suggested structure for future art:
```text
production/artwork/
  source_manifests/
  key_art/
  characters/
    khaled_characterB/
    kevin_characterA/
  environments/
  props/
  interfaces/
  title_graphics/
  episode1/
  derived/
  review/
```

This is a proposed organizational structure. Do not move existing source files or change canonical paths without a separate migration plan and approval.

## 9. Review checklist

- [ ] Source file retrieved and opened.
- [ ] Provenance and hash verified.
- [ ] Approval state is accurate.
- [ ] Canonical character/entity identity correct.
- [ ] Creator corrections included.
- [ ] No invented details.
- [ ] Derivative operations documented.
- [ ] Original unchanged.
- [ ] Continuity checked.
- [ ] Creator review captured.
