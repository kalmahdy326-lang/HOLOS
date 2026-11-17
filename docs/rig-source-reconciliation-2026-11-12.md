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


## 2026-11-17 recovery-session addendum — Project Library enumeration

A further read-only Library inventory was performed during the 2026-11-17 recovery session. The root Library listing was paginated and the `/HOLOS` folder was separately checked. The following exact source candidates were found:

| Library path | File | Size | Current evidentiary status |
|---|---|---:|---|
| `/HOLOS/HOLOS_Model_Initialization_Package.zip` | `HOLOS_Model_Initialization_Package.zip` | 64,530 bytes | Located; archive bytes unavailable to this session; contents unknown |
| `/HOLOS/HOLOS_Autonomous_Execution_Package.zip` | `HOLOS_Autonomous_Execution_Package.zip` | 21,652 bytes | Located; archive bytes unavailable to this session; contents unknown |
| `/HOLOS/HOLOS_Episode_1_The_Moon_Has_Anger_Issues_Complete_Screenplay.docx` | Complete Episode 1 screenplay | 48,709 bytes | Located; not required for rig recovery; screenplay contents not inspected in this recovery pass |

The Library also lists character-reference images and HOLOS audio assets. These are not substitutes for Godot project sources.

A raw-byte materialization attempt was made for both ZIP packages and the screenplay. The Library returned: `This Project file does not have an authorized raw-byte materialization path.` No archive was opened, extracted, hashed, or modified. The listed sizes are Library metadata, not independently verified filesystem sizes or checksums.

**Important qualification:** the two ZIP filenames are candidate source packages only. Their names do not establish that either contains a Godot project, character rig, benchmark, or the missing Milestone 3/4 deliverables. Do not describe them as rig archives until their contents are inspected.

### Exact next handoff

Provide the two ZIP files as direct attachments in a session that permits reading their bytes, or export them from the Project Library to an accessible local folder and provide the files. Preserve the original filenames and bytes. On receipt:

1. Compute SHA-256 before extraction.
2. List archive members without extracting over any existing project.
3. Identify every `project.godot`, `.tscn`, `.scn`, `.gd`, imported resource, addon, benchmark, and render.
4. Extract only into a new timestamped recovery workspace.
5. Inventory and hash the extracted tree; inspect project settings and transitive scene dependencies.
6. Compare the evidence against the reported Khaled Milestone 3, Kevin Milestone 4, and two-character interaction work.
7. Only then prepare a non-destructive integration branch.

Until this handoff is complete, rig recovery remains blocked by source access, not by the generic renderer.
