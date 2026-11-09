"""Tests for the Godot subprocess command contract."""

import unittest
from pathlib import Path

from holos_engine.godot_adapter import build_render_command


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


if __name__ == "__main__":
    unittest.main()
