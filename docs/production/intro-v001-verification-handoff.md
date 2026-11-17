# HOLOS — Silent Intro v001 Verification Handoff

**Project author:** Khaled AL-MAHDY  
**Asset:** `HOLOS_Intro_Review_v001.mp4`  
**Status:** User-reported complete; independent verification in the Manus production environment requested. The video/package are not stored in this repository by this document.

## 1. Reported deliverable

The user supplied a production completion report stating:
- 12-second silent visual intro;
- 1280×720;
- H.264 / yuv420p;
- 24 fps;
- 288 frames;
- no audio stream;
- approved poster/key art with orbital background, title reveal, restrained push-in and fade to black;
- full-file FFmpeg decode and ffplay playback checks passed;
- representative encoded frames inspected;
- Godot rendering and FFprobe/media checks passed;
- editable Godot project, rendered frames, asset manifest, checksums and build instructions included in a ZIP package.

Reported MP4 SHA-256:
`be255a5d7d1dec5da31b7591e55543a5e19ca915e9b42dcf3cf65d26c2660044`

The completion report also states the 209-second source M4A and the unapproved 12-second WAV draft were untouched and excluded from the video.

## 2. Provenance and evidence status

This record preserves the user's supplied completion report. It does not independently inspect the Manus-local files.

The paths reported by Manus:
- `/home/ubuntu/HOLOS_INTRO_BUILD/04_RENDER/HOLOS_Intro_Review_v001.mp4`
- `/home/ubuntu/HOLOS_Intro_Review_v001_Package.zip`
- `/home/ubuntu/HOLOS_INTRO_BUILD/05_QC/QC_report.md`

These are environment-local paths, not GitHub repository paths. They must not be treated as accessible from another machine or as checked-in deliverables.

Status:
- **REPORTED COMPLETE:** MP4 render and package creation.
- **REPORTED PASSED:** Godot render, FFprobe/media checks, full-file decode and playback.
- **NOT INDEPENDENTLY VERIFIED HERE:** exact file bytes, MP4 checksum, ZIP integrity, project rerender, offline rebuild and dependency closure.
- **NOT INCLUDED IN THIS REPOSITORY BY THIS DOCUMENT:** MP4, ZIP, frames or local Godot project.

## 3. Independent verification required

Run the verification in the same Manus environment that contains the files:
1. Recompute MP4 and ZIP SHA-256 and compare with recorded values.
2. Run FFprobe; record all stream and format metadata.
3. Confirm exactly 288 decoded video frames, 24 fps, 1280×720, 12.000 seconds and zero audio streams.
4. Decode the entire file again and play it from start to finish.
5. Inspect beginning, title reveal, middle, title hold and ending.
6. Compare the embedded poster to the approved source bytes; record source and derived hashes and transforms.
7. Verify the ZIP and enumerate all members; confirm all frames, Godot project, instructions, manifests and QC records exist.
8. Open the packaged project and rerender into a new, separate verification directory. Never overwrite v001.
9. Test rebuild without network access using only the package and locally installed dependencies.
10. Write `HOLOS_Intro_v001_Independent_Verification_Report.md` with VERIFIED, FAILED, NOT TESTED or BLOCKED per check.

## 4. Preservation and version policy

- v001 is immutable review history.
- Corrections must produce v002 or a separately named candidate.
- Never overwrite original approved artwork or soundtrack.
- Silent review remains distinct from a soundtrack master.
- The final 1920×1080 / 30 fps delivery profile remains a separate future target, not a property of v001.
- Episode 1 body recovery and character rig integration remain separate workstreams.
- Do not claim that a 12-second intro proves the complete episode pipeline or offline acceptance.

## 5. GitHub storage recommendation

Do not commit the ZIP or 288-frame sequence as ordinary Git files. If the creator later wants the video archived in GitHub:
- decide whether a GitHub Release asset, Git LFS or external owner-controlled archive is appropriate;
- check repository/LFS limits and retention first;
- include the MP4, package, checksum sidecar and verification report as a matched release set;
- preserve source files and use a new immutable version tag;
- do not publish unverified media as final.

This handoff is documentation only. It does not upload, modify or certify the Manus-local output.
