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
from holos_engine.preflight import (
    ScenePreflightError,
    validate_scenes_with_godot,
)

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.environ.get("HOLOS_GODOT"), "Set HOLOS_GODOT to run Godot integration test")
class GodotOffscreenIntegrationTests(unittest.TestCase):
    def test_runtime_preflight_loads_each_scene_as_packed_scene(self):
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            copied_project = temp_root / "godot"
            shutil.copytree(ROOT / "godot", copied_project,
                            ignore=shutil.ignore_patterns(".godot", ".git"))
            episode = {"scenes": [{"scene_id": "preflight", "shots": [
                {"shot_id": "A", "scene": "res://test_scenes/adapter_test.tscn"},
                {"shot_id": "B", "scene": "res://test_scenes/adapter_test.tscn"},
            ]}]}
            result = validate_scenes_with_godot(
                project_root=temp_root, episode=episode,
                godot_project=Path("godot"), executable=os.environ["HOLOS_GODOT"],
                timeout_seconds=120,
            )
            self.assertTrue(result["valid"])
            self.assertEqual(len(result["checked"]), 2)
            self.assertTrue(all(item["valid"] for item in result["checked"]))
            self.assertIn("major", result["godot_version"])

    def test_runtime_preflight_rejects_invalid_scene_file(self):
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            copied_project = temp_root / "godot"
            shutil.copytree(ROOT / "godot", copied_project,
                            ignore=shutil.ignore_patterns(".godot", ".git"))
            invalid_scene = copied_project / "test_scenes" / "invalid_preflight.tscn"
            invalid_scene.write_text("this is not a Godot scene", encoding="utf-8")
            episode = {"scenes": [{"scene_id": "preflight", "shots": [
                {"shot_id": "BAD", "scene": "res://test_scenes/invalid_preflight.tscn"},
            ]}]}
            with self.assertRaisesRegex(ScenePreflightError, "PackedScene"):
                validate_scenes_with_godot(
                    project_root=temp_root, episode=episode,
                    godot_project=Path("godot"), executable=os.environ["HOLOS_GODOT"],
                    timeout_seconds=120,
                )

    def test_cli_blocks_batch_when_scene_file_cannot_load(self):
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp) / "project"
            project_root.mkdir()
            for folder in ("godot", "holos_engine", "tools", "examples"):
                shutil.copytree(ROOT / folder, project_root / folder)
            invalid_scene = project_root / "godot" / "test_scenes" / "broken.tscn"
            invalid_scene.write_text("not a valid scene resource", encoding="utf-8")

            episode_path = project_root / "examples" / "broken_scene_episode.json"
            episode_path.write_text(json.dumps({
                "schema_version": 1,
                "episode_id": "broken_scene_episode",
                "title": "Broken Scene Preflight Test",
                "render": {"width": 320, "height": 180, "fps": 24},
                "audio": {"dialogue": None, "music": None},
                "scenes": [{"scene_id": "scene_01", "shots": [{
                    "shot_id": "BROKEN",
                    "scene": "res://test_scenes/broken.tscn",
                    "start_frame": 0,
                    "end_frame": 2,
                    "characters": [],
                    "assets": [],
                }]}],
            }), encoding="utf-8")

            env = os.environ.copy()
            env["PYTHONPATH"] = str(project_root)
            command = [
                sys.executable, str(project_root / "tools" / "holos.py"),
                "--project-root", str(project_root),
                "render-episode", "--episode", str(episode_path),
                "--mode", "debug", "--godot-executable", env["HOLOS_GODOT"],
            ]
            result = subprocess.run(
                command, cwd=project_root, env=env, capture_output=True,
                text=True, timeout=120, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PackedScene", result.stderr + result.stdout)
            self.assertFalse((project_root / "output" / "renders").exists())
            self.assertFalse((project_root / "output" / "manifests").exists())

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
                / "adapter_test_episode" / "debug" / "ADAPTER_TEST"
            )
            frames = sorted(rendered.glob("frame_*.png"))
            self.assertEqual(len(frames), 4)
            self.assertTrue((project_root / "output" / "reports"
                             / "adapter_test_episode-debug-ADAPTER_TEST-render.json").is_file())

            production_command = command.copy()
            production_command[production_command.index("--mode") + 1] = "production"
            production_result = subprocess.run(
                production_command, cwd=project_root, env=env,
                capture_output=True, text=True, timeout=120, check=False,
            )
            self.assertEqual(
                production_result.returncode, 0,
                production_result.stderr or production_result.stdout,
            )
            production_dir = (
                project_root / "output" / "renders" / "adapter_test_episode"
                / "production" / "ADAPTER_TEST"
            )
            production_frames = sorted(production_dir.glob("frame_*.png"))
            self.assertEqual(len(production_frames), 4)
            self.assertTrue((project_root / "output" / "reports"
                             / "adapter_test_episode-production-ADAPTER_TEST-render.json").is_file())
            self.assertNotEqual(
                frames[0].read_bytes(),
                production_frames[0].read_bytes(),
                "Debug fixture should include the debug overlay; production must not.",
            )


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
                / "adapter_test_episode_batch" / "debug"
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
