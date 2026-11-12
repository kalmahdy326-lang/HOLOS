# HOLOS project hub and Project-space consolidation register

**Researcher and project author:** Khaled AL-MAHDY  
**Programme:** HOLOS  
**Record date:** 11 November 2026 (Pacific); CI records may carry a 12 November UTC date  
**Purpose:** establish one navigable project record across the HOLOS research, manuscript, creative-production and local-engine work without conflating their evidence or software requirements.

## 1. Consolidation decision

HOLOS has two active GitHub repositories with different technical responsibilities. They are connected as one programme but are not merged into one dependency tree.

| Layer | Canonical repository | Responsibility |
|---|---|---|
| Project hub, animation and local production | [kalmahdy326-lang/HOLOS](https://github.com/kalmahdy326-lang/HOLOS) | Character/scene production, Godot, Python orchestration, FFmpeg/FFprobe, assets, episode workflow, preservation and offline acceptance |
| Scientific research | [kalmahdy326-lang/holos-reality](https://github.com/kalmahdy326-lang/holos-reality) | Research charter, evidence ledger, mathematical investigations, literature, experiments, tests and research CI |

This separation is intentional. The production engine must remain locally operable and dependency-light; the research programme has its own scientific dependencies and test gates. The root README of this repository is the entry point. Each repository links back to the other.

**Do not merge repositories by copying files over one another.** Any later monorepo migration must preserve both Git histories, source assets, file hashes, test workflows and project boundaries, and must be separately reviewed.

## 2. Programme identity and methodological constitution

HOLOS asks:

> What is the underlying mathematical structure of reality, and can phenomena we observe — matter, energy, gravity, entropy, information, space and time — be understood or derived from a more fundamental set of relationships?

The governing rule is:

> We are not trying to make our theory right. We are trying to find out what is right.

The programme must distinguish:
- **Established:** theorem, replicated result or accepted finding within a stated domain.
- **Active inquiry:** unresolved question with credible competing accounts.
- **HOLOS interpretation:** proposed organization or interpretation of known material.
- **Speculative / metaphysical:** possibility not yet operationalized or supported.
- **Rejected / revised:** a route that failed or was narrowed; retained in the record.

No analogy is a derivation. A cross-domain connection requires an explicit mapping of objects, variables, transformations, units, mechanisms and preserved quantities. Negative results and failed hypotheses remain recorded.

## 3. Scientific research layer

The scientific repository contains:
- Investigations **INV-001 through INV-014**, including local/global information, gravity–entropy–information comparisons, quantum correlations, decoherence, finite-dimensional CMI/Markov recovery, nested-region buffers, noise, target-informed and target-independent recovery, noisy and retained/discarded side information, non-orthogonal quantum clues, and pure-state approximate conversion.
- A separate **boundary-mathematics** line with BM-001 onward and its founding paper. Its definitions and claims remain subject to their own proof and counterexample gates.
- Technical notes on nested CMI recovery, thermodynamic relaxation, Newtonian gradient-flow reconstruction, comparative gravity/entropy work, channel capacities and finite-block primitives.
- Reproducible experiments, unit tests, references, literature reports, master programme integration and GitHub Actions workflows.

### 3.1 Current scientific status

- INV-014 is closed for the specified **pure two-state conversion** problem. Its exact optimum is analytic; the SDP and 101 × 101 surface are verification tools, not the proof.
- The arbitrary mixed-qubit state-conversion problem remains open.
- The finite-dimensional quantum-information results do **not** derive geometry, gravity, Lorentzian spacetime or Einstein dynamics.
- The proposed gravity–entropy–information invariant remains an open research target. Existing results from Jacobson, entanglement equilibrium, holography and generalized/relative-entropy gravity models must be compared on their actual assumptions; they are not interchangeable.
- Workstream B (gravitational entropy and information metrics) is the core physics bridge investigation. No finite-dimensional recovery theorem is to be advertised as a gravitational result without a separate, independently reviewed bridge.
- Exploratory collective-learning, morphic-resonance, animal-learning, magnetosensation and quantum-biology topics belong to a quarantined exploratory track. They cannot serve as evidence for the core physics claims without an independently established mechanism and bridge.

### 3.2 INV-005 independent cross-check

The isolated NumPy-only workflow in the research repository ran the actual demo and test module.

| Field | Recorded result |
|---|---|
| GitHub Actions run | [INV-005 cross-check #4](https://github.com/kalmahdy326-lang/holos-reality/actions/runs/43156925600) |
| Tested commit | \`e9d6aa1a3da86a33a34c19fd288abb371265df8d\` |
| Local Pacific date | 11 November 2026 |
| UTC timestamp | 2026-11-12 04:46:09Z |
| Runner | Ubuntu 26.04.1 |
| Python | 3.11.18 |
| NumPy | 1.26.4 (only installed numerical dependency) |
| Demo | Passed |
| Unit tests | **19 passed; 0 failed** |
| Reproducibility artifact | [inv005-crosscheck-python311-numpy1264](https://github.com/kalmahdy326-lang/holos-reality/actions/runs/43156925600/artifacts/13916118283) |

Numerical landmarks:
- Maximum one-/two-party marginal difference: \(1.11022302463\times10^{-16}\).
- \(I(A:C|B)_{\rm GHZ}=1\) bit.
- Diagonal mixture CMI \(=0\).
- Product Markov state CMI \(=0\).
- Petz GHZ fidelity \(=0.707106781187\).
- Petz diagonal-mixture fidelity \(=1\).
- GHZ/mixture global fidelity \(=0.707106781187\).
- The product Markov Petz exact-recovery check is included in the unit suite and passed.

**Count discrepancy retained:** the supplied protocol expected 18 tests, but the committed module currently discovers 19 test methods because it includes an additional fidelity-range test. All 19 passed. The suite was not altered to remove a valid test merely to match the earlier count. The demo prints named metrics rather than a five-section narrative summary; the expected numerical landmarks are present.

A workflow-label edit briefly produced a YAML parse failure before any test job started. The label was corrected; run #3 above is the successful, final verification. This configuration-only failure did not correspond to a failed experiment or unit test.

## 4. Animation and local-production layer

The production repository currently contains the Python/Godot/FFmpeg engine, configuration examples, contracts, tests and CI.

### 4.1 Character and animation status

The project history records:
- Khaled functional character rig / Milestone 3 benchmark completed.
- Kevin independent rig / Milestone 4 benchmark completed.
- Two-character interaction work is a prototype/refinement milestone, not finished production animation.
- Known polish gaps include phoneme-level lip synchronization, facial-layer edges, articulated torso/arms/hands/props, smoother gaze/head motion, broader expressions and clean production removal of diagnostics.

**Important repository limitation:** the source inventory baseline for the current GitHub checkout recorded 36 regular files (196,252 bytes), 3 skipped entries and 0 traversal errors. It found only the generic Godot shot runner and adapter test scene; it did not find the original Khaled/Kevin rig scenes or their resource dependencies. The CI fixture is not evidence that the original character rigs have been integrated.

### 4.2 Milestone 6 — Local Production Engine

The existing engine includes:
- Python CLI and versioned JSON episode configuration.
- Generic Godot shot-render adapter and resource dependency audit.
- Ordered, resumable multi-shot rendering with manifests and integrity checks.
- FFmpeg episode assembly and FFprobe validation.
- Stream-level audio/video timing checks.
- Source inventory, verified backup and non-overwriting restore operations.
- Debug/production output separation and automated tests.

Still unverified:
- Integration and regression testing of the actual Khaled and Kevin source rigs.
- Inventory and verified backup of the real local source project and media.
- Offline acceptance on the target production machine.
- Final production-quality animation.

The open [Milestone 6 GitHub issue](https://github.com/kalmahdy326-lang/HOLOS/issues/1) remains the authoritative acceptance brief. Offline acceptance must be performed with internet disconnected; CI is not a substitute.

### 4.3 Non-negotiable production constraints

- Local-first and offline-capable; Manus is optional development assistance, never a runtime dependency.
- No paid software, subscriptions, AI credits or external AI services without explicit authorization.
- Preserve original source assets, dialogue, soundtrack, benchmarks and history.
- Inventory and back up before changes; do not overwrite or delete originals without safeguards.
- Separate source material from generated output.
- Distinguish prototype, validated component and production-ready status.

## 5. Book manuscript and editorial records

The manuscript must remain separate from the physics research papers and the animation screenplay.

The authoritative working text recorded in the project history on 4 November 2026 consists of:
- Introduction: **“The Picture We Cannot See”**
- Chapter 1: **“An Interesting Little Universe”**
- Chapter 2: **“The Man in the Mirror”**

That supplied text was designated unchanged; Chapter 3 had not yet been written at that point. The working title recorded for Chapter 3 was **“The Space Between Things.”**

Later Project-space material dated around 9 November contains editorial/revision discussions referring to Chapters 4 and 5, an Epilogue, the emergence/status ladder, a revised relational posture and a proposed “Ultimate Whole” section. Those are later revision notes and pasted excerpts, not a verified complete replacement manuscript. The source text and chapter numbering therefore need reconciliation before any merge.

**Preservation rule:** do not overwrite the 4 November manuscript, invent missing chapters, or silently combine the later editorial excerpts with the earlier text. Store each recovered manuscript snapshot with its own date and hash; keep revision briefs separate from clean manuscript text. The actual full manuscript source was not present in the current GitHub production tree at the time of this inventory.

## 6. Creative assets and source-package inventory

The Project-space Library inventory surfaced the following HOLOS source materials. They are identified here so they are not lost or mistaken for files already present in GitHub.

| Source item | Current classification | GitHub status |
|---|---|---|
| \`HOLOS_Fundamental_Structure_of_Reality_Research_Project_v1.docx\` and PDF | Master research charter, v1.0, 5 Nov 2026 | Research content represented in research repo; original binary source not yet mirrored here |
| \`HOLOS_Weekly_Research_Intelligence_Report_004.docx\` | Weekly research report, 8 Nov 2026 | Related technical notes exist in research repo; original report binary not yet mirrored |
| \`HOLOS_Technical_Note_004-A.md/.docx\` and \`004-A(1).docx\` | GfE reconstruction/audit and subsequent review | Some related 004-series notes are in research repo; source versions need explicit reconciliation |
| \`HOLOS_Technical_Investigation_001\` package and notebook | Earlier GfE reconstruction work | Preserve as dated source snapshot; compare with current 004-series notes |
| \`HOLOS_Technical_Investigation_002\` PDF/DOCX/notebook/package | Earlier technical investigation | Preserve as dated source snapshot; compare before superseding |
| \`holos-reality-repository.zip\` | Earlier research repository archive | Superseded as live working source by the current research repository, but preserve as historical snapshot |
| \`HOLOS_Episode_1_The_Moon_Has_Anger_Issues_Complete_Screenplay.docx\` | Episode 1 screenplay | Not found in current production repository tree |
| Character reference/guide sheets for Khaled and Kevin | Visual source references | Not found in current production repository tree |
| \`HOLOS_Model_Initialization_Package.zip\` and checksum | Project initialization archive | Not yet mirrored; retain checksum and original |
| \`HOLOS_Autonomous_Execution_Package.zip\` | Execution/research workflow archive | Not yet mirrored; inspect contents before integration |
| \`HOLOS_Theory_of_Nested_Emergence_Presentation.pptx\` | Historical conceptual presentation | Preserve as historical framing; do not treat its claims as current scientific conclusions |
| Later \`Pasted text\` project records | Manuscript revision notes and other project conversations | Use as dated decision/editorial records, not as a replacement for original manuscript or source files |

The table is an inventory of surfaced source items, not a claim that every binary file has already been copied into this repository. Before migration, preserve originals, inspect archive contents, compute SHA-256, record provenance/date/version, and avoid committing generated caches, credentials or unlicensed third-party material. Large media should use Git LFS or a separately controlled artifact/archive strategy only after size and license review.

## 7. Other projects deliberately excluded

The wider Projects space also contains work that is not part of HOLOS and must not be imported merely because it shares an account or workspace:
- PersonaOS and other software/startup work.
- The Incomplete Record channel and unrelated production assets.
- Music and album projects.
- Public-accountability research and unrelated writing.

If one of those projects later supplies a clearly defined HOLOS deliverable, import only that deliverable with provenance and a documented reason. Do not merge entire unrelated projects into HOLOS.

## 8. Source-of-truth rules and migration sequence

1. **GitHub research repo** is the source of truth for scientific investigations, proofs, code, tests, references and evidence labels.
2. **This HOLOS repo** is the source of truth for animation production code, engine contracts, character integration, episode configuration and local-production acceptance.
3. **Manuscript source files** remain versioned as their own dated text snapshots; no silent editorial changes.
4. **Original media and source archives** remain immutable until inventoried and backed up. Generated renders and reports stay separate.
5. **Project-space chat summaries** are not substitutes for missing source documents. Where only a summary or excerpt survives, label it as such.
6. Every migrated file receives a source path/name, date/version if known, SHA-256, destination, license/provenance note and migration commit.
7. Every scientific or production claim retains its own acceptance gate; a green research test does not validate an animation rig, and a successful render does not validate a physics hypothesis.

### Next consolidation gates

- [ ] Recover and reconcile the exact current manuscript text and later Chapter 4/5 revision records.
- [ ] Migrate the master research charter and selected dated research reports as immutable source documents, with hashes and a clear supersession map.
- [ ] Inspect and inventory the Episode 1 screenplay, character sheets, initialization package and execution package before adding source assets.
- [ ] Inventory and back up the actual local Khaled/Kevin Godot rigs and their complete dependencies.
- [ ] Integrate both original rigs under the existing adapter contract and run the character regression benchmarks.
- [ ] Perform and record the actual disconnected-network Episode 1 acceptance test.
- [ ] Continue the scientific mixed-state conversion work only inside the finite-dimensional quantum-information track; maintain the explicit no-gravity-bridge boundary.

---

**Governing principle:** preserve the record, separate the workstreams, and let evidence decide what survives.


## Source recovery and first migration pass — 2026-11-12

The Project-space Library has now been searched beyond the initial top-level inventory. Additional original records were located:

### Research records

- Master Research Charter v1.0, 5 November 2026 (DOCX, 93,836 bytes; 38 pages).
- Weekly Research Intelligence Report 004, 8 November 2026 (DOCX, 19,252 bytes; 5 pages).
- Technical Note 004-A (DOCX, 49,498 bytes; 8 pages), plus a native Markdown source (33,390 bytes).
- Technical Investigation 001 — GfE Reconstruction (DOCX, 56,079 bytes; 15 pages) and its Jupyter notebook (12,046 bytes).
- Technical Investigation 002 — Lorentzian Curvature Traces (DOCX, 48,647 bytes; 10 pages) and its Jupyter notebook (7,154 bytes), plus a PDF.
- Weekly Research Intelligence Report 002 (PDF, 700,586 bytes).
- Investigation 001 and 002 ZIP packages and the prior holos-reality repository ZIP.

Readable text snapshots for the charter, Report 004, Technical Note 004-A, Investigations 001/002, and the complete screenplay have been committed to the appropriate repositories. The two Investigation 002 notebooks were text-compared and are identical; one canonical notebook is retained. The two Technical Note 004-A DOCX extractions are identical; one canonical extraction is retained. The native Markdown 004-A source is retained separately because it is a distinct source format.

Research archive index: https://github.com/kalmahdy326-lang/holos-reality/tree/main/research/source_archive

### Production records and visual references

- Complete Episode 1 screenplay, “The Moon Has Anger Issues” (DOCX, 48,709 bytes; 25 pages); readable text extraction committed to the production repository.
- Three paired Khaled/Kevin character-guide PNGs (2,013,102; 1,949,860; and 2,085,157 bytes) were visually inspected and inventoried. The artwork distinguishes Khaled (brown hair, blue eyes, senior researcher) from Kevin (red hair, blue eyes, junior investigator) and includes turnaround/expression views. These are reference sheets, not the actual Godot rigs.
- Model Initialization ZIP (64,530 bytes) and Autonomous Execution ZIP (21,652 bytes) were located, but their contents could not be inspected because raw-byte materialization was not authorized in this session. No integration or contents claim is made.

Production source archive index: https://github.com/kalmahdy326-lang/HOLOS/tree/main/docs/source_archive

### Exact manuscript remains a separate unresolved source-recovery item

The authoritative manuscript is still identified as the exact text supplied on 4 November 2026: Introduction “The Picture We Cannot See,” Chapter 1 “An Interesting Little Universe,” and Chapter 2 “The Man in the Mirror.” Chapter 3, “The Space Between Things,” had not yet been written. The current Library search surfaced later editorial/audit text that explicitly says the full manuscript text was not available there; it is not a substitute for the authoritative manuscript. Do not reconstruct, paraphrase, or silently merge it from summaries. The exact 4 November source conversation or original manuscript file must be recovered before an immutable manuscript snapshot can be committed.

### Binary preservation boundary

All GitHub imports in this pass are readable text extractions or notebook JSON, not original DOCX/PDF/PNG/ZIP binaries unless explicitly identified otherwise. No original-binary SHA-256 values are claimed. Original Library sources remain untouched. The remaining binary export/checksum and large-asset strategy are open tasks.


### Additional historical HOLOS artifacts located

- `HOLOS_Theory_of_Nested_Emergence_Presentation.pptx` (537,980 bytes; 21-slide historical presentation, identified in the Library). It belongs in the historical concept archive and must not replace the current reality-first research charter.
- `holos_final_conclusion.md` (23,030 bytes; located but not yet reviewed or designated current).
- `HOLOS — Weekly Research Intelligence Report 002` (PDF, 700,586 bytes; located, text extraction not yet available).
- Prior `holos-reality-repository.zip` (57,237 bytes; located, contents not yet inspected).

The PowerPoint and final-conclusion Markdown were not successfully extracted in this pass. They remain located but unimported; no content or current-status claims are inferred from their filenames.


### Khaled/Kevin rig status reconciliation

A new evidence conflict was identified. An earlier milestone update says Khaled's functional rig was complete and Kevin's independent rig was next; the Milestone 6 document lists both rigs and a two-character prototype as existing work; the current character-rig integration contract says neither original rig scene/dependency set is present in this repository. The repository tree and 231-item Project-space Library inventory contain three visual reference sheets but no verified character scene or rig source files. The small initialization/autonomous ZIP packages could not be opened in this session, so they cannot be used as evidence that the rigs are present.

The defensible status is therefore: visual references located; original rig files not yet recovered/verified; generic adapter CI only. Milestone 6 remains in progress. See [rig source reconciliation](rig-source-reconciliation-2026-11-12.md). Do not replace the missing source with newly generated substitute rigs.
