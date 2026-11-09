"""End-to-end tests for an installed Godot 4 executable and real viewport rendering.

Set HOLOS_GODOT to the executable path to enable the offscreen render tests.
On display-less Linux, also set the Xvfb wrapper and disable strict headless mode.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from holos_engine.godot_adapter import render_shot

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.environ.get("HOLOS_GODOT"), "Set HOLOS_GODOT to run Godot integration test")
class GodotOffscreenIntegrationTests(unittest.TestCase):
    def test_minimal_scene_renders_expected_frames(self):
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            config = temp_root / "shot.json"
            config.write_text(json.dumps({
                "scene": "res://test_scenes/adapter_test.tscn",
                "shot_id": "ADAPTER_TEST",
                "start_frame": 0,
                "end_frame": 4,
                "fps": 24,
                "width": 320,
                "height": 180,
                "mode": "debug"
            }), encoding="utf-8")

            # Config and output must be project-root-contained. Use a temporary
            # copy of the small test project so the test never writes into source.
            import shutil
            copied_project = temp_root / "godot"
            shutil.copytree(ROOT / "godot", copied_project,
                            ignore=shutil.ignore_patterns(".godot", ".git"))
            copied_config = copied_project / "shot.json"
            copied_config.write_text(config.read_text(encoding="utf-8"), encoding="utf-8")

            result = render_shot(
                project_root=copied_project,
                godot_project=Path("."),
                runner_script="res://holos_shot_runner.gd",
                shot_config=Path("shot.json"),
                output_dir=Path("output/adapter_test"),
                expected_frame_count=4,
                executable=os.environ["HOLOS_GODOT"],
                timeout_seconds=120,
                # Godot's --headless mode uses a dummy renderer and cannot
                # provide viewport textures. CI uses Xvfb + software GL.
                headless=os.environ.get("HOLOS_GODOT_HEADLESS", "1") != "0",
                command_prefix=tuple(
                    [os.environ["HOLOS_GODOT_DISPLAY_WRAPPER"], "-a"]
                    if os.environ.get("HOLOS_GODOT_DISPLAY_WRAPPER") else []
                ),
            )
            self.assertEqual(result["frame_count"], 4)
            self.assertTrue(Path(result["first_frame"]).is_file())
            self.assertTrue(Path(result["last_frame"]).is_file())

    def test_cli_renders_configured_shot_end_to_end(self):
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp) / "project"
            project_root.mkdir()
            for folder in ("godot", "holos_engine", "tools", "examples"):
                shutil.copytree(ROOT / folder, project_root / folder)

            env = os.environ.copy()
            env["PYTHONPATH"] = str(project_root)
            command = [
                sys.executable,
                str(project_root / "tools" / "holos.py"),
                "--project-root", str(project_root),
                "render",
                "--episode", "examples/adapter_test_episode.json",
                "--shot", "ADAPTER_TEST",
                "--mode", "debug",
                "--godot-executable", env["HOLOS_GODOT"],
            ]
            wrapper = env.get("HOLOS_GODOT_DISPLAY_WRAPPER")
            if wrapper:
                command.extend(["--display-wrapper", wrapper])

            result = subprocess.run(
                command,
                cwd=project_root,
                env=env,
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

            rendered = (
                project_root / "output" / "renders"
                / "adapter_test_episode" / "ADAPTER_TEST"
            )
            frames = sorted(rendered.glob("frame_*.png"))
            self.assertEqual(len(frames), 4)
            self.assertTrue((project_root / "output" / "reports"
                             / "adapter_test_episode-ADAPTER_TEST-render.json").is_file())


    def test_cli_renders_episode_in_order_and_resumes_verified_shots(self):
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp) / "project"
            project_root.mkdir()
            for folder in ("godot", "holos_engine", "tools", "examples"):
                shutil.copytree(ROOT / folder, project_root / folder)

            env = os.environ.copy()
            env["PYTHONPATH"] = str(project_root)
            command = [
                sys.executable,
                str(project_root / "tools" / "holos.py"),
                "--project-root", str(project_root),
                "render-episode",
                "--episode", "examples/adapter_test_episode_batch.json",
                "--mode", "debug",
                "--godot-executable", env["HOLOS_GODOT"],
            ]
            wrapper = env.get("HOLOS_GODOT_DISPLAY_WRAPPER")
            if wrapper:
                command.extend(["--display-wrapper", wrapper])

            first = subprocess.run(
                command, cwd=project_root, env=env, capture_output=True,
                text=True, timeout=180, check=False,
            )
            self.assertEqual(first.returncode, 0, first.stderr or first.stdout)

            render_root = (
                project_root / "output" / "renders"
                / "adapter_test_episode_batch"
            )
            for shot_id in ("ADAPTER_TEST_A", "ADAPTER_TEST_B"):
                frames = sorted((render_root / shot_id).glob("frame_*.png"))
                self.assertEqual(len(frames), 2)

            manifest_path = (
                project_root / "output" / "manifests"
                / "adapter_test_episode_batch-debug-render.json"
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(
                [item["status"] for item in manifest["shots"]],
                ["completed", "completed"],
            )

            second = subprocess.run(
                command, cwd=project_root, env=env, capture_output=True,
                text=True, timeout=60, check=False,
            )
            self.assertEqual(second.returncode, 0, second.stderr or second.stdout)
            batch_report = (
                project_root / "output" / "reports"
                / "adapter_test_episode_batch-debug-batch.json"
            )
            result = json.loads(batch_report.read_text(encoding="utf-8"))
            self.assertEqual(
                result["batch"]["skipped_verified"],
                ["ADAPTER_TEST_A", "ADAPTER_TEST_B"],
            )


if __name__ == "__main__":
    unittest.main()
