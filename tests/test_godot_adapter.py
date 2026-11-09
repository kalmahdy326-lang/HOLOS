"""Tests for the Godot subprocess command contract and safe preflight."""

import tempfile
import unittest
from pathlib import Path

from holos_engine.godot_adapter import (
    GodotAdapterError,
    build_render_command,
    render_shot,
)


class GodotCommandTests(unittest.TestCase):
    def test_builds_headless_command_with_user_arguments(self):
        command = build_render_command(
            "godot",
            Path("/project/godot"),
            "res://holos_shot_runner.gd",
            Path("/project/config/shot.json"),
            Path("/project/output/shot"),
        )
        self.assertEqual(command[0:4], [
            "godot", "--headless", "--path", "/project/godot"
        ])
        self.assertIn("--script", command)
        self.assertIn("--", command)
        self.assertEqual(command[-4:], [
            "--config", "/project/config/shot.json",
            "--output", "/project/output/shot",
        ])

    def test_rejects_project_without_project_file_before_launch(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / "godot"
            project.mkdir()
            config = root / "shot.json"
            config.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(GodotAdapterError, "project.godot"):
                render_shot(
                    project_root=root,
                    godot_project=Path("godot"),
                    runner_script="res://holos_shot_runner.gd",
                    shot_config=Path("shot.json"),
                    output_dir=Path("output/shot"),
                    expected_frame_count=1,
                    executable="godot",
                )

    def test_rejects_output_outside_project_root(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / "godot"
            project.mkdir()
            (project / "project.godot").write_text("config_version=5\n", encoding="utf-8")
            (project / "holos_shot_runner.gd").write_text("# runner\n", encoding="utf-8")
            config = root / "shot.json"
            config.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(GodotAdapterError, "inside project root"):
                render_shot(
                    project_root=root,
                    godot_project=Path("godot"),
                    runner_script="res://holos_shot_runner.gd",
                    shot_config=Path("shot.json"),
                    output_dir=Path("../outside"),
                    expected_frame_count=1,
                    executable="godot",
                )


if __name__ == "__main__":
    unittest.main()
