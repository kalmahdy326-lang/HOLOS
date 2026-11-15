# Episode 1 — Shared Audio Clock Integration Contract

**Status:** implementation scaffold; not production-validated.  
**Companion:** `godot/episode_audio_transport.gd`

## Required architecture

There must be exactly one dialogue transport for the active episode scene:

- The director owns the transport lifecycle.
- Khaled's actor adapter reads the transport position.
- Kevin's actor adapter reads the same transport position.
- Each actor asks the timeline for its own speaker-specific viseme at that shared time.
- No actor starts a second audio player or maintains a separate accumulated animation clock.

The transport exposes play-from-start, pause, resume, stop, seek and a playback-position estimate. The estimate is derived from the active Godot audio player and AudioServer mix timing, not a manually accumulated `delta`.

## Integration example

The following is an architectural example. Node paths and rig controls must be replaced only after inspecting the actual production project:

```gdscript
# Director owns one shared transport and one validated timeline.
var transport: HolosEpisodeAudioTransport
var timeline: HolosTimeline

func _process(_delta: float) -> void:
    if not transport.is_playing():
        return
    var shared_seconds := transport.get_transport_seconds()
    var khaled_state := timeline.state_at(shared_seconds, "KHALED")
    var kevin_state := timeline.state_at(shared_seconds, "KEVIN")
    # Send semantic visemes to each actor's verified rig adapter.
```

Do not paste this example into a production scene until the project-specific node paths, audio file, timeline timebase and rig mappings have been verified.

## Timebase selection gate

The absolute timeline uses source-MP3 seconds. The relative review timeline uses review-WAV seconds and records a 0.091-second source offset. A controller must load only the timeline whose provenance is tied to the exact audio file it plays.

The current Manus and Codex review WAV hashes differ. This scaffold intentionally does not choose either variant and does not include a default audio path.

## Required tests before acceptance

1. One audio player is the only dialogue transport in the episode scene.
2. Play, pause, resume, stop and seek update both actors from the same position.
3. At a fixed transport position, repeated actor queries return identical timeline states.
4. Kevin events never drive Khaled's rig; Khaled events never drive Kevin's rig.
5. Seeking across a word boundary updates both actors on the same frame.
6. Paused playback holds the last transport position without advancing mouths.
7. End-of-stream returns both rigs to their approved rest poses.
8. Measured A/V offset stays within the approved tolerance over the complete dialogue.
9. The selected audio file hash, measured duration and timeline provenance are recorded in the production manifest.

A passing generic timeline test is not a substitute for this two-character integration benchmark.
