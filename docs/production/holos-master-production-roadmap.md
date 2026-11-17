# HOLOS Master Production Roadmap

This roadmap defines the route to a high-quality, fully animated television series. It is a production dependency map, not a claim that any stage is complete. Reassess statuses against the repository and actual artifacts at every session.

## North-star quality bar

The finished series must deliver professional television-cartoon quality or higher: expressive character acting, fluid movement, controlled timing, strong posing and silhouettes, readable staging, detailed and coherent environments, intentional camera language, consistent art direction, convincing facial animation and lip-sync, polished editing, designed sound, and reliable delivery masters.

Do not optimize for the number of shots rendered at the expense of quality. A small, finished, approved sequence is more valuable than a large collection of weak placeholders.

## Gate 0 — Access, source recovery, and provenance

**Objective:** Establish what actually exists and make all authorized source material accessible.

Tasks:
- Confirm GitHub branch, pull-request, and asset state.
- Confirm Project-space Library access.
- Recover the authoritative screenplay DOCX and compare it with the text extraction.
- Recover all three character-reference PNGs.
- Inspect both ZIP archives completely, including nested archives.
- Locate original character rigs, native project files, textures, skeletons, animation actions, audio, and environment assets.
- Record SHA-256, size, source, and inspection status for every original.
- Create a non-destructive asset manifest and backup.

**Exit gate:** All available sources are inventoried; missing sources and access blockers are explicit; source authority and provenance are clear. No asset is described as recovered without inspection.

## Gate 1 — Canon, screenplay, and storyboard lock

**Objective:** Establish exactly what the episode is meant to contain before building shots.

Tasks:
- Compare the original screenplay DOCX against the repository extraction.
- Reconcile all 65 storyboard IDs and their order against the authoritative screenplay.
- Record missing, altered, unsupported, and ambiguous material for author decision.
- Confirm scene boundaries, cast, dialogue, sound cues, timing evidence, and continuity.
- Keep text-only storyboard descriptions distinct from actual panel artwork.
- Obtain project-author decisions on unresolved story and audio questions.

**Exit gate:** A traceable, author-reviewed episode source package exists. No invented dialogue, scene, character, or timing is used to conceal a gap.

## Gate 2 — Character and visual development

**Objective:** Establish production-ready, consistent character assets and visual language.

Tasks:
- Inspect and validate the original Khaled and Kevin rigs and source projects.
- Preserve native rigs and create adapters/wrappers rather than destructive substitutions.
- Establish model sheets, turnarounds, proportions, facial controls, eye controls, mouth shapes, hands, deformation rules, and costume/prop continuity.
- Define reusable body mechanics and acting libraries.
- Validate silhouettes, posing, expressions, and consistency across camera angles.
- Develop the lunar research station and other approved environments as reusable production assets.
- Establish lighting, materials, effects, compositing, and color pipeline.

**Exit gate:** Each principal character passes a repeatable animation benchmark using the actual approved design and rig. Environments and visual assets are approved, reusable, and traceable.

## Gate 3 — Animation and render pipeline

**Objective:** Turn the existing engine infrastructure into a dependable production pipeline.

Tasks:
- Inspect the Python engine, Godot runner, timeline system, adapters, configuration validator, and test scenes.
- Reconcile the actual episode JSON v1 schema with runtime requirements.
- Implement explicit scene paths, shot timing, camera, character, dialogue, audio, and render settings only where supported by a versioned contract.
- Add robust preflight validation and useful error reporting.
- Add deterministic frame-state evaluation and repeatable shot rendering.
- Strengthen media validation: codec, pixel format, dimensions, frame rate, duration, decoded frame count, full-file decode, audio stream properties, A/V synchronization, and visual corruption checks.
- Ensure incomplete renders are safely recoverable and completed outputs are integrity-checked.
- Validate the target Godot version and disconnected-network behavior on the actual production machine.

**Exit gate:** A clean, reproducible test episode renders from configuration through the existing engine, passes automated checks, and can be visually inspected.

