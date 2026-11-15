# Milestone 5.1 production integration gates

## Ready for repository validation

- The source MP3 hash is verified.
- The approved transcript and pronunciation decision are recorded.
- The supplied full-episode word alignment and flat event timelines are checked in the PR handoff.
- The portable builder emits schema-versioned output through the repository's strict processor contract.
- Godot headless tests load the handoff timeline files through the existing `HolosTimeline` consumer.

## Still required for production animation acceptance

The current repository contains only the minimal Godot adapter test project. It has no Episode 1 production dialogue controller, director, character scenes, mesh or skeleton assets, WAV asset, or animated production camera setup. Therefore this branch cannot safely connect a timeline to the production actors or name any rig controls.

The two review WAV variants have different hashes:

- Manus variant: `4b8c1d78ac6ca233f9ae2ba3f31566baaa75a83802eac8257ba7cba48cd76730`
- Codex variant: `e9d8a3a88f310b1558a884fcec87f8cf16741019ddbcede2a2db2cc2db74194f`

They remain separate. Before a production controller can reference audio, select one exact WAV as the production source, verify its hash and audio format, and keep its timeline offset tied to that same file.

After the production Godot project and selected WAV are present:

1. Integrate audio playback with one shared transport clock. The director and both actor adapters must consume the same audio position for play, pause, resume, seek, and stop.
2. Load the relative flat timeline using the chosen WAV's provenance and duration.
3. Map semantic visemes only to controls verified in each actual character rig.
4. Run Godot headless schema, ordering, timing, silence, and speaker-isolation checks.
5. Render the benchmark and review eased transitions, facial seams, hair continuity, and the final held/rest pose.
6. Accept production animation only after the rendered result passes visual review.

Passing the handoff file checks or the adapter headless test does not by itself constitute production animation acceptance.
