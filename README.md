HOLOS

An Independent Animation & Production Project

Project author: Khaled AL-MAHDY

HOLOS is an independent animation and storytelling project focused on building a complete, locally operated production pipeline.

The goal is to develop a production environment where characters, environments, animation, dialogue, sound, and final video assembly work together as one coherent system.

HOLOS is designed to remain independent of external AI services, subscriptions, paid generation credits, and internet-dependent production tools.

---

1. Project Philosophy

HOLOS belongs to the project, not to any particular software platform or service.

Its production system must remain:

- Independent: No mandatory dependence on external AI platforms or subscriptions.
- Local-first: Core production must run on locally available software and assets.
- Offline-capable: Rendering, assembly, and validation must work without internet access.
- Reproducible: Production should be driven by explicit configurations and repeatable processes.
- Modular: Characters, scenes, animation, audio, and rendering should remain independently manageable.
- Preservational: Existing assets, completed work, dialogue, soundtrack, and benchmarks must be protected.

The objective is not simply to produce individual animations. It is to establish a reusable production system capable of producing complete episodes.

2. Technical Architecture

HOLOS uses several tools, each with a clearly defined responsibility.

Technology| Responsibility
Godot| Character rigs, animation, scenes, and rendering
Python| Production controller, configuration, automation, validation, and reporting
FFmpeg| Video assembly, encoding, and audio integration
FFprobe| Media inspection and technical validation
JSON| Episode, scene, shot, dialogue, and render configuration
Git| Version control and project history

The architecture avoids unnecessary duplication of responsibilities.

Godot handles animation and rendering. Python coordinates production. FFmpeg handles media assembly. JSON defines what is being produced.

3. Character Development

HOLOS currently has two independently functioning character animation prototypes.

Khaled — Milestone 3

- Independent character rig.
- Layered facial animation.
- Multiple mouth shapes.
- Blinking and gaze changes.
- Facial expression changes.
- Head movement and environmental animation.
- Functional dialogue benchmark.

Kevin — Milestone 4

- Independent character rig.
- Facial and mouth animation.
- Blinking and gaze changes.
- Multiple expression states.
- Speaking and listening states.
- Functional dialogue benchmark.

Both characters have completed initial functional benchmarks.

These are working prototypes, not yet finished production-quality character rigs.

Further development includes improved phoneme-level lip synchronization, facial-layer polish, articulated body movement, smoother gaze tracking, and more expressive acting.

The HOLOS adapter handoff requirements and evidence gates for integrating the original character files are documented in [Character Rig Integration Contract](docs/character-rig-integration-contract.md). The current repository does not yet contain either original rig scene or its dependencies.

4. Production Engine — Milestone 6

The current major engineering objective is the HOLOS Local Production Engine.

The purpose is to integrate existing character rigs and production tools into a unified system.

The engine will provide:

1. A central Python production controller.
2. Structured episode and shot configuration.
3. Godot integration for character and scene rendering.
4. Individual shot rendering.
5. Ordered multi-shot rendering with resumable manifests.
6. Verified complete-episode assembly from ordered shot folders.
7. Automatic audio/video assembly and validation.
8. Separate production/debug render modes with a debug-only optional overlay.
9. Automated validation.
10. Versioned outputs, verified backups, and non-overwriting source restoration.
11. Structured production logs.
12. Offline installation and operation.

Intended production commands

python tools/holos.py render-episode --episode examples/episode_01.json --mode production

python tools/holos.py render --episode examples/episode_01.json --shot S01_B01 --mode debug

python tools/holos.py assemble-episode --episode examples/episode_01.json --mode production --output output/episode_01.mp4

python tools/holos.py inventory

python tools/holos.py backup --inventory output/reports/source-inventory-YYYYMMDDTHHMMSSZ.json

python tools/holos.py restore --backup output/backups/source-backup-YYYYMMDDTHHMMSSffffffZ

The CLI implements `render` for one shot, `render-episode` for an ordered,
resumable batch, and `assemble-episode` for final FFmpeg/FFprobe-validated
assembly from the verified manifest. The engine still requires validation
against the actual Khaled and Kevin rigs and an offline acceptance test on the
target production machine.

