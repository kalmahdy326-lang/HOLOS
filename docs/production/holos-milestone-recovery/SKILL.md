---
name: holos-milestone-recovery
description: Recover, verify and hand off HOLOS animation milestones through GitHub, with credential-safe CI diagnostics, audio/timeline provenance checks, and Godot logic-versus-pixel validation. Use for HOLOS Milestone 5.1 handoffs, PR/Actions recovery, WAV/timeline verification, or CI visual lip-sync gates.
---

# HOLOS Milestone Recovery

Use this skill to recover a HOLOS Milestone 5.1 handoff without overwriting source audio, changing `main`, or claiming production acceptance before evidence is available.

## Non-destructive operating rules

- Preserve the approved transcript exactly. Record ASR spelling normalizations explicitly; do not silently rewrite dialogue.
- Preserve the source MP3 and existing Godot project assets.
- Work on a feature branch or review checkout. Do not commit directly to `main`.
- Treat turn boundaries, word boundaries and phoneme boundaries as different evidence types. Never infer phoneme timings from turn boundaries.
- Keep derived WAV provenance variants separate until source hash, extraction command, format and duration are reconciled.
- Do not use or print GitHub tokens. Do not start authentication without the user completing the login flow.
- Do not merge a draft PR. Report unavailable private-repository data as unavailable rather than guessing.

## Workflow

1. **Establish access.** Run `scripts/check_run_status.sh` only after the user authenticates `gh` with an account that can read the private repository. Confirm repository, PR and run visibility before inspecting diffs.
2. **Inventory the PR.** List open PRs, workflows, branch runs and commits. Compare the feature branch against `main`; inspect workflow YAML and all changed files.
3. **Verify audio provenance.** Confirm the source MP3 SHA-256. Record derived WAV hashes, extraction commands, sample rate, channel count, bit depth and duration. Keep differing WAVs as separate variants.
4. **Validate the transcript.** Confirm speaker order, opening word, absence of unapproved leading words and completion of the final line. Preserve approved spelling while documenting accepted ASR normalizations.
5. **Validate the timeline.** Require a versioned flat event schema, supported visemes, positive durations, chronological ordering, speaker ownership and a clear absolute-versus-relative timebase.
6. **Separate CI gates.** Treat `--headless` as script/scene/timeline logic validation only. Treat pixel-producing visual validation as a separate gate requiring a real or virtual display context.
7. **Inspect Godot visual evidence.** Read `references/godot-offscreen-ci.md` before changing a workflow. Confirm the workflow actually captures frames or movie output; a step named “offscreen render” is not sufficient.
8. **Decide merge readiness.** Require completed CI, successful logic checks, successful pixel-producing render, visual inspection, repository-relative paths, selected WAV provenance and no unintended production-file changes before moving a draft PR toward merge.

## CI script

Run:

```bash
./scripts/check_run_status.sh
```

Validate configuration without contacting GitHub:

```bash
./scripts/check_run_status.sh --dry-run
```

Dry-run mode checks non-empty configuration, prints the exact read-only commands that would run, and performs no authentication, repository access, network request or write.

Optional variables:

```bash
HOLOS_REPO=owner/repo HOLOS_PR=6 HOLOS_RUN_ID=123456789 ./scripts/check_run_status.sh
```

The script is read-only. It checks authentication, repository visibility, PR metadata, run metadata, job conclusions, failed logs and recent branch runs. It does not call `gh auth login`, push, commit, rerun or merge.

## Godot acceptance distinction

- `godot --headless`: import, script parsing, timeline self-tests and deterministic logic only.
- `xvfb-run` plus a normal Godot window, Movie Writer, or a capture autoload: pixel-producing CI evidence.
- Manual/desktop capture: acceptable fallback when Linux virtual display is unavailable, but must be recorded as a separate gate.

## Required report fields

Report the repository/account access result, PR and branch, exact commits/files changed, source and derived audio hashes, alignment method and timebase, transcript checks, timeline schema checks, CI run/job conclusions, render-capture method, visual inspection result, remaining blockers and merge decision.

Read the Godot reference only when visual CI configuration is needed:

- `references/godot-offscreen-ci.md`
