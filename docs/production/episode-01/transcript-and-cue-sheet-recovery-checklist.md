# HOLOS Episode 1 — Transcript and Sound-Cue Source Recovery Checklist

**Version:** 0.1  
**Date:** 2026-11-26  
**Project author:** Khaled AL-MAHDY  
**Status:** Intake checklist; no missing file is assumed absent from the creator's local workspace.

## 1. Locate the originals

- [ ] Search the current project workspace and its subfolders for timestamped transcript exports, subtitle files, cue sheets and audio session exports.
- [ ] Search the HOLOS Project-space Library and Drive locations for likely filenames and revisions.
- [ ] Record the exact path/location and original filename; do not rename or move the source originals.
- [ ] Check whether the transcript is a standalone document, an export from an editor, or embedded in a production package.
- [ ] Check whether the sound-design cue sheet is a standalone spreadsheet/document or part of a DAW/session package.
- [ ] Identify the owner/author, creation date, modified date, version and approval status of each source.
- [ ] If several candidates exist, retain all candidates and compare them; do not select the newest file solely by modification date.

## 2. Preserve and checksum

- [ ] Make a verified working copy without altering the original.
- [ ] Calculate SHA-256 for each original source file and record its byte size.
- [ ] Record the tool and version used for hashing and extraction.
- [ ] Preserve comments, revision history, sheet tabs, hidden rows/columns, embedded audio and media references where applicable.
- [ ] Keep extracted text/CSV derivatives separate from the originals and label them as derivatives.
- [ ] Confirm that all derivatives can be traced back to their exact source filename and SHA-256.

## 3. Transcript verification

- [ ] Verify that all nine pacing phases and the 15:14.84 main-program out-point are represented.
- [ ] Confirm speaker labels against the established five Episode 1 identities.
- [ ] Record dialogue in/out timecodes and timecode format (SMPTE, milliseconds, samples or editor-specific).
- [ ] Check for omitted pauses, overlaps, pickups, alternate takes and non-dialogue vocal events.
- [ ] Preserve exact dialogue spelling, including the Scene 4 source wording “Dr. AL-MAHDY”; do not harmonize spelling by assumption.
- [ ] Reconcile the timestamped transcript against the authoritative screenplay revision and list every discrepancy.

## 4. Sound-design cue sheet verification

- [ ] Record every cue ID, type (dialogue, music, ambience, SFX, transition, silence), in/out timecode and duration.
- [ ] Identify whether cue times are locked to the full master, a dialogue master, a music stem or a rough assembly.
- [ ] Record overlaps, fades, pre-laps, tails, intentional silence and ducking/headroom instructions.
- [ ] Check the 02:04–02:30 listening window, the 09:51 crisis-transition anchor, dialogue headroom through 07:54–09:51, and 13:55–15:14.84 final-reframe window.
- [ ] Confirm the three isolation operations have separate sonic identities.
- [ ] Record source audio filenames and hashes for any cue that references a media file.

## 5. Reconcile before assigning panel frames

- [ ] Confirm the full master video/audio duration, frame rate, timebase, start time and stream offsets with FFprobe.
- [ ] Identify whether transcript and cue-sheet timecodes reference the same master.
- [ ] Map 62 main-story storyboard panel IDs to phase(s), then to the 65 proposed production-shot IDs; permit one-to-many or many-to-one mappings only when justified by content and reviewed.
- [ ] Keep PC_001–PC_003 outside the 15:14.84 main program unless a separate post-credit duration is approved.
- [ ] Derive panel/shot frame ranges from verified source timecodes, using start-inclusive/end-exclusive ranges.
- [ ] Validate that no gaps, overlaps or accidental duration changes have been introduced.
- [ ] Run a listening/animatic review for pause duration, dialogue clarity, visual density and final out-point.
- [ ] Update the JSON feed and CSV maps only after these checks; keep all earlier versions for rollback.

## Acceptance record

For each source, record: filename; original path; version; approval state; byte size; SHA-256; timecode basis; extraction method; derivative paths; verifier; date; and unresolved discrepancies.

**Stop condition:** If the original transcript or cue sheet cannot be located or its timecode basis cannot be established, retain the phase-level timing plan and leave per-panel/per-shot timecodes unassigned. Never infer missing cue or dialogue boundaries from phase duration alone.
