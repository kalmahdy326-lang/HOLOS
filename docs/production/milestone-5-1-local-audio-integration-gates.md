# HOLOS Milestone 5.1 — local production WAV integration gates

**Project author:** Khaled AL-MAHDY  
**Record date:** 2026-11-17  
**Status:** REPORTED HANDOFF / BLOCKED — input package and local project not available in this GitHub repository  
**Purpose:** Preserve the integration requirements without treating an incomplete instruction message, an earlier WAV, or an intermediate timeline as production authority.

## 1. Evidence boundary

The project-author supplied a Manus integration instruction naming:

- Local project: `/home/ubuntu/holos_rigging`
- Production scene: `res://scenes/milestone51_production.tscn`
- Scene audio reference currently reported as `res://audio/holos_animation_test_audio_15s.wav`
- Character scripts currently reported as `FunctionalKevin.gd` and `InteractionKhaled.gd`
- A timeline currently reported as `HOLOS_Milestone51_Manual_Phoneme_Timeline.json`

The message received in this session ends immediately after the heading **“1. Required input package — Prepare these two files before changing the Godot project:”**. The two filenames, the files themselves, and the remaining instructions have not been supplied in this handoff.

The local project path and named production scene/scripts are not present in the checked GitHub repository tree inspected for this record. The repository's `godot/holos_timeline.gd` is a generic deterministic timeline consumer; it is not the named production scene, either character rig, or the shared interactive audio transport. No local filesystem access to `/home/ubuntu/holos_rigging` is established here.

Accordingly, this record does **not** claim that the new WAV has been received, hashed, listened to, transcript-checked, or integrated.

## 2. Non-negotiable source gate

Before changing the production Godot project:

1. Obtain both exact files specified by the complete Manus handoff.
2. Identify the approved transcript version and its approval evidence. Do not reconstruct or normalize approved dialogue.
3. Hash the exact WAV bytes (SHA-256) and record filename, byte size, duration, sample rate, channel count, sample format, and codec/container information.
4. Listen to the WAV and compare every spoken turn, in order, against the approved transcript. Confirm that the unapproved leading **“But”** is absent and that the fourth line is complete.
5. Confirm that the WAV is the intended dialogue source, not the previously identified 15-second animation test WAV, theme music, or another provisional recording.
6. Generate or accept a timeline only from the verified WAV and approved transcript. Record the WAV hash, transcript identity/hash, timeline hash, timebase, and measured audio duration together.
7. Reject any timeline whose ordered speaker/word sequence differs from the approved transcript, whose event times are invalid, or whose final event exceeds the measured WAV duration beyond the explicitly approved tolerance.

The earlier intermediate WhisperX timeline described in the handoff is **not an approved production input**. Its leading “But” and incomplete fourth line must not be carried into a replacement timeline.

## 3. Required controller architecture

After the source gate passes, the production integration must implement one transport owner:

- The production director owns the dialogue AudioStreamPlayer and the authoritative transport position.
- The director exposes one shared absolute playback position to both character adapters.
- `FunctionalKevin.gd` and `InteractionKhaled.gd` consume the already-loaded, validated timeline and the same transport position. They must not independently load the timeline JSON.
- Character mouth/viseme state is evaluated as a pure lookup at the supplied absolute audio time. Character scripts must not maintain their own elapsed `_process(delta)` clocks.
- The director must not run a separate elapsed timer. The playing audio stream's playback position is the source of truth.
- Pause, resume, seek, stop, and end-of-stream behavior must be defined by the transport owner and observed consistently by both characters.
- Timeline loading and validation must fail closed. A missing, malformed, transcript-mismatched, or duration-incompatible timeline must prevent the production dialogue benchmark from starting.

This is an integration contract, not a claim that the shared transport has already been implemented in the external project.

## 4. Production changes expected after inputs are available

1. Back up the local project non-destructively and record the baseline inventory/hash manifest.
2. Inspect the actual production scene and all attached scripts before editing.
3. Replace the obsolete scene audio resource path with the verified new WAV path.
4. Introduce one director-owned timeline load and one shared audio-derived transport clock.
5. Update both character scripts to receive the shared timeline/transport state; remove direct JSON loading and independent elapsed timers.
6. Preserve approved dialogue text, source WAV bytes, original rigs, scene structure, and unrelated assets.
7. Do not overwrite the old WAV or timeline. Keep them archived with provenance if they are needed for audit.

## 5. Acceptance tests

The production benchmark remains **NOT ACCEPTED** until all applicable checks pass in the target Godot 4.7.2 project:

### Source and transcript
- Exact WAV SHA-256 and technical metadata are recorded.
- Listening review confirms transcript match, no leading “But”, and a complete fourth line.
- Timeline ordered speaker/word sequence exactly matches the approved transcript.
- Timeline is bound to the exact WAV and transcript hashes and measured duration.

### Architecture
- The scene references the verified WAV, not the obsolete 15-second test file.
- The timeline is loaded once by the director/transport owner.
- Neither character script loads the timeline JSON directly.
- No director or character elapsed-time accumulator advances dialogue animation independently of audio playback.
- Both characters receive the same transport position on every update.

### Runtime synchronization
- Test playback from the beginning, mid-word, across speaker changes, through pauses/resumes, after seeks, and at end-of-stream.
- Confirm both characters evaluate the same absolute audio time and return to rest outside their events.
- Measure and record observed audio/animation offset against a stated tolerance; do not infer synchronization merely because playback starts together.
- Run and capture evidence using Godot 4.7.2 and the actual Khaled/Kevin rigs.

### Preservation and reporting
- Baseline and post-change inventories are retained.
- Original WAV, transcript, timeline, rigs, and scene are preserved or backed up.
- Record exact changed paths, hashes, test commands, runtime version, test results, and unresolved defects.

## 6. Current blockers and next action

**BLOCKED — required inputs:** The instruction message is incomplete at the required-input-package heading. Obtain the remainder of the Manus instructions and the two named files before modifying the production project.

**BLOCKED — execution environment:** The named local project and production rig scripts are not in this repository and have not been accessed through this GitHub session. Repository CI currently validates a separate generic Godot fixture and must not be represented as production-scene acceptance.

**Next action:** Complete the input handoff, then inspect and back up `/home/ubuntu/holos_rigging` in the authorized local/Manus environment. Only after transcript/audio verification should the production scene and controller be changed.
