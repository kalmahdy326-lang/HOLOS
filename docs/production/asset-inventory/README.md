# HOLOS Animation — Initial Asset Inventory

**Project:** HOLOS — The Fundamental Structure of Reality  
**Episode focus:** Episode 1 — *The Moon Has Anger Issues*  
**Project author:** Khaled AL-MAHDY  
**Inventory date:** 2026-11-26  
**Record version:** 0.1  
**Status:** Read-only discovery pass; proposed organization only

## Purpose and scope

This record identifies HOLOS animation materials located in the accessible ChatGPT Project Library and the connected `kalmahdy326-lang/HOLOS` GitHub repository on 2026-11-26. It is an initial inventory, not a statement that every external drive, local workstation, cloud folder, or older conversation attachment has been exhaustively recovered.

**No original assets were moved, renamed, overwritten, deleted, or copied into this repository during this pass.** The source artwork, screenplay DOCX and audio masters remain in their existing Library locations. Large binary assets are referenced by source name/path and metadata; they are not committed to Git by this inventory.

The folder `/HOLOS` was visible in the Library root, and several assets were found within it by indexed filename search. The Library listing service did not return a complete recursive child listing for that folder in this pass, so this should not be treated as a complete filesystem crawl.

## Executive result

| Area | Finding | Status |
|---|---|---|
| Episode 1 screenplay | Original 25-page DOCX found in Library; text extraction exists in GitHub | Source located; extraction not certified verbatim |
| Character references | Three Khaled/Kevin reference-sheet variants found and visually inspected | Found; select one master set |
| Environment / interface concepts | Lunar station, ORBIT control room, city and apartment boards found | Found; mostly concept-level |
| HOLOS theme | Two M4A files are byte-identical | Duplicate source copies verified |
| Theme text | A short lyric-like text file exists | Relationship to final audio unverified |
| Test audio | 15-second test WAV found | Test only; not approved final |
| Episode 1 opening MP4 | Not located in the accessible Library video listing | Missing / request source |
| “HOLOS Cartoon” folder | No separately named folder found in the accessible root listing | Location unresolved |
| Storyboard | 65-panel storyboard is referenced by project records and GitHub Issue #11 | Actual panel source not inventoried here |
| Original Godot character rigs | Current production repository does not contain Khaled/Kevin source rig scenes | Recovery / integration blocked |
| Production engine | Python/Godot/FFmpeg pipeline code and documentation are in GitHub | Available; actual character-rig acceptance remains open |

## 1. Primary screenplay and series documents

### Episode 1 screenplay

