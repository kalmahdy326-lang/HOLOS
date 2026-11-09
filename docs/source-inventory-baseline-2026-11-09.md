# Source inventory baseline — 2026-11-09

**Project author:** Khaled AL-MAHDY  
**Repository:** \`kalmahdy326-lang/HOLOS\`  
**Branch:** \`main\`  
**Inventory implementation commit:** \`461a289d\`  
**Verification:** GitHub Actions run #99 — Python/media and Godot jobs passed

## Result

The read-only inventory command completed against the GitHub Actions checkout:

| Measure | Result |
|---|---:|
| Status | Complete |
| Regular files inventoried | 36 |
| Total inventoried size | 196,252 bytes |
| Skipped entries | 3 |
| Traversal errors | 0 |
| Inventory algorithm | SHA-256 |

**Aggregate inventory SHA-256**

\`\`\`text
01172e1debbd39611f2e07788a0c975ff51583c203345e56f16ad25f566f443f
\`\`\`

## Files by category

| Category | Count |
|---|---:|
| Documentation | 4 |
| Examples | 4 |
| Godot project | 4 |
| Production code | 11 |
| Project configuration | 4 |
| Tests | 9 |
| **Total** | **36** |

## Godot project contents at this baseline

The repository contains:

- \`godot/project.godot\`
- \`godot/holos_shot_runner.gd\`
- \`godot/test_scenes/adapter_test.gd\`
- \`godot/test_scenes/adapter_test.tscn\`

These are the generic rendering adapter and its test fixture. The inventory
contains no character asset directory and no Khaled or Kevin rig scene files.
Therefore, the CI-rendered fixture must not be presented as validation of either
character rig.

## Interpretation and limits

This is a baseline of the repository checkout used by CI at commit
\`461a289d\`. It is not an inventory of other local folders, external drives,
older ZIP archives, or the target production workstation. The inventory
implementation intentionally excludes Git metadata, generated output,
dependency/cache directories, symlinks, and common secret-file names.

Run the inventory command in the actual production project checkout before
moving or backing up those external character assets. The report can then be
used directly by the verified backup command from that same project root.
