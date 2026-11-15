# Animation synchronization notes

Status: proposed editorial cue sheet. Not frame-accurate and not synchronized to rendered audio.

## Clock authority
When integrated into HOLOS, the approved audio file must be the sole playback clock. The director/controller reads the audio playback position and distributes that same position to every animated character and visual layer. Character scripts must not run independent elapsed-time clocks for lip sync or cue timing.

For render-at-frame, derive audio time from global frame index and render FPS, then evaluate every animated track at that same time. Independent process-delta accumulators can drift and are not acceptable for synchronized production.

## Lip-sync policy
- The intro theme is external narration, not character dialogue.
- No character is singing or speaking the lyrics.
- Do not animate Khaled or Kevin as if delivering the lyric.
- Use expressions, gaze, body action and environmental timing to react to music.
- The anonymous final “Look between” texture does not assign a mouth performance to the Unknown Voice.

## Picture-lock procedure
1. Select and approve actual audio.
2. Measure exact duration and inspect waveform/transients.
3. Replace provisional cue timestamps with measured timestamps.
4. Confirm project FPS and frame-rounding convention.
5. Convert cue times to frame indices.
6. Test opening cut, chorus accents, fourth-signal reveal and final title hit.
7. Render a low-resolution synchronization benchmark.
8. Inspect audio and video together, then approve picture lock.
9. Preserve source audio and record edit offsets.

For cue time t and frame rate fps, nominal frame index is round(t * fps). Choose and consistently apply one rounding convention.

## Acceptance
A sync test passes only after actual audio and rendered animation have been played together and inspected. A valid CSV or successful Python test does not prove audiovisual synchronization.
