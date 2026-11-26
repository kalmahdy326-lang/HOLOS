# HOLOS Episode 1 — Pacing Analysis Integration

**Version:** 0.1  
**Date:** 2026-11-26  
**Project author:** Khaled Al Mahdy  
**Status:** Production-control addendum; phase timing is accepted as the governing timing spine. Per-panel timing and audio binding remain pending.

## 1. Timing authority

The creator-designated **Episode 1 Pacing Analysis** is the top-level timing authority for the 15:14.84 (914.84-second) main-program master. The nine phase boundaries are recorded in the machine-readable planning feed v0.2 and remain mirrored in the editorial blueprint.

Phase boundaries use start-inclusive, end-exclusive intervals. The exact phase durations are:

| Phase | In | Out | Duration |
|---|---:|---:|---:|
| P01 — Cold open / ordinary world | 00:00 | 00:47 | 0:47 |
| P02 — Anomaly | 00:47 | 02:04 | 1:17 |
| P03 — Threshold crossing | 02:04 | 04:30 | 2:26 |
| P04 — Epistemic framework | 04:30 | 06:44 | 2:14 |
| P05 — Catalyst | 06:44 | 07:54 | 1:10 |
| P06 — Midpoint transformation | 07:54 | 09:51 | 1:57 |
| P07 — Controlled crisis | 09:51 | 11:58 | 2:07 |
| P08 — False resolution / debrief | 11:58 | 13:55 | 1:57 |
| P09 — Final reframe | 13:55 | 15:14.84 | 1:19.84 |

P09 carries the 0.84-second residual to the exact master out-point. It is not permission to add dialogue, music, or exposition.

## 2. Timing schema decision

Use a **machine-readable timing layer inside the episode planning JSON**, while keeping the Episode 1 Pacing Analysis as the editorial source of truth. The JSON is a synchronized implementation mirror, not an independent authority. This avoids requiring the animation controller to parse prose while preserving one editorial authority.

The JSON records:
- exact phase in/out timecodes and durations;
- numeric seconds for deterministic calculations;
- provisional 24 fps phase-boundary frame estimates;
- protected listening/transition beats;
- dialogue-headroom windows;
- original storyboard panel-to-phase assignments; and
- explicit pending states for per-panel timing and audio references.

The 24 fps numbers are planning estimates only. The opening is the only segment whose 24 fps specification is currently confirmed. Probe the approved full master with FFprobe before locking frame count or frame endpoints. At 24 fps, 914.84 seconds equals 21,956.16 frame intervals; 21,956 is only a rounded estimate, not an exact accepted frame count.

## 3. Canonical storyboard phase assignment

The canonical text storyboard contains **62 main-story panels** across S01–S07 and **three post-credit panels**. The companion `panel-phase-map.csv` preserves every original panel ID and assigns it to a dramatic phase:

- S01_001–S01_003 → P01; S01_004–S01_009 → P02.
- S02_001–S02_009 → P03.
- S03_001–S03_008 → P04.
- S04_001–S04_004 → P05; S04_005–S04_010 → P06.
- S05_001–S05_008 → P07.
- S06_001–S06_005 → P07; S06_006–S06_009 → P08.
- S07_001–S07_005 → P08; S07_006–S07_009 → P09.
- PC_001–PC_003 → post-credit timing pending; outside the 15:14.84 main-program master unless an approved revision says otherwise.

These are phase-level assignments based on the described panel content and sequence. They are not per-panel timecodes. The map intentionally leaves panel in/out and frame columns blank until the transcript, cue sheet and animatic are reconciled. It also does not force a one-to-one relationship between the canonical storyboard panels and the 65 newly proposed production-shot IDs.

## 4. Protected beats and mix/visual constraints

**02:04–02:30 — protected listening space (approximate).** Longer hold, minimal cuts and no decorative/non-diegetic overlays. Preserve room tone and the voice/listening space.