5. Proposed Repository Structure

HOLOS/
│
├── assets/
│   ├── characters/
│   ├── environments/
│   ├── audio/
│   └── references/
│
├── config/
│   ├── episodes/
│   └── schemas/
│
├── docs/
│
├── godot/
│   ├── characters/
│   ├── scenes/
│   └── scripts/
│
├── tools/
│   ├── render_episode.py
│   ├── validate_episode.py
│   └── holos/
│
├── output/
│   ├── renders/
│   ├── reports/
│   └── manifests/
│
└── tests/

This is the intended organization. Existing project files will be inventoried before integration or relocation.

6. Production Standards

Every production operation should follow several rules:

- Original source files remain untouched.
- Generated outputs are stored separately.
- Production settings are explicitly defined.
- Debug overlays never appear in final production output.
- Incomplete renders are never treated as completed shots.
- Failed operations produce useful logs and error codes.
- Existing work is backed up before structural changes.
- Every final episode can be technically inspected and validated.

The system must also distinguish between identical binary output and visually and temporally equivalent output when rendering introduces nondeterministic behavior.

7. Independence From External Services

HOLOS does not require Manus to operate.

Manus and other AI assistants may optionally help with development, research, planning, or troubleshooting.

However, the actual production pipeline must remain independently executable.

No paid software, subscriptions, AI generation credits, or external AI services are to be introduced without explicit authorization.

8. Development Roadmap

Milestone| Objective| Status
1–2| Initial production research and animation groundwork| Completed
3| Khaled functional character rig| Completed
4| Kevin functional character rig| Completed
5| Two-character interaction and animation refinement| Prototype / refinement
6| Unified local production engine| Current objective
7| Production-ready animation workflow| Planned
8| Full Episode 1 animation| Planned

Milestone completion must be supported by actual working results and documented verification.

9. Acceptance Standard

The production engine will not be considered complete until it can:

1. Operate with internet access disabled.
2. Load both existing character rigs.
3. Render multiple configured shots.
4. Assemble those shots into a complete video.
5. Preserve and integrate the original audio.
6. Validate the final output.
7. Produce a report and production manifest.
8. Recover safely from interrupted production.
9. Reproduce the configured workflow without external services.

An offline acceptance test must actually be performed before offline capability is declared verified.

---

10. Project Attribution

HOLOS
An independent animation and production project.

Researcher and Project Author:
Khaled AL-MAHDY

The project is developed through independent research, technical experimentation, original creative work, and iterative engineering.

All development should preserve a clear distinction between completed work, working prototypes, ongoing investigations, and future objectives.

---

Build independently. Preserve what works. Verify what is claimed.

11. HOLOS Project Hub and Research Programme

HOLOS is maintained as one programme with two deliberately separated GitHub repositories:

- **This repository — [HOLOS production hub](https://github.com/kalmahdy326-lang/HOLOS):** local-first animation and the Python/Godot/FFmpeg production engine.
- **[HOLOS scientific research](https://github.com/kalmahdy326-lang/holos-reality):** the reality-first research charter, investigations INV-001 through INV-014, boundary-mathematics work, source register, reproducible experiments, tests and research workflows.

The separation keeps scientific dependencies and evidentiary claims independent from animation production code. The shared [Project-space consolidation register](docs/project-space-consolidation-2026-11-11.md) records the cross-project architecture, manuscript status, source-package inventory, migration gates and the boundary between HOLOS and unrelated projects.

The research programme's governing rule is: “We are not trying to make our theory right. We are trying to find out what is right.” No finite-dimensional quantum-information result is to be presented as a derivation of gravity or spacetime without a separate, independently reviewed bridge.

The production repository's current implementation status and offline acceptance requirements remain in [Milestone 6 — Local Production Engine](docs/milestone-6-local-production-engine.md). The actual Khaled/Kevin source rigs and disconnected-network acceptance test remain unverified in this repository.
