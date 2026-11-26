# HOLOS Animation — Proposed Folder Map

**Status:** Proposed target structure, not a claim that these folders currently exist.  
**Principle:** preserve source originals, version working documents, keep production code separate from binary media, and never overwrite a source asset.

## Target inside the existing `kalmahdy326-lang/HOLOS` repository

```text
docs/
  production/
    README.md
    asset-inventory/
      README.md
      asset-manifest.csv
      folder-map.md
    series-bible/
      HOLOS_SERIES_BIBLE_v0.1.md
      decisions.md
      continuity-register.md
    episode-01/
      screenplay/
        source-record.md
        screenplay-extraction.md
        verification-matrix.csv
      storyboard/
        panel-breakdown.md
        panel-register.csv
      animatic/
        timing-sheet.csv
        review-notes.md
      shots/
        shot-list.csv
        shot-status.csv
      audio/
        music-cue-sheet.csv
        dialogue-cue-sheet.csv
      qc/
        opening-qc-report.md
        episode-qc-report.md

assets/
  source-register/
    asset-manifest.csv
  character-reference/
    khaled/
    kevin/
  environments/
    mare-umbrae/
    control-room/
    corridors/
    city/              # use only where supported by approved story material
    apartments/        # use only where supported by approved story material
  interface/
    orbit/
  props/
  fx/
  logos/

media/
  original/
    audio/
    video/
    artwork/
  working/
    audio/
    video/
    image-sequences/
  approved/
    audio/
    video/
    artwork/
  previews/
  masters/

godot/
  characters/
    khaled/
    kevin/
  scenes/
  scripts/
  materials/
  textures/
  audio/

output/
  renders/
  manifests/
  reports/
  recovery/
  qc/

```

## Source / working / approved distinction

- **original:** an immutable source received from the creator or recovered from the original project.
- **working:** a derived copy being edited, converted, cleaned, animated or mixed.
- **approved:** a specific revision explicitly accepted for production use.
- **preview:** a review export; never a master.
- **master:** final delivery output with a QC report and matching manifest.

Do not store original source binaries in generated-output directories. Keep Git source code and production documentation versioned in Git. Use Git LFS or a controlled local artifact store for large binaries only after deciding the offline-compatible storage and backup policy.

## Asset naming convention

Use a predictable identifier and preserve the original filename in the manifest:

`HOLOS_EP01_<ASSETTYPE>_<SHORTNAME>_v001_<STATUS>.<ext>`

Examples:

- `HOLOS_EP01_CHAR_KHALED_REF_v001_SOURCE.png`
- `HOLOS_EP01_AUDIO_THEME_v001_SOURCE.m4a`
- `HOLOS_EP01_VIDEO_OPENING_v001_REVIEW.mp4`
- `HOLOS_EP01_SHOT_S01_B03_v001_PREVIEW.mp4`

Never rename or move the original Library file just to impose this naming convention. Apply it only to approved working copies.

## Required manifest fields

`asset_id, original_filename, library_or_source_path, category, episode, version, status, byte_size, sha256, created_or_received_date, source_owner, rights_basis, approval_record, dependencies, notes`

A checksum is mandatory before any copy or transformation. Record an unavailable checksum as blank with an explicit reason; do not invent one.

## Change-control rules

1. Record source path and file size before import.
2. Generate SHA-256 for any binary that can be lawfully/raw-byte accessed.
3. Preserve the original unchanged.
4. Create a working copy for editing.
5. Record tool versions and transformation settings.
6. Obtain creator approval before promoting a working revision to `approved`.
7. Publish new revisions; do not overwrite prior approved files.
