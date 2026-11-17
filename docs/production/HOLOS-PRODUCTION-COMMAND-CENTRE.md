# HOLOS Production Command Centre

**Project:** HOLOS  
**Project author:** Khaled AL-MAHDY  
**Purpose:** Persistent, evidence-led control centre for producing the complete, high-quality animated series.  
**Status:** Initial production-control framework; not evidence that production milestones have been completed.

## The non-negotiable destination

HOLOS is to become a polished, fully animated television series at a high professional standard. Teletoon-quality animation is a reference point, not a ceiling. The finished work must feel like a real television production, not a slideshow, moving-poster sequence, motion comic, or animatic.

The quality target includes expressive acting, fluid character movement, convincing facial performance and lip-sync, consistent character models, designed environments, cinematic staging and camera work, deliberate editing, sound design, and technically reliable final renders.

An animatic is a planning and review tool only. It is never an acceptable substitute for the finished animated series.

## How this command centre is used

This directory is the durable source of truth for production planning and progress. At the beginning of each new work session:

1. Read this file first.
2. Read [the master production roadmap](holos-master-production-roadmap.md).
3. Read [the production ledger](holos-production-ledger.md).
4. Read the relevant existing engineering, artwork, screenplay, audio, and provenance documents linked below.
5. Inspect the current repository branch and actual files before making claims about their state.
6. Resume the earliest unblocked, highest-priority task. Do not restart completed work or silently change prior decisions.
7. Record every meaningful result, evidence link, commit, blocker, decision request, and next action in the ledger.

At the end of a work session, update the ledger with what was actually done and the exact next action. Never mark a task complete based only on a plan, prompt, or unverified report.

## Production truth rules

Every important item must be labelled as one of:

- **VERIFIED** — directly inspected or tested, with evidence.
- **REPORTED** — stated by a person or external agent but not independently checked.
- **PROPOSED** — a suggested design or implementation, not approved canon.
- **BLOCKED** — cannot proceed until a named prerequisite is satisfied.
- **NOT TESTED** — implementation or artifact exists, but acceptance has not been performed.
- **ACCEPTED** — the project author has explicitly approved the result against its stated criteria.

Never turn REPORTED into VERIFIED by repetition. Never describe an animatic, placeholder, test scene, still image, prototype rig, or technical render test as a finished animated scene.

## Source and canon protection

- Khaled is Character B. Kevin is Character A.
- ORBIT and the Moon are separate identities.
- Do not invent the Moon's origin, appearance, lore, or unapproved dialogue.
- Do not invent, rewrite, or silently normalize screenplay or storyboard content.
- Preserve all original assets and their provenance. Work on copies or derived files.
- The 65-panel storyboard is text-only unless image panels are recovered and verified.
- Do not create substitute character or environment artwork and present it as recovered source material.
- Do not select, replace, remix, or declare a soundtrack approved without explicit project-author approval.
- No paid software, paid services, or AI-generation credits without explicit authorization.
- Keep the animation project separate from the HOLOS reality-research repository.

## Repository and external asset boundary

The GitHub repository does not necessarily contain all project materials. The original screenplay DOCX, reference images, ZIP archives, rigs, source audio, and other materials may exist in the Project-space Library or other authorized handoff locations.

Before asset-dependent work, confirm that the working agent can access the relevant Library sources. Inspect both ZIP archives, including nested contents, rather than assuming what they contain. If access is unavailable, record the blocker and continue only with tasks that can be completed from verified repository sources.

For each recovered original, record filename, source location, byte size, SHA-256, inspection status, and whether it is safe to use. Do not overwrite originals.

## Required production disciplines

1. **Asset recovery and provenance:** find, inspect, hash, catalogue, and preserve original materials.
2. **Canon reconciliation:** compare source screenplay, character references, storyboard, audio, and approved decisions. Escalate ambiguity rather than inventing answers.
3. **Character performance:** recover and validate the actual character rigs; implement expressive body, face, eye, mouth, and acting systems.
4. **Environment and visual development:** create production-ready locations and reusable assets consistent with approved art direction.
5. **Shot and scene production:** construct real scenes with staging, blocking, camera, lighting, effects, and continuity.
6. **Dialogue and audio:** connect approved recordings to a shared playback clock, speaker identity, phoneme/viseme timing, facial performance, sound effects, and approved music.
7. **Rendering and editorial:** produce reproducible shots, edit complete sequences, mix sound, and render review and delivery masters.
8. **Quality assurance:** inspect actual playback, visual performance, continuity, sync, image integrity, and technical specifications.
9. **Delivery and archival:** package editable projects, dependencies, renders, manifests, checksums, and reproducible instructions.

## Existing project references

Use the current versions in the repository and verify branch availability before relying on them:

- [Milestone 6 implementation reference](../engineering/milestone-6-implementation-reference.md)
- [Episode JSON v1 reference](../engineering/episode-config-v1-reference.md)
- [Milestone 6 next work package](../engineering/milestone-6-next-work-package.md)
- [Character animation and dialogue integration roadmap](../engineering/character-animation-and-dialogue-integration-roadmap.md)
- [Offline acceptance and dependency policy](../engineering/offline-acceptance-and-dependency-policy.md)
- [Visual art direction bible](../artwork/holos-visual-art-direction-bible.md)
- [Character art and model-sheet specification](../artwork/holos-character-art-and-model-sheet-spec.md)
- [Artwork provenance and review workflow](../artwork/holos-artwork-asset-provenance-and-review-workflow.md)
- [Episode 1 narrative and research boundary](episode1-narrative-and-research-boundary.md)
- [Intro v001 verification handoff](intro-v001-verification-handoff.md)

Some references may exist only on unmerged pull-request branches. Do not assume they are on the default branch. Record the exact branch or commit used.

## How the assistant should continue work

When the project author says "continue HOLOS production", "resume the command centre", or similar:

- Re-read the command centre, roadmap, and ledger from GitHub.
- Inspect the current state of relevant code and assets; do not rely on stale summaries.
- Choose the next useful task that can be completed safely with available tools.
- Prefer concrete, testable deliverables over another layer of generic planning.
- Make changes on a dedicated branch, preserve originals, run relevant tests, and record evidence.
- Open or update a draft pull request for review. Do not merge without explicit approval.
- If a task requires Manus, Library access, local rendering, or another unavailable environment, prepare a precise handoff and label the dependency. Do not claim to have performed that external work.
- Do not claim autonomous overnight activity or background execution. Work continues when an active session or authorized scheduled workflow runs.

## Definition of success

The command centre succeeds when it reliably guides the project from the current incomplete repository and recovered source assets to a complete, editable, reproducible, professionally animated series, with every scene and final delivery supported by inspectable evidence and project-author acceptance.
