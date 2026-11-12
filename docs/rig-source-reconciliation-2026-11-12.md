# Khaled/Kevin rig source reconciliation — 2026-11-12

**Project author:** Khaled AL-MAHDY  
**Status:** Source handoff required; no actual rig scene is verified in the GitHub repository or the searchable HOLOS Project-space Library inventory.

## Conflicting status records

Three records do not currently align:

1. The project memory/earlier production update dated 8 November 2026 described Milestone 3 as a completed and validated functional Khaled rig, with Milestone 4 (Kevin's independent rig using the Khaled architecture) as the next task.
2. `docs/milestone-6-local-production-engine.md` lists a functional Khaled rig, a functional Kevin rig, and an existing two-character interaction prototype among work to preserve.
3. `docs/character-rig-integration-contract.md` states that the current repository contains no Khaled or Kevin rig scenes, scripts, textures, audio, imported resources, or completed character benchmark assets; both source handoffs are blocked.

## Direct repository and Library check

The current production repository tree contains 55 paths. The only Khaled/Kevin-related path is the generic integration contract; no character-specific .tscn/.scn scene, rig script, character asset directory, or benchmark file is present.

The searchable Project-space Library inventory contains 231 items. Under the HOLOS folder, three paired character-reference PNGs were found and visually inspected. No Godot scene, rig script, or character resource files were found in that inventory. The two small production ZIP packages were located, but raw-byte materialization was not authorized in the current session, so their contents are unknown and must not be assumed to contain the rigs.

## Current defensible status

- Character concept/reference sheets: located and visually inspected.
- Khaled rig: reported complete in an earlier milestone note, but original scene/dependency handoff is not currently verifiable.
- Kevin rig: status conflicts between earlier milestone notes; original scene/dependency handoff is not currently verifiable.
- Two-character interaction prototype: claimed in Milestone 6's preservation list, but no source scene or benchmark is present in the current repository tree.
- Generic Python-to-Godot adapter: implemented and CI-tested; it validates the rendering interface, not either character.

## Required reconciliation evidence

Before changing milestone status or beginning integration, recover the original local Godot project(s) and provide:

- full project root(s), including project.godot and addons/autoloads;
- Khaled and Kevin primary scenes and all transitive dependencies;
- scripts, textures, skeletons, animations, materials, shaders, audio and imported resources;
- known-good benchmark scenes/renders and their configuration;
- source inventory and verified backup reports;
- date/version/provenance identifying which milestone record each asset satisfies.

Then update the milestone table based on actual file evidence. Do not generate substitute rigs and label them as the original assets. Do not overwrite or relocate the originals during initial integration.

## Acceptance boundary

A green generic adapter CI run is not a rig validation. Milestone 6 remains in progress until both real character rigs load, render repeatably, pass their individual benchmarks, and the two-character interaction benchmark passes in the target local/offline environment.