## Gate 4 — Performance and dialogue

**Objective:** Deliver believable character performances, not merely moving rigs.

Tasks:
- Verify the authoritative audio sources and approved speaker identities.
- Verify transcript and alignment provenance; distinguish word alignment from true phoneme alignment.
- Implement one shared audio clock for dialogue, mouth shapes, facial actions, and body performance.
- Map phonemes to a validated viseme vocabulary and test coarticulation.
- Build listening, speaking, interruption, reaction, gaze, blink, breath, and turn-taking behaviors.
- Create acting passes for every speaking and non-speaking character.
- Validate lip-sync visually against the actual approved audio.
- Add approved sound effects and music only under the project's authorization rules.

**Exit gate:** Dialogue scenes pass audio/visual sync review, speaker identity review, acting review, and continuity review.

## Gate 5 — Environment, layout, and shot production

**Objective:** Build complete scenes with deliberate cinematic composition.

Tasks:
- Create reusable sets, props, lighting rigs, and environment effects.
- Define camera coverage, lens/framing conventions, movement, focus, and continuity.
- Block scenes with correct character positions, eyelines, entrances, exits, and spatial relationships.
- Replace blocking with final character animation and approved assets.
- Add secondary motion, interaction, environmental motion, particles, and effects where motivated.
- Maintain consistent screen direction, geography, timing, and performance between shots.
- Review every shot at intended playback speed and in sequence.

**Exit gate:** Every required shot has a complete, approved visual performance and no placeholder is being passed off as final work.

## Gate 6 — Editorial, sound, and finishing

**Objective:** Turn approved shots into a coherent finished episode.

Tasks:
- Assemble shots in verified screenplay/storyboard order.
- Review pacing, transitions, scene rhythm, and comedic/dramatic timing.
- Mix dialogue, ambience, effects, and explicitly approved music.
- Check dialogue intelligibility and consistent loudness.
- Perform color, compositing, cleanup, titles, credits, and final audio/video finishing.
- Review the entire episode from beginning to end, not only isolated shots.

**Exit gate:** Full-episode review copy is complete and passes editorial, visual, audio, continuity, and technical review.

## Gate 7 — Delivery and archive

**Objective:** Deliver a reproducible, editable, high-quality episode and preserve its production record.

Tasks:
- Render the agreed delivery format and a review copy.
- Include editable Godot project, source assets or authorized references, episode configuration, scripts, dependencies, manifests, and build instructions.
- Record checksums for all final deliverables.
- Verify full-file decoding and playback on a clean environment.
- Verify project opens and renders without relying on undocumented local state.
- Archive approvals, QC reports, known limitations, and exact source revisions.

**Exit gate:** Project author accepts the episode and the full package is independently reproducible.

## Work priority rules

1. Unblock source access and provenance before asset-dependent production.
2. Resolve screenplay and canon discrepancies before final scene animation.
3. Validate actual character rigs before building performance around assumptions.
4. Improve the engine only to support concrete production needs and test each change.
5. Complete a representative high-quality scene as a vertical slice before scaling to all scenes.
6. Use the vertical slice to calibrate art, acting, animation, rendering, audio, and review standards.
7. Scale only after the author accepts the benchmark.
8. Keep quality gates intact; do not relabel incomplete work to move milestones forward.

## Vertical-slice requirement

Before producing the whole episode, select one representative scene with the project author or from the verified screenplay. It should exercise:
- Two-character interaction where available.
- Dialogue and listening performance.
- Facial expression and lip-sync.
- Character movement and spatial continuity.
- Environment, camera, lighting, and effects.
- Audio synchronization and final render.

The vertical slice must be finished to the target quality and explicitly reviewed. It becomes the measurable reference for the rest of the production.

## Status protocol

Use the production ledger for live status. Each task must identify its owner, prerequisite, evidence, status, and next action. Never infer acceptance from code existence or successful rendering alone.
