# HOLOS — Character Animation, Facial Performance and Dialogue Integration

**Project author:** Khaled AL-MAHDY  
**Scope:** Roadmap from the existing generic Godot shot runner and functional character prototypes to production-ready character performance.  
**Status:** Interface and future work specification; phoneme-level facial animation and original-rig adapters are not claimed complete.

## 1. Source-of-truth hierarchy

1. Latest explicit creator instruction.
2. Original character reference sheets and creator-approved corrections.
3. Original Godot character project/scene and its complete dependency set.
4. Preserved Milestone 3/4 benchmarks.
5. Character-specific adapter and performance configuration.
6. Derived model sheets, expression maps and animation tests.

A model sheet is not a rig. A rig is not a completed performance. A generic Godot adapter test scene is not Khaled or Kevin.

## 2. Character identity and current integration gate

- Khaled = Character B.
- Kevin = Character A.
- The two “Surprised” portraits filed beneath Kevin were corrected by the creator as Khaled.
- ORBIT is the station AI/system voice and is distinct from the Moon.
- The Moon is an unidentified speaking presence communicated through station infrastructure; no humanoid design is established.

The Character Rig Integration Contract requires the complete original project-native resource set for each character: primary scene, scripts, textures/spritesheets, fonts, shaders/materials, animation/skeleton resources, audio resources, addons, autoloads, project settings, input configuration and known-good benchmark.

Before integration:
1. Inventory and hash the source set.
2. Create and verify a backup.
3. Inspect project settings, import settings, plugins and resource path assumptions.
4. Load the original scene unchanged in its native project context.
5. Build a separate HOLOS wrapper around it.
6. Keep adaptation code outside the original scene wherever possible.

The current repository contract records both original rig scenes and dependencies as absent from the inspected repository snapshot. The source handoff remains a gate.

## 3. Existing generic Godot contract

The runner instantiates the configured PackedScene and optionally calls:
```gdscript
func holos_apply_shot(config: Dictionary) -> void:
    pass

func holos_set_frame(frame_index: int, fps: float) -> void:
    pass
```

These hooks are suitable for a wrapper to translate frame-indexed performance state into the original rig's real controls. The hooks do not define the controls themselves.

A character adapter should:
- expose a stable HOLOS-facing interface;
- map explicit character-state identifiers to real rig controls;
- accept absolute frame/time inputs;
- set deterministic pose/face/mouth/gaze state for each requested frame;
- report unsupported states as errors rather than silently ignoring them;
- keep debug controls out of production output.

## 4. Proposed facial/lip-sync data model

This is a proposed future contract, not a description of implemented phoneme control.

Represent speech as timed segments:
- `segment_id`
- `speaker_id`
- `audio_asset_id`
- `start_frame`
- `end_frame`
- `alignment_source`
- `alignment_version`
- `phoneme_events[]`

Each phoneme event should include:
- `phoneme` (from a documented language-specific inventory);
- `start_frame`, `end_frame`;
- `viseme` mapping;
- optional confidence/source timing;
- coarticulation/transition policy.

Use visemes for visible mouth poses; do not assume one unique mouth drawing per phoneme. The mapping table should be character-specific only where the art/rig requires it, while preserving a shared timing interface.

A practical first pass:
1. Verify exact dialogue audio source and speaker identity.
2. Obtain or create alignment from an approved local tool/workflow.
3. Review phoneme timing manually around difficult consonant clusters and pauses.
4. Map phonemes to a small tested viseme set.
5. Add anticipation, jaw motion and neutral holds only where the original rig supports them.
6. Render close-up dialogue tests at normal speed and frame-by-frame.
7. Compare mouth timing against audio; record drift and corrected event times.

Do not infer phoneme timing from the screenplay text alone. Do not use an unapproved audio file as the final performance source.

## 5. Proposed performance state model

Speaking/listening are not single static poses. A future character performance block may include:
- `body_state`: neutral, speaking, listening, reacting, moving (only states actually supported by the rig);
- `gaze_target_id` or explicit target coordinates;
- `head_orientation`;
- `expression_id`;
- `mouth_state` or timed viseme events;
- `gesture_id`;
- `start_frame`, `end_frame`;
- optional transition/easing profile.

For dialogue staging:
- the current speaker receives the speaking performance and appropriate gaze;
- listeners retain independent listening/reaction performance;
- gaze changes should be keyed or deterministically computed from explicit targets;
- avoid every listener staring continuously at the speaker;
- reaction timing must be authored and reviewable, not randomly generated at render time.

These are animation-design requirements, not claims about existing Khaled/Kevin body-state systems.

## 6. Milestone 3/4 prototype-to-production gates

### Khaled — Milestone 3
- Recover original source scene and dependencies.
- Compare against preserved Milestone 3 benchmark.
- Verify neutral pose, face layers, blink, gaze, mouth shapes and head motion.
- Add tested viseme timing and deterministic state evaluation.
- Expand body articulation only using verified rig layers.
- Test close-up, medium and two-character framing.
- Deliver source wrapper, test scene, render set, timing comparison and regression report.

### Kevin — Milestone 4
Repeat the same gates independently. Do not copy Khaled's visual geometry or rig assumptions. Preserve Kevin's distinct approved appearance and performance.

### Two-character benchmark
Only after both independent adapters pass:
- stage a dialogue exchange;
- test speaking/listening overlap;
- verify gaze target handoff;
- test simultaneous reactions;
- validate audio sync;
- render the same frame range twice;
- compare against both single-character baselines.

## 7. Required review evidence

For every character release candidate:
- original source inventory and hashes;
- verified backup manifest;
- adapter scene/script;
- mapping table from HOLOS states to actual rig controls;
- neutral and expression contact sheets;
- mouth/viseme chart with timing examples;
- blink/gaze/body-motion tests;
- audio-aligned close-up;
- repeated-render comparison;
- debug-vs-production comparison;
- known limitations and creator review status.

Do not label a rig production-ready until the original source is integrated and all required gates have evidence.
