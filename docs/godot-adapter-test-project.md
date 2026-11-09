# Godot Adapter Test Project

This is a deliberately tiny Godot 4 project for exercising the generic HOLOS
shot runner before any character rig is connected.

## Contents

- `project.godot`: minimal project configuration.
- `holos_shot_runner.gd`: shared HOLOS frame-capture runner.
- `test_scenes/adapter_test.tscn`: simple test scene.
- `test_scenes/adapter_test.gd`: deterministic frame-driven visual.

## Rendering modes

Godot's `--headless` mode uses a dummy rendering backend in environments
without a rendering device. It can run non-visual tasks, but it cannot provide
the viewport texture required by this PNG frame-capture runner.

For actual frame capture on a display-less Linux machine, run Godot with a
rendering-capable display supplied by Xvfb and software OpenGL. The Python
adapter supports this using `headless=False` and a command prefix such as
`("xvfb-run", "-a")`. On a desktop with a working display, use
`headless=False` without the Xvfb prefix.

## Manual test on Linux

Install Godot 4, Xvfb, and Mesa software rendering. From the repository root:

```bash
mkdir -p godot/output
cp examples/adapter_test_shot.json godot/adapter_test_shot.json
LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a godot --path godot \
  --script res://holos_shot_runner.gd -- \
  --config adapter_test_shot.json \
  --output output/adapter_test_manual
```

Expected output: four PNG frames named `frame_000000.png` through
`frame_000003.png`, each 320×180.

## Automated integration test

Set `HOLOS_GODOT` to the installed Godot 4 executable path. On a Linux
machine with Xvfb and Mesa installed, run:

```bash
HOLOS_GODOT=/path/to/godot \
HOLOS_GODOT_HEADLESS=0 \
HOLOS_GODOT_DISPLAY_WRAPPER=xvfb-run \
LIBGL_ALWAYS_SOFTWARE=1 \
python -m unittest discover -s tests -p "test_godot_integration.py" -v
```

If `HOLOS_GODOT` is not set, the integration test is skipped. A skipped test
is not evidence that Godot rendering passed.
