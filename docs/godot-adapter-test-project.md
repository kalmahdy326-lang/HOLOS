# Godot Adapter Test Project

This is a deliberately tiny Godot 4 project for exercising the generic HOLOS
headless shot runner before any character rig is connected.

## Contents

- `project.godot`: minimal project configuration.
- `holos_shot_runner.gd`: shared HOLOS frame-capture runner.
- `test_scenes/adapter_test.tscn`: simple test scene.
- `test_scenes/adapter_test.gd`: deterministic frame-driven visual.

## Manual test

From the repository root:

```bash
godot --headless --path godot --script res://holos_shot_runner.gd -- \
  --config examples/adapter_test_shot.json \
  --output output/adapter_test_manual
```

The command above uses a config path visible to the runner process; for this
minimal project, copy the example JSON into the Godot project directory or use
an absolute path under the repository.

Expected output: four PNG frames named `frame_000000.png` through
`frame_000003.png`, each 320×180.

## Automated integration test

Set `HOLOS_GODOT` to the installed Godot 4 executable path, then run:

```bash
HOLOS_GODOT=/path/to/godot python -m unittest tests/test_godot_integration.py -v
```

If the variable is not set, the integration test is skipped. A skipped test is
not evidence that Godot rendering passed.
