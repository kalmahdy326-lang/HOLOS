# Character rig integration contract

**Project author:** Khaled AL-MAHDY  
**Milestone:** 6 — Local Production Engine  
**Status:** Interface defined; actual Khaled and Kevin scene integration is blocked until their original scene files and dependencies are present.

## 1. Current evidence

The current repository contains a generic Godot runner and a deterministic adapter
test scene. It does not contain the Khaled or Kevin rig scenes, their scripts,
textures, audio, imported resources, or completed character benchmark assets.

The adapter test proves that the Python-to-Godot pipeline can launch a scene,
advance frames, and capture PNGs. It does not prove that either character rig
loads or behaves correctly.

Do not create substitute character scenes and label them as the original rigs.
Do not modify or relocate the original rig files during initial integration.

## 2. Required source handoff

For **each** character, bring the full project-native source set into the
repository or make it available in the target local project:

- The primary Godot scene (.tscn or .scn) for the character.
- Every referenced script (.gd), including inherited scripts and tool scripts.
- All referenced textures, spritesheets, fonts, shaders, materials, audio files,
  animation resources, skeleton resources, and other imported resources.
- Any addons, plugins, autoloads, project settings, or input configuration
  required for the scene to load and animate.
- The known-good character benchmark and its source configuration.
- A short provenance note identifying the original source folder and the
  inventory/backup report used to protect it.

Do not copy only the visible scene file: Godot scenes can depend on resources
and project settings elsewhere in the project. Keep the original directory
structure where practical so res:// references continue to resolve.

Before integration, run inventory, create a verified backup, and retain both
reports/manifests. If the source is in another Godot project, first identify
its project settings, addons, autoloads, and resource path assumptions.
Do not merge two project configuration files blindly.

## 3. Scene hook interface

The existing runner loads the configured res:// PackedScene and instantiates
its root node. The root node may implement these optional methods:

\`\`\`gdscript
func holos_apply_shot(config: Dictionary) -> void:
    pass

func holos_set_frame(frame_index: int, fps: float) -> void:
    pass
\`\`\`

The runner calls holos_apply_shot(config) once after instantiation and before
the frame loop. It then calls holos_set_frame(frame_index, fps) for each
configured frame, in ascending order. frame_index is the configured
half-open episode frame number, not the zero-based PNG filename index.

The adapter must map these stable HOLOS hooks to the character's real animation
system. It must not assume names for the existing rig's animation players,
skeletons, blend trees, mouth shapes, or expression controls until those
resources have been inspected.

The runner currently waits two process frames after each hook call, then
captures the root viewport. The hook should set the complete deterministic
state for the requested frame rather than relying on accumulated wall-clock
delta. If the original rig uses physics, particles, random behavior, or
time-based tweens, document and explicitly control those dependencies before
claiming reproducible frame stepping.

PNG names are local to each shot: the first captured frame is
frame_000000.png, even when the configured start_frame is not zero.

## 4. Adapter layout

Keep character-specific integration outside the generic runner. Prefer one
adapter/root wrapper per character, with its own scene and scripts, for example:

\`\`\`text
godot/
  characters/
    khaled/
      khaled_holos_adapter.tscn
      khaled_holos_adapter.gd
      source/...
    kevin/
      kevin_holos_adapter.tscn
      kevin_holos_adapter.gd
      source/...
\`\`\`

This is a proposed target layout, not a claim that these files already exist.
The wrapper may instance the original character scene as a child and translate
HOLOS configuration into that rig's real controls. Keep the original scene and
its scripts unchanged initially; put adaptation logic in the wrapper wherever
possible.

Use an episode shot's scene field to select the wrapper scene. Character
identity and asset declarations should remain explicit in the episode config;
do not infer which rig to load from filenames or visual appearance.

## 5. Minimum integration tests per character

1. Load the original character scene and all dependencies in the correct
   project context without missing-resource or script errors.
2. Render a short neutral/idle reference shot with no debug overlay.
3. Exercise at least one known-good animation state from the existing benchmark.
4. Render the same frame range twice from the same configuration and compare
   exact hashes where deterministic, otherwise record image differences and
   explain nondeterministic sources.
5. Verify expected output dimensions, frame count, non-empty images, and
   per-frame hashes.
6. Compare the result against the preserved character benchmark; record
   differences rather than silently replacing the benchmark.
7. Run each character through both debug and production modes and verify no
   diagnostics appear in production.
8. Render one two-character interaction scene only after the two independent
   character adapters pass.

## 6. Acceptance record

Complete this table only with evidence from the real source assets:

| Gate | Khaled | Kevin |
|---|---|---|
| Original scene and dependencies inventoried | Blocked — source missing | Blocked — source missing |
| Verified backup exists | Blocked — source missing | Blocked — source missing |
| Scene loads in target project | Not tested | Not tested |
| HOLOS hook wrapper implemented | Not started | Not started |
| Known-good benchmark rendered | Not tested | Not tested |
| Repeat-render comparison | Not tested | Not tested |
| Debug/production comparison | Generic fixture only | Generic fixture only |
| Two-character interaction | Blocked by both adapters | Blocked by both adapters |

## 7. Do not advance the acceptance claim

The generic adapter CI passing is evidence for the rendering mechanism only.
Milestone 6 remains in progress until both original character rigs pass the
tests above and the complete production workflow is accepted on the target
machine with network access disabled.
