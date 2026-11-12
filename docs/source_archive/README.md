# HOLOS production source archive

**Project author:** Khaled AL-MAHDY  
**Purpose:** Preserve readable screenplay text and document the visual reference assets discovered in the Project-space Library, without claiming that the original binary assets have been copied into Git.

## Screenplay text snapshot

| Source | Library size | GitHub record | Status |
|---|---:|---|---|
| HOLOS_Episode_1_The_Moon_Has_Anger_Issues_Complete_Screenplay.docx | 48,709 bytes | [Extracted Markdown](2026-11-episode-1-the-moon-has-anger-issues-screenplay.extracted.md) | 25-page text extraction committed; source DOCX binary remains in Library |

The source title page does not provide a reliable document date in the extracted text. The GitHub snapshot therefore records the date as unknown rather than inferring one from the migration date.

## Character reference assets discovered and inspected

These are concept/reference sheets, not the production Godot rigs.

| Library source | Size | Visible content |
|---|---:|---|
| HOLOS Character Guide: Moonlit Investigators.png | 2,013,102 bytes | Khaled and Kevin, front/side/back turnarounds, expression panels, dark lunar-station setting, Episode 1 title |
| HOLOS Character Reference Sheet.png | 1,949,860 bytes | Alternate character-guide layout with front/side/back views, expression panels and HOLOS branding |
| HOLOS: Khaled and Kevin Character Sheet.png | 2,085,157 bytes | Another paired character sheet with the same core character identities and appearance |

The reference artwork labels Khaled as age 38, 6'1", brown hair, blue eyes, senior researcher; Kevin as age 23, 6'0", red hair, blue eyes, junior investigator. The artwork presents distinct silhouettes and expressions: Khaled has brown hair and a more restrained, analytical presentation; Kevin has red hair and a more expressive, rebellious presentation. These are visual design references only; they do not establish the state of any actual rig.

## Related source packages located

| Source package | Library size | Current handling |
|---|---:|---|
| HOLOS_Model_Initialization_Package.zip | 64,530 bytes | Identified; raw-byte materialization unavailable in this session, so contents not inspected |
| HOLOS_Autonomous_Execution_Package.zip | 21,652 bytes | Identified; raw-byte materialization unavailable in this session, so contents not inspected |
| HOLOS_Episode_1_The_Moon_Has_Anger_Issues_Complete_Screenplay.docx | 48,709 bytes | Text extraction committed; original binary not committed |

The ZIP files were not opened or integrated. Their contents must not be inferred from filenames. The actual Khaled/Kevin Godot rig scenes and dependencies remain a separate, unverified asset-recovery task.

## Preservation limitations

- The screenplay Markdown is a text extraction, not a DOCX binary.
- The three PNG originals were visually inspected but have not been committed to Git; the project register records their Library names and sizes.
- No SHA-256 is claimed for these source binaries.
- Do not overwrite or delete Library originals.
- Large binary asset strategy (Git LFS or another controlled artifact store) remains open pending a local/offline-compatible review.
