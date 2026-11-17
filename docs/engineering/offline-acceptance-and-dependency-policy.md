# HOLOS — Offline Acceptance and Dependency Independence Policy

**Project author:** Khaled AL-MAHDY  
**Purpose:** Define what it means for the HOLOS production toolchain to be genuinely independent, local-first and reproducible.

## 1. Independence is an enforceable production property

A local-first pipeline must not merely prefer local tools. A clean production run must be possible without:
- external AI inference or generation services;
- subscriptions, metered APIs or cloud rendering;
- network authentication to launch the editor, render, assemble or validate;
- runtime downloads of plugins, fonts, models, packages or media;
- remote asset URLs or network-mounted project dependencies.

Manus, ChatGPT and other assistants may be optional development aids. They are not production runtime dependencies.

No new paid service, AI credit, subscription or hosted dependency may be introduced without explicit creator authorization.

## 2. Dependency policy

Every dependency must be recorded with:
- name and purpose;
- exact version/build;
- source/distribution;
- license and redistribution constraints;
- executable or package path;
- checksum where practical;
- whether needed at authoring, rendering, assembly, validation or packaging time;
- whether the dependency is available in the offline installation bundle.

Separate:
1. **Core runtime:** Godot, Python and required Python standard-library/runtime components, FFmpeg/FFprobe, GPU/display drivers and OS libraries.
2. **Project resources:** Godot scenes, scripts, imported resources, fonts, shaders, textures, audio and configuration.
3. **Development/test tools:** linters, test runners and diagnostic utilities not required to run a finished render.
4. **Optional assistants:** never required for runtime.

Pin exact versions for validated production builds. A broad requirement such as “Godot 4.x” is not a reproducibility lock.

Do not silently install or update dependencies during an offline render. Preflight should fail with an actionable missing-dependency report.

## 3. Disconnected-network acceptance test

A pass requires a clean, documented test on the target production machine with network access disabled at the operating-system/network layer. A CI run, airplane-mode screenshot, or successful run while a cached service remains reachable is not sufficient by itself.

### Test preparation
- Record OS/version, machine identifier (non-secret), CPU/GPU, driver, RAM and free disk.
- Record Godot, Python, FFmpeg and FFprobe exact versions and executable hashes.
- Inventory all project files and external resources.
- Create and verify a source backup.
- Prepare an offline dependency bundle and its checksums.
- Record network-disconnection method and test start/end times.
- Start from a clean output directory with no previous successful render to reuse.

### Required test sequence
1. Disable network access; verify DNS and outbound network are unavailable using approved local diagnostics.
2. Start Godot and open/import the project without network access.
3. Run Python config validation and preflight.
4. Load each original character rig and all required dependencies.
5. Render one representative shot for Khaled and one for Kevin.
6. Render a two-character interaction shot after both individual adapters pass.
7. Run a multi-shot batch with at least three shots.
8. Interrupt one run deliberately at a documented safe point; restart and verify completed shots are hash-checked and skipped while partial output is archived and retried.
9. Assemble a video with the configured original audio, plus a separate silent-preview case.
10. Run FFprobe validation and a full-file decode.
11. Run source inventory, backup and restore-to-new-directory checks.
12. Repeat the same configuration and compare outputs for bit identity or documented visual/temporal equivalence.
13. Inspect logs and process/network evidence for unexpected external calls.

### Pass criteria

All must be true:
- Every required step completes with the network disabled.
- No external service, cloud account, API key, subscription or AI service is contacted or required.
- All resources resolve from local project paths or the documented offline dependency bundle.
- Both original character rigs load and render; a generic adapter fixture does not count.
- At least three configured shots render in order and assemble successfully.
- The interrupted batch recovers without losing or silently overwriting completed work.
- Final video passes configured metadata validation and full decode.
- Original audio inputs remain byte-identical.
- Backup and restore produce verified copies without overwriting the working project.
- Repeated output is bit-identical or its nondeterminism is measured, explained and accepted.
- Logs, manifests, tool versions, hashes and a signed-off test report are retained.

Any missing step, network dependency, unverified original rig, missing resource or unexplained nondeterminism is a FAIL or BLOCKED result, not a partial pass. Report sub-results individually.

## 4. Git, large binary files and asset storage

Git is authoritative for source code, text documentation, small configuration and reviewable manifests. Large binary assets require an explicit policy:
- Use Git LFS for large source media when the repository's LFS quota, access and object retention are understood.
- Keep generated frame sequences, temporary renders, caches, editor imports and local backups out of ordinary Git history.
- Store reproducible render outputs as versioned release artifacts or separately managed production packages, with checksums and provenance.
- Never commit credentials, tokens or private account data.
- Do not assume that a Git LFS pointer proves the binary object can be retrieved. Verify the actual bytes and SHA-256.
- Never rewrite canonical source binaries merely to simplify rendering.

For each source/derivative pair, preserve source hash, derivative hash, tool version, transformation settings and approval state.

## 5. Failure and fallback policy

| Failure | Required response |
|---|---|
| Godot missing or crashes | Stop the affected job; preserve logs and partial output; do not switch to a cloud renderer |
| FFmpeg/FFprobe missing | Stop assembly/validation; retain rendered shots; repair the local toolchain before continuing |
| Python dependency missing | Report exact package/version; install only from the approved offline bundle |
| GPU/driver failure | Capture environment and logs; retry only under a documented supported local rendering configuration |
| Disk space low | Stop before unsafe writes; preserve completed outputs and report required capacity |
| Corrupt source asset | Quarantine a copy for diagnosis; preserve original bytes and checksum |
| Power loss/reboot | Resume from the manifest; verify completed frame hashes; archive partial shot output |
| Offline resource unavailable | Mark BLOCKED; do not substitute an unapproved asset or external service |

Fallback means a documented local alternative with equivalent acceptance evidence. It does not mean silently lowering quality, replacing original rigs, using placeholder characters or introducing paid services.

## 6. Backups and restoration

Backups must be non-overwriting, timestamped and separate from source directories. Each backup manifest must identify:
- source project root and inventory digest;
- relative file paths, sizes and SHA-256 values;
- backup destination and creation timestamp;
- per-file copy verification;
- skipped/excluded paths and reasons;
- final status.

Restoration must target a new directory. The current implementation explicitly restores source files to a new snapshot and does not overwrite the working project or reconstruct Git metadata/generated output. Keep this boundary visible in user-facing instructions.

A backup is valid only if the source inventory is complete and copied files re-hash to the same values.

## 7. Current status and next evidence

The Milestone 6 documentation records inventory, backup/restore, ordered batch recovery, adapter rendering and media assembly code. It also explicitly says the original Khaled/Kevin rigs are not yet integrated and the target-machine offline acceptance test has not been performed.

Therefore:
- Local-first architecture: designed and partially implemented.
- Disconnected-network acceptance: NOT VERIFIED.
- Full production independence: NOT YET ACCEPTED.
- Original character rig integration: BLOCKED pending source handoff.

Do not upgrade these statuses without new test evidence.
