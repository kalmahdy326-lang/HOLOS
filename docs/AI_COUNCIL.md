# HOLOS AI Council — Dual-Track Governance Constitution

**Programme:** HOLOS — The Fundamental Structure of Reality  
**Researcher and project author:** Khaled AL-MAHDY  
**Version:** 1.0  
**Status:** Proposed governance baseline on a review branch; adoption and merge require Khaled's approval.

## 1. Purpose and repository boundary

HOLOS is one programme with two connected but strictly separated repositories:

1. **Scientific research — [holos-reality](https://github.com/kalmahdy326-lang/holos-reality):** mathematical and computational investigations of information, entropy, quantum information, recovery maps, emergent structure and possible relationships to geometry and gravity.
2. **Animation and local production — [HOLOS](https://github.com/kalmahdy326-lang/HOLOS):** the 18+ animated science-fiction series, including Episode 1, The Moon Has Anger Issues, and the local-first Godot/Python/FFmpeg production pipeline.

The repositories may share high-level questions and project identity. They do not share evidence standards, code dependencies, asset stores or acceptance claims. A result may move between tracks only through an explicit, documented translation appropriate to its destination.

## 2. Shared constitution — non-negotiable rules

### 2.1 Fiction is not evidence

Events in Episode 1, including the fictional Moon, Lunar Interface, Regions A/B/C, the fourth signal, the Unknown Voice, character dialogue and all fictional incidents, must never be cited, logged or framed as scientific evidence in holos-reality.

Fiction may dramatize, simplify or take inspiration from research. Such use must be labelled as fiction or dramatization. A fictional event cannot validate a theorem, mechanism, physical correspondence, experiment or research hypothesis.

Scientific findings may inform future storytelling only after the research record is checked. Storytelling must not feed back into the research evidence ledger as support.

### 2.2 Prototypes are not production acceptance

A generic Godot test fixture, one successful render, a passing CI job, a screenshot, an unverified benchmark, or an uninspected ZIP archive does not satisfy character-rig integration or Milestone 6 offline production acceptance.

Status labels must distinguish:
- concept/reference asset;
- prototype;
- locally reproduced;
- CI-tested component;
- integrated character rig;
- two-character benchmark accepted;
- complete production workflow accepted offline.

A claim may advance only when its stated evidence gate has passed.

### 2.3 Inventory and backup before mutation

Before overwriting, renaming, moving, relocating, converting or otherwise mutating any original character reference PNG, WAV, transcript, phoneme timeline, Godot rig, ZIP archive or historical benchmark:

1. Record its original source location, name, byte size, provenance and version/date where known.
2. Compute a SHA-256 hash from the actual source bytes.
3. Create a separate backup and verify the copied bytes against the original hash.
4. Record the inventory and backup reports.
5. Perform work on a copy or branch; retain the original unchanged.

A filename, screenshot, Library listing, successful text extraction or file-size listing is not a SHA-256 hash. If raw bytes are inaccessible, record the hash as NOT COMPUTED and keep the mutation gate blocked. Never infer archive contents from a filename.

### 2.4 Single audio-derived transport clock

For dialogue animation, one central director/transport owns the audio player and publishes the authoritative playback position. Khaled and Kevin must sample that same audio-derived clock.

Character scripts must not maintain independent elapsed-time clocks driven by separate _process(delta) accumulators. The phoneme timeline is loaded and validated centrally, then exposed to both characters through a shared interface.

Pause, resume, seek, stop, restart and end-of-stream behaviour must be defined and tested. Encoded stream timing within 80 ms is a media acceptance check; it is not, by itself, proof of phoneme-level lip-sync accuracy. The approved phoneme tolerance must be separately defined and measured.

### 2.5 No paid dependencies; offline-first operation

The research and animation pipelines must remain executable with locally available tools and data. No paid APIs, subscriptions, AI credits, hosted inference, mandatory telemetry or cloud runtime dependencies may be introduced without Khaled's explicit authorization.

GitHub Actions may provide CI evidence, but CI does not replace the disconnected-network acceptance test on the target production machine. Any workflow that downloads dependencies during CI must not be described as proof that the local production runtime needs a network connection.

### 2.6 Human authority

Khaled AL-MAHDY is the final human authority for:
- accepting a research claim as ESTABLISHED in the programme record;
- accepting recovered Khaled/Kevin source rigs and their provenance;
- accepting character and two-character production benchmarks;
- approving asset migration or changes to canonical source material;
- approving offline production acceptance;
- approving merges to either repository's main branch.

AI Council roles provide analysis, drafts, tests and recommendations. They do not confer approval on themselves. No agent may merge to main, delete historical material, silently change milestone identifiers or override an explicit human decision.

## 3. Research evidence protocol

All scientific material belongs in holos-reality. Research records must:
- use the project's evidence labels: ESTABLISHED, ACTIVE RESEARCH, HOLOS HYPOTHESIS, SPECULATIVE, or REJECTED / REVISED;
- state definitions, units, conventions, assumptions and domain of validity;
- identify primary literature and reproducible calculations;
- separate theorem, numerical diagnostic, empirical result, interpretation and speculation;
- include counterexamples, failure conditions and known limitations;
- retain negative results and superseded reasoning with provenance.

A finite-dimensional quantum-information theorem or recovery result is not a derivation of spacetime geometry, gravity, Lorentzian structure or Einstein dynamics unless a separate, explicit, independently reviewed bridge is supplied. No analogy may be promoted as a derivation.

The fictional lunar anomaly and fourth signal are expressly outside the scientific evidence base.

## 4. Animation and asset protocol

All character, environment, screenplay, dialogue, sound, Godot, rendering and production-engine source of truth belongs in the HOLOS production repository or its approved, provenance-tracked asset store.

For each character, source recovery must include the complete Godot project context and transitive dependencies: project settings, addons, autoloads, primary scenes, inherited and tool scripts, textures, skeletons, animation resources, shaders, materials, fonts, audio and known-good benchmark configuration.

Do not copy only a visible scene file and assume it is self-contained. Do not replace an original rig with a newly generated stand-in and label it as recovered. Use wrappers/adapters around source rigs where practical, preserving the original files.

For Milestone 5.1:
- the corrected WAV must be checked against the approved four-line transcript before timeline creation or promotion;
- the unapproved leading word “But” must not be silently accepted;
- the incomplete fourth line must be resolved against the approved transcript;
- the accepted timeline must record the WAV and transcript hashes, sample rate, duration, version and provenance;
- one central director must load and own the timeline and provide the audio-derived transport position to both character rigs;
- no dialogue wording may be changed to fit an unapproved intermediate WhisperX timeline.

## 5. AI Council — role mandates

These are responsibility assignments for human-orchestrated review. They do not imply that the named external services are connected, installed, autonomous or able to access local files. Each role must work only from artifacts actually supplied to it.

| Agent / role | Dual-track mandate | Immediate priority | Prohibition |
|---|---|---|---|
| Perplexity — Auditor | Audit primary quantum-information literature in research; independently compare supplied approved transcript, corrected WAV and phoneme evidence in production. | Check for the unapproved leading “But”, completeness of all four lines and transcript/audio alignment once the files are available. | Never treat screenplay language or fictional events as physics literature or data. |
| GPT — Chief Architect | Architect research-ledger structure and research workflow interfaces; design the Godot/Python Milestone 5.1–6 production architecture. | Specify a single central audio-derived transport contract consumed by Khaled and Kevin. | Never infer that an unverified ZIP contains rigs or claim an unimplemented design is working code. |
| Claude — Math & Code Critic | Independently review proofs, SDP constraints/tolerances and research code; inspect GDScript/Python timing, determinism and race conditions. | Review the Godot frame-hook contract and phoneme timeline/transport synchronization tests. | Never approve code or mathematics without checking assumptions and deterministic or reproducible evidence appropriate to the claim. |
| Manus — Execution & Ops | Execute authorized repository tasks, manage review branches, run local inventories and available Godot/FFmpeg pipelines. | Read-only SHA-256 inventory of source packages and character references; recover and preserve the real source project; run documented acceptance steps. | Never merge to main, delete archives, mutate originals before verified backup, or invent local test results. |
| Grok — Red Team | Attack scientific overclaims and counterexamples; stress-test render recovery, manifests, audio/video synchronization and production/debug separation. | Test mid-shot crashes, corrupt or reordered manifests, symlink redirection, A/V drift above 80 ms and debug-overlay leakage. | Never accept a single successful render as offline production readiness. |
| Gemini — Synthesizer / Verifier | Synthesize research findings without collapsing evidence levels; independently inspect production output, FFprobe reports and hashes. | Maintain the fiction/research firewall and independently verify media timing and render manifests. | Never convert narrative resemblance into mathematical support or accept unverified reports as output evidence. |
| Meta AI — Interface & Communications | Design local interfaces for research-ledger navigation and the production status dashboard. | Prototype an offline status viewer for shot manifests, render/recovery health and audio-sync results. | Never add cloud dependencies, external telemetry or a required hosted service. |
| Vibe — Prototyping & Visualization | Prototype interactive mathematical visualizations for research; create visual look-development tests for the animated series. | Explore a non-humanoid visual treatment of the Moon as Regions A/B/C merging into synchronized geometric patterns and the post-credit geometric grid. | Never replace or overwrite approved character reference turnarounds with unapproved generated designs. |
| Muse — Exploratory Muse | Generate clearly labelled research questions and speculative narrative/comedic ideas. | Draft optional Khaled/ORBIT dry-humour beats or Episode 2 hooks around the fourth-signal timestamp. | Never inject speculative story ideas into scientific records or present them as evidence. |
| Khaled — Human authority | Set programme direction and adjudicate research, asset and production acceptance. | Review the council charter, authorize source migration and approve milestone acceptance only after evidence is available. | Approval cannot be delegated to an AI agent. |

## 6. Task-routing matrix

| Work item | Destination | Primary role | Independent review | Acceptance authority / evidence |
|---|---|---|---|---|
| Quantum-information literature and claims | holos-reality | Perplexity | Claude; Gemini | Khaled; primary sources, assumptions and evidence label |
| Proofs, CMI, recovery maps and SDP | holos-reality | Claude | GPT; Grok | Khaled; derivation, feasibility/residual checks, tests |
| Research-ledger architecture | holos-reality | GPT | Claude; Meta AI | Khaled; schema, provenance and offline tests |
| Fictional screenplay and character dialogue | HOLOS | Muse | Perplexity only for factual source-checking; GPT for continuity | Khaled; approved screenplay revision |
| WAV/transcript/phoneme audit | HOLOS | Perplexity | Claude; Manus for file hashes | Khaled; approved transcript, verified WAV, hashes and aligned four-line timeline |
| Godot central transport and character adapters | HOLOS | GPT | Claude; Grok | Khaled; synchronized deterministic tests on real rigs |
| Rig-source recovery and preservation | HOLOS | Manus | Grok; Gemini | Khaled; complete inventory, SHA-256, verified backup and provenance |
| Character look development | HOLOS | Vibe | GPT; Khaled | Khaled; approved reference comparison; originals preserved |
| Local dashboards and status interfaces | HOLOS | Meta AI | GPT; Claude | Khaled; offline/local data-only operation and tests |
| Render, assembly and release verification | HOLOS | Manus | Grok; Gemini | Khaled; actual-rig renders, clean production frames, FFprobe and offline acceptance |
| Cross-track concept transfer | Destination-specific review only | GPT | Claude and relevant track auditor | Khaled; written mapping, fictionalization label or scientific bridge |

### Routing rule

A task is routed to the repository that owns its source of truth. Cross-track work requires an explicit handoff note identifying what is transferred, what is not transferred, its evidence status, and the receiving repository's review gate. Do not copy scientific dependencies into the animation engine or animation assets into the research evidence tree merely to simplify access.

## 7. Immediate execution sequence — Milestones 5.1 and 6

### Gate 0 — Source access and preservation
- Confirm the exact local project root and the source handoff version.
- Inventory the two initialization/execution ZIP packages and the three character-reference PNGs by source path, size and SHA-256.
- Create and verify immutable backups before migration.
- Inspect ZIP contents without extracting over or altering originals.
- Mirror reference PNGs only as byte-identical copies with recorded source hashes and approval.
- If source bytes cannot be retrieved or hashed, record the blocker; do not claim inventory or copy completion.

### Gate 1 — Audio/transcript approval
- Obtain the corrected WAV and the approved four-line transcript.
- Verify audio content and line completeness; explicitly check removal of the unapproved leading “But”.
- Compare the actual audio with the approved wording; do not promote the intermediate WhisperX timeline as-is.
- Generate/reconcile the phoneme timeline, tie it to WAV and transcript SHA-256 values, and obtain review.
- Lock the timeline only after Khaled's approval.

### Gate 2 — Central transport refactor
- Inspect and back up the actual production scene, director and character scripts.
- Correct the production scene's obsolete WAV reference only after Gate 1.
- Move timeline loading/validation to the central director.
- Expose one audio-derived playback position; make both character scripts read it.
- Remove independent character/director elapsed-time accumulators.
- Test play, pause, resume, seek, restart, stop and end-of-stream behaviour.
- Keep sample/phoneme accuracy distinct from the 80 ms encoded stream acceptance tolerance.

### Gate 3 — Character and interaction benchmark
- Integrate only recovered original Khaled and Kevin rigs with all dependencies.
- Pass each character's load, idle, dialogue, repeat-render and debug/production tests.
- Render the two-character benchmark in production mode.
- Inspect final frames for skeletons, debug labels, collision shapes, timing overlays or other diagnostics.
- Confirm the audio transport position and phoneme events agree for both characters.

### Gate 4 — Media and offline acceptance
- Assemble with FFmpeg and validate with FFprobe.
- Require audio/video stream start offset and duration difference to remain within the configured 80 ms limit.
- Verify frame count, dimensions, frame hashes and manifest integrity.
- Stress-test interrupted rendering, recovery, corrupt manifests and symlink paths.
- Disable network access on the target machine and perform the complete accepted workflow using local dependencies.
- Record logs, versions, configuration, hashes and results. Khaled accepts or rejects the milestone.

## 8. Production-repository scope

This copy is authoritative for animation, screenplay, audio, character assets, Godot adapters, local rendering, FFmpeg/FFprobe and production acceptance. It links to the shared scientific governance but does not make production code or fictional material part of the research evidence base.

## 9. Current known blockers and truthful status

The following blockers must remain visible until source evidence resolves them:
- The production GitHub repository's current tree does not contain the original Khaled/Kevin Godot rig scenes and their transitive dependencies.
- The two located ZIP packages are not inspected; their contents must not be inferred from names.
- Character reference PNGs are concept/reference assets, not production rigs. A visual inspection or Library listing is not a byte hash or a successful migration.
- The corrected Milestone 5.1 WAV and approved four-line transcript must be supplied and verified before timeline promotion.
- The supplied local path /home/ubuntu/holos_rigging is not automatically accessible from the GitHub repository.
- A generic adapter CI pass is not proof of original-rig integration or offline production acceptance.

## 10. Change control and records

- AI-prepared repository changes belong on review branches or pull requests.
- Do not merge to main without Khaled's explicit approval.
- Preserve milestone identifiers and historical records; add dated corrections rather than silently rewriting history.
- Every execution report must distinguish planned, attempted, blocked, tested and accepted.
- Never claim a local test was run when only a GitHub file inspection or CI result exists.
- Retain failed results, negative tests and recovery artifacts according to the preservation rules.

---

**Governing principle:** We are not trying to make our theory right. We are trying to find out what is right.

**Programme author and human approval authority:** Khaled AL-MAHDY