- **Library source:** `/HOLOS/HOLOS_Episode_1_The_Moon_Has_Anger_Issues_Complete_Screenplay.docx`
- **Library metadata:** DOCX, 48,709 bytes, located in the Library on 2026-11-06.
- **GitHub text record:** [Consolidated screenplay extraction](https://github.com/kalmahdy326-lang/HOLOS/blob/main/docs/source_archive/2026-11-episode-1-the-moon-has-anger-issues-screenplay.extracted.md).
- **Important provenance limitation:** The extraction itself says that the full 957-line local attachment was not available for verbatim comparison and labels the result a consolidated chat-derived screenplay, not a certified recovery of the original DOCX. The original DOCX is present in Library metadata, but raw-byte materialization was not authorized in this pass; its comments, tracked changes, exact revision state and binary checksum have not been inspected here.
- **Action:** Preserve the original DOCX unchanged. Establish the authoritative revision and compare it against the GitHub extraction before declaring the text extraction canonical.

### Series bible

- **Source:** `HOLOS_SERIES_BIBLE_v0.1.md`
- **Library metadata:** Markdown, 23,324 bytes, created 2026-11-17.
- **Status:** Foundational working draft. It establishes the series' investigative principle, current character/world rules and Episode 1 premise. It is the best located continuity baseline, but it is not a substitute for explicit creator approval of unresolved details.
- **Action:** Use it as the current working continuity reference; preserve its unresolved questions.

### Generated / non-authoritative research documents

Two generated documents created on 2026-11-26 are also in the Library:

1. **HOLOS Series and Episode 1 Bible – Comprehensive Production Guide** — 49,595 bytes. This report contains useful research leads, but also stale statements (including that no screenplay had been found) and provisional/speculative material. It is not the controlling series bible.
2. **HOLOS Animated Series – Deep-Research Dossier (2026)** — 96,937 bytes. This contains unrelated proposed characters and story elements (including Captain Celeste Vega, a robot companion, an anthropomorphic Moon deity and Dr. Marisol Kahn). These do not match the existing HOLOS screenplay and visual references.

**Disposition:** Retain both documents as historical generated proposals for audit purposes, but do not use either as canon, character design authority or pitch copy without a complete reconciliation.

## 2. Character reference artwork

Three paired Khaled/Kevin model-sheet variants were found under the Library `/HOLOS` folder and visually inspected:

| Asset | Size | Visible content | Initial assessment |
|---|---:|---|---|
| `HOLOS Character Guide: Moonlit Investigators.png` | 2,013,102 bytes | Paired character guide; front/side/back turnarounds and expressions | Strong candidate reference; approval still to be confirmed |
| `HOLOS Character Reference Sheet.png` | 1,949,860 bytes | Alternate paired sheet and model views | Reference variant; compare before locking |
| `HOLOS: Khaled and Kevin Character Sheet.png` | 2,085,157 bytes | Alternate paired sheet and expression/model views | Reference variant; compare before locking |

The visible guide labels describe Khaled as age 38, 6'1", brown hair, blue eyes, senior researcher; Kevin as age 23, 6'0", red hair, blue eyes, junior investigator. The current working series bible records Khaled as Character B / senior relational physicist and Kevin as Character A / junior systems investigator. The artwork is the authority for visual appearance, but the three near-duplicate sheets still need one creator-selected master reference.

**Do not treat the concept boards or posters as substitutes for these model sheets.**

## 3. Environment, interface and key-art concepts

The following concept images were found and visually inspected:

| Asset | Size | Visible subject | Continuity / use note |
|---|---:|---|---|
| `Orbit Research Control Room.png` | 2,199,216 bytes | ORBIT control room with Region A/B/C panels and temporal alignment | Useful station/interface design reference; screen data remains placeholder-like |
| `HOLOS: Lunar Mystery Concept Board.png` | 2,900,359 bytes | Lunar research station, Khaled, Kevin, Scott, ORBIT and a face-like Moon concept | Exploratory only: shows Scott the Wizard, Kevin age 25, a physical ORBIT orb and a personified Moon; several details conflict with current working bible/reference sheets |
| `Holos: The Lunar Interface.png` | 2,800,327 bytes | Poster-style lunar key art with Khaled and Kevin | Key-art concept, not a model sheet or approved shot reference |
| `HOLOS: The Moon Has Anger Issues.png` | 2,656,633 bytes | Episode-title poster with Khaled, Kevin and Moon imagery | Key-art concept; not evidence of an approved opening frame |
| `HOLOS Futuristic City Reference Board.png` | 2,321,661 bytes | City, transit, vehicles, buildings and branding | Wider-world concept; the located Episode 1 screenplay is set at the lunar research station, so city use in Episode 1 needs script support |
| `Khaled’s Cozy Futuristic Apartment.png` | 2,219,876 bytes | Warm apartment interior with city view | Optional environment concept; no located screenplay evidence makes it an Episode 1 set |
| `Cosmic HOLOS Ensemble Poster.png` | 2,731,947 bytes | Space/lunar ensemble poster with a face-like Moon and orb-like AI imagery | Exploratory poster; not canonical character/interface authority |
| `HOLOS: Orbital Echoes.png` | 3,313,896 bytes | Khaled/Kevin expression collage, orb-like ORBIT and face-like Moon | Potential character-expression reference, but it conflicts with the non-humanoid ORBIT interface rule; use only after reconciliation |
| `HOLOS: Cosmic Reality Unveiled.png` | 2,872,208 bytes | Cosmic poster artwork | General key art; not episode continuity evidence |

The visual material suggests a cinematic science-fiction world with dark lunar environments, blue/cyan interface lighting and stylized, expressive character artwork. The final animation medium, rendering method, material treatment, linework and color tokens are **not yet locked by this inventory**.

### Continuity conflicts to resolve

- Some concept art labels Kevin as age 25, while the paired character sheets label him as age 23.
- Some concept boards depict ORBIT as a physical floating orb; the working series bible describes ORBIT as a non-humanoid station AI/system voice.
- Some concept boards depict the Moon as a face or humanoid presence; the working series bible preserves the Moon's identity and origin as unresolved.
- Scott the Wizard appears in one concept board but is not established as a principal character in the current working bible.
- Poster clothing and styling vary from the paired turnaround sheets.

These images should be tagged `CONCEPT — REVIEW` until a single continuity decision is recorded.

## 4. Audio inventory

### HOLOS theme

Two Library files were located:

- `HOLOS theme.m4a` — 1,307,950 bytes
- `HOLOS theme(1).m4a` — 1,307,950 bytes

Both were materialized for read-only inspection and found to have the same SHA-256:

`aee4733881850f4a3a83be5ae6b69c94cdbbbebc4467916ad3aeec5b3e3bd09e`

FFprobe reports a 209-second AAC audio stream, 48 kHz, stereo, in an M4A/MP4-family container. The files are byte-for-byte identical. This is a duplicate-copy relationship, not evidence of two alternate mixes.

**Action:** Keep both Library originals untouched. In the production manifest, designate one logical canonical source and mark the other as a duplicate alias only after creator confirmation of the preferred filename.

### Other audio files

- `holos_animation_test_audio_15s.wav` — 2,880,078 bytes; test audio, not established as a final theme or approved Episode 1 dialogue master.
- `HOLOS theme.txt` — 499 bytes; contains a short lyric-like text fragment. Its association with the 209-second theme, completeness and approval are not verified.
- `Digital Wasteland.m4a` — 5,404,311 bytes; found in Library, but no current HOLOS production record establishes that it belongs to this episode. Keep unassigned pending confirmation.

Do not replace, trim, remix or normalize the original theme source. Create derived working copies and document their source checksum.

## 5. Video and opening sequence

The accessible Library video listing returned only:

- `sample-render-synthetic-test.mp4` — 433,000 bytes, created 2026-10-31.
- `demo_render.mp4` — 815,023 bytes, created 2026-10-31.

Their names identify them as generic synthetic/demo renders, not the HOLOS Episode 1 opening. **The actual 12-second Episode 1 opening MP4 was not found in the accessible Library video listing.**

The supplied technical target for the opening remains:

- 12 seconds
- 1920×1080
- 24 fps
- H.264 video
- AAC audio

The production report describes an intended non-dialogue sequence (lunar approach, Khaled vignette, Kevin vignette, ORBIT panels, then HOLOS and episode title), but the original beat sheet and rendered MP4 have not been inspected as source assets in this inventory. Treat this description as a documented intention, not as proof of what the current video contains.

At 24 fps, a 12-second opening is 288 frames. The current `examples/episode_01.json` in the repository is explicitly a placeholder at 1280×720 with a 240-frame/10-second shot; it is not the opening master configuration.

## 6. Storyboard, rigs and production code

### Storyboard and screenplay reconciliation

GitHub Issue [#11 — Obtain authoritative screenplay and verify all 65 storyboard panels](https://github.com/kalmahdy326-lang/HOLOS/issues/11) records that a 65-panel text storyboard exists and requires panel-by-panel comparison with the authoritative screenplay. The actual storyboard source file was not independently located in this Library inventory.

Do not call the storyboard locked or screenplay-verified until every panel has an evidence-linked disposition.

### Godot character rigs

The production repository's [Character Rig Integration Contract](https://github.com/kalmahdy326-lang/HOLOS/blob/main/docs/character-rig-integration-contract.md) states that the current repository contains a generic Godot runner/test scene, not the original Khaled/Kevin character rig scenes and dependencies. It explicitly blocks claims of actual-rig integration until source scenes, scripts, textures and dependencies are recovered and tested.

The Library archive register previously identified `HOLOS_Model_Initialization_Package.zip` (64,530 bytes) and `HOLOS_Autonomous_Execution_Package.zip` (21,652 bytes), but those archives have not been inspected or integrated. Their contents must not be inferred from their filenames.

### Production code

Primary animation repository: [kalmahdy326-lang/HOLOS](https://github.com/kalmahdy326-lang/HOLOS)

Useful source-of-truth links:

- [README / production architecture](https://github.com/kalmahdy326-lang/HOLOS/blob/main/README.md)
- [Quickstart](https://github.com/kalmahdy326-lang/HOLOS/blob/main/docs/quickstart.md)
- [Milestone 6 local production engine](https://github.com/kalmahdy326-lang/HOLOS/blob/main/docs/milestone-6-local-production-engine.md)
- [Character rig integration contract](https://github.com/kalmahdy326-lang/HOLOS/blob/main/docs/character-rig-integration-contract.md)
- [Episode 1 starter configuration](https://github.com/kalmahdy326-lang/HOLOS/blob/main/examples/episode_01.json)
- [Screenplay text extraction](https://github.com/kalmahdy326-lang/HOLOS/blob/main/docs/source_archive/2026-11-episode-1-the-moon-has-anger-issues-screenplay.extracted.md)
- [Production source archive register](https://github.com/kalmahdy326-lang/HOLOS/blob/main/docs/source_archive/README.md)

Separate HOLOS research repository: [kalmahdy326-lang/holos-reality](https://github.com/kalmahdy326-lang/holos-reality). Keep its scientific research material separate from animation assets and production code.

## 7. Folder-name and location findings

The Library root listing exposed `/HOLOS`, `/How the World Works`, `/Red Lion` and `/Space`. No separately named `HOLOS Cartoon` folder was visible in the accessible listing or returned by targeted Library search.

The `/HOLOS` Library folder contains the three paired character sheets and the original screenplay DOCX among other material. Some files in that folder (for example, research initialization documents) belong to the separate HOLOS scientific research programme and should not be mixed into the animation asset tree.

**Action:** Ask for the exact drive/path or folder link for the “HOLOS Cartoon” folder if it is stored outside the accessible Project Library. Do not create a replacement folder or move similarly named material as a guess.

## 8. Recommended disposition

| Group | Disposition |
|---|---|
| Original screenplay DOCX | Preserve unchanged as the source; compare extraction against it |
| GitHub screenplay extraction | Keep as a provisional text snapshot until exact source comparison |
| Three Khaled/Kevin sheets | Preserve all variants; select and approve one master reference |
| ORBIT control-room concept | Keep as environment/interface design reference |
| Lunar concept board, posters and city/apartment art | Preserve as concept material; mark `CONCEPT — REVIEW` |
| Duplicate HOLOS theme M4As | Keep both originals; record identical checksum; select canonical filename |
| 15-second test WAV | Keep as test/reference only |
| Generic MP4 demos | Keep outside the Episode 1 opening deliverable |
| Generated speculative dossiers | Archive as non-authoritative proposals; do not use as canon |
| Uninspected ZIP packages | Preserve and inspect only after raw access/transfer is available |
| Missing opening MP4 | Recover from creator's source location; do not reconstruct and call it original |

## 9. Next actions for the inventory stage

1. Locate and inspect the real 12-second opening MP4; record SHA-256, FFprobe metadata and exact shot/timecode observations.
2. Obtain the precise `HOLOS Cartoon` folder path or share link and enumerate its contents.
3. Confirm which of the three paired character sheets is the master design reference.
4. Recover the actual Godot rigs and their dependencies from the original project or archives.
5. Reconcile the screenplay DOCX with its GitHub extraction and the 65-panel storyboard.
6. Confirm the canonical theme filename and the relationship (if any) of `HOLOS theme.txt` to the original M4A.
7. After these are complete, migrate approved copies into the target project tree and add checksums, provenance and rights fields to the manifest.

---

**Inventory boundary:** This document records what was found and inspected. It does not certify asset ownership/licensing, screenplay fidelity, character-rig functionality, storyboard approval, or completion of the opening/full episode.
