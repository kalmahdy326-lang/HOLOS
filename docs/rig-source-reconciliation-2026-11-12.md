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


## 2026-11-17 extended Library inventory and checksum-sidecar finding

The Library root was enumerated through all pages available in this session (250 items; no continuation cursor). The extension-filtered inventory found no standalone native Godot project/scene/script or common 3D source files anywhere in those 250 entries: no `.tscn`, `.scn`, `.gd`, `.tres`, `.res`, `.blend`, `.glb`, `.gltf`, `.fbx`, or `.obj`. This is a Library metadata inventory, not proof that no external/local project exists.

Exact Library metadata for the two production package candidates:

| File | Library path | File ID | Library file ID | Listed size |
|---|---|---|---|---:|
| `HOLOS_Model_Initialization_Package.zip` | `/HOLOS/HOLOS_Model_Initialization_Package.zip` | `file_00000000589c81fd8881be1b40463286` | `libfile_6ea524836424819188448a483fe738af` | 64,530 bytes |
| `HOLOS_Autonomous_Execution_Package.zip` | `/HOLOS/HOLOS_Autonomous_Execution_Package.zip` | `file_0000000055d481fd9d58ea0c5fec4c66` | `libfile_46a9799a3ec08191b506e953f1b823a8` | 21,652 bytes |

A checksum sidecar exists for the Model Initialization package:

- Sidecar: `/HOLOS/HOLOS_Model_Initialization_Package.zip.sha256`
- Sidecar listed size: 105 bytes
- Sidecar declares SHA-256: `48b0a93b9afe2cd316f2ef2a25d62910170a6b0a45ddbb616120e8a9c6a108ba`
- Sidecar target filename: `HOLOS_Model_Initialization_Package.zip`

**Checksum status:** this is a checksum value read from the sidecar text. It has not been independently verified against the ZIP bytes because raw-byte materialization remains denied. Do not label it a verified archive hash. No checksum sidecar for the Autonomous Execution package was found in the enumerated Library inventory.

The Library also contains separate research ZIPs (including the GfE reconstruction and Technical Investigation 002 packages), but their filenames and location do not establish that they contain animation rigs. They are not being treated as character-source candidates.

Raw-byte materialization was retried using the exact Library file IDs for both animation package candidates and the checksum sidecar, in both raw-file and text representations. The service returned the same authorization denial for all three. No ZIP contents were inspected.

### Updated recovery decision

The previous request to supply the two package files remains valid. If a transfer is possible, include the Model Initialization sidecar too; retain its original name and contents. On receipt, verify the archive against the declared checksum before opening it, then inventory without overwriting. If it does not match, preserve the archive and report the mismatch rather than silently regenerating the checksum.


## 2026-11-17 all-branch Git tree audit

The GitHub branch inventory was rechecked and all **20 currently listed branches** were inspected by commit SHA using recursive Git trees. No branch contains a Khaled or Kevin character scene, character rig script, skeletal resource, or 3D model source.

The scene/source assets present across the branches are production infrastructure and generic tests:

- `godot/test_scenes/adapter_test.tscn` and its adapter test script;
- `godot/scenes/episode_bookend_card.tscn` and its script;
- `godot/holos_shot_runner.gd`, `godot/holos_timeline.gd`, and `godot/episode_audio_transport.gd`;
- `godot/holos_scene_preflight.gd` on the later preflight branch.

The media files present on the production branches are the HOLOS theme, the 15-second test audio, approved character/key-art references, and the expression sheet. These are not rig scene sources.

This closes the GitHub-branch search for the currently listed branches. It does not inspect external Manus workspaces, local disks, or the contents of the two ZIP packages whose raw bytes remain inaccessible.


## 2026-11-17 contextual classification correction — Library package family

A later read-only inspection of the Library files adjacent to the two ZIPs materially changes how the filenames should be interpreted:

- /HOLOS/README.md is explicitly titled HOLOS Model Initialization — v0.1.0 and describes a finite Rep(Z2) / quantum-double stabilizer research benchmark, not an animation project. It lists model specification, lattice/stabilizer code, tests, validation logs and research manifests.
- /HOLOS/MODEL_SPECIFICATION.md describes a periodic square–octagon cellulation and quantum-information calculations. It contains no character-rig or Godot-animation scope.
- /HOLOS/S1_INITIALIZATION_REPORT.md and /HOLOS/EXECUTION_STATUS.md likewise describe the finite research benchmark and its scientific gates.
- /HOLOS/holos_final_conclusion.md is a research-programme execution conclusion, not an animation handoff.

**Reclassification:** the Library's HOLOS_Model_Initialization_Package.zip is strongly indicated by its surrounding package documentation to be a reality-research benchmark archive, not the missing Khaled/Kevin animation rig export. The similarly named HOLOS_Autonomous_Execution_Package.zip appears to belong to the same research package family, but its own archive contents remain uninspected. Because the ZIP bytes are still unavailable, neither archive's internal member list has been verified. Do not request or use these two archives as character-rig deliverables unless their contents are independently shown to contain the actual Godot character project.

The sidecar checksum remains only a declared value; it has not been verified against the archive bytes. This correction does not resolve the animation source handoff. The missing rig source must be sought in the original animation/Manus workspace or supplied as the actual Godot project export.
