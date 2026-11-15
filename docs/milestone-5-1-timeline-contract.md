
# HOLOS Milestone 5.1 timeline contract (Godot side)

**Project author:** Khaled AL-MAHDY
**Status:** Consumer implemented; not yet executed against a committed timeline or a character rig.

## Scope

`godot/holos_timeline.gd` loads and validates the JSON timeline committed by
`tools/process_holos_aligned_audio_v2.py` and evaluates it deterministically.
`godot/test_scenes/timeline_selftest.gd` is its headless self-test.

## Processor output compatibility

The processor emits the existing flat event schema with a `schema_version`
field. `build_godot_timeline()` normalizes speaker/viseme values against the
consumer's accepted vocabulary and checks chronology, positive durations and
the optional measured audio duration. It keeps events flat so phoneme timing
is retained. Silence remains an explicit `SIL` event with the `rest` viseme;
unrepresented acoustic gaps also evaluate to rest.

The consumer does not own audio playback. Offline rendering derives time from
the requested frame index and FPS. Interactive playback must pass the same
audio transport position to each character adapter; this repository has no
integrated audio player or character rig adapter yet. Viseme labels are
semantic values only: no blend-shape names or mesh controls are assumed to
exist. Those mappings require inspection of each original rig.

## Deterministic evaluation rule

`HolosTimeline.state_at(time_seconds, speaker)` is a pure function of time.
It never reads the wall clock and never accumulates state. Frame-based
consumers derive time from the frame index (`frame_index / fps`) inside
`holos_set_frame`, consistent with the existing runner contract. A real-time
transport clock (for example an AudioStreamPlayer playback position) belongs
in an interactive rig adapter, not in this class and not in the headless
runner.

## Validation parity

The loader mirrors the Python gate: approved speakers only, supported visemes
(rest, closed, open, wide, round, teeth), chronology, positive durations,
SIL mapped to rest, no unapproved "But", required approved words present, and
an optional audio-duration check when the caller supplies a measured duration.
The Python processor remains the authority; this loader is defence in depth.

## Self-test

`godot --headless --path godot --script res://test_scenes/timeline_selftest.gd`

Exit 0 means all checks passed. The self-test requires no assets and no audio.

## Current limits

- Never executed: no committed timeline exists yet because no real WAV has
  been processed.
- No rig mapping: this class returns viseme labels; mapping visemes to a
  specific rig's blend shapes or animation controls is the per-character
  adapter's job and must not assume control names (per the character rig
  integration contract).
- Audio stays outside the Godot adapter, as already defined in the Godot
  adapter contract; FFmpeg assembles dialogue with rendered frames later.