**Around 09:51 — protected crisis-transition anchor.** Preserve the transition into the controlled crisis. The exact duration of the hold is not specified and must come from the audio sources and animatic.

**07:54–09:51 — dialogue headroom across the feedback crisis.** Dialogue takes precedence. Effects must be shaped/ducked around speech. Avoid competing visual layers over key lines. Keep signal convergence, warning, physical failure and Kevin’s injury legible in a clear visual hierarchy.

**13:55–15:14.84 — protected final reframe.** Longer holds, minimal cuts, no decorative overlays or lower thirds. Only diegetic data graphics required by the story may appear. Protect the raw-record command, final Unknown Voice lines, silence and exact out-point.

## 5. Cast and identity reconciliation

- **Scott:** Creator-confirmed approved canon character asset. Episode 1 scene/shot placement is pending. No Episode 1 speaking role or dialogue is established. Keep Scott out of Episode 1 scene-cast lists and do not invent a cameo or lines. The Series Bible update is recorded on PR #9's `docs/holos-series-bible` branch.
- **Dr. Al Mahdy:** The creator has confirmed that this reference is Khaled (Character B), not a separate researcher or third character. “Elmahdi” in transcript/secondary reference material is an error. The canonical spelling for new and corrected production records is **Al Mahdy** (two words, no hyphen). The existing screenplay quotation in the source evidence is retained verbatim and is not the normalized form; preserve source files unchanged. Use Khaled/Character B for all model, rig and cast labels. Keep the screenplay's “Dr.” wording where it appears, without inferring further biography. See the cast reconciliation register v0.3.
- The five established Episode 1 speaking/story identities remain Khaled, Kevin, ORBIT, The Moon and the Unknown Voice. Scott is an approved asset, not an additional Episode 1 speaking identity.

### Panel IDs versus proposed production-shot IDs

The canonical storyboard contains 62 main-story panels and three post-credit panels (65 unique panel IDs total). The proposed shot list in Blueprint v0.1 contains 65 *new production-shot IDs*, all provisionally assigned within the 15:14.84 main-program timeline. These two sets are not interchangeable. No validated panel-to-shot mapping currently demonstrates how the 62 main-story panels expand into the 65 proposed production shots. The 65-shot schedule remains a planning allocation, not a claim that all 65 canonical storyboard panels are in the main program. Keep the three post-credit panel IDs separate and untimed until approved.

## 6. Transcript and cue-sheet intake

The creator confirms that a timestamped transcript and a detailed sound-design cue sheet now exist. Their exact files were not surfaced by the connected Library or repository searches performed on 2026-11-26. The general HOLOS deep-research dossier contains generic cue-sheet guidance, not the episode-specific cue sheet.

When the actual sources are located, commit searchable derivatives alongside the screenplay extraction as separate, provenance-labelled files. Preserve the original files unchanged. Each derivative must record original filename, source location, version/date, source hash where available, extraction method, and limitations. Then:
1. use transcript timecodes to align dialogue and speaker turns;
2. use the cue sheet to align SFX, music, ambience and listening pauses;
3. reconcile all 62 body panels and 65 proposed production shots without silently merging or splitting them;
4. write panel/shot timecodes and frames using the verified full-master timebase; and
5. bind audio cue IDs to the shot configuration and QC manifest.

Do not infer per-shot timing from phase boundaries alone.

## 7. Status

**Accepted:** 15:14.84 main-program timing spine; nine phase boundaries; protected listening/headroom requirements; Scott asset status; creator-confirmed Dr. Al Mahdy / Khaled (Character B) identity and surname spelling.

**Provisional:** panel-to-phase assignments; 24 fps full-episode frame estimates; panel-to-production-shot correspondence.

**Pending:** exact location/hash of the pacing-analysis source file; transcript and cue-sheet source files; per-panel/per-shot in/out timecodes; full-master FFprobe metadata; post-credit duration; final shot/audio binding.
