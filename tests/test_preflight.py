"""Tests for episode-level Godot scene resource preflight."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from holos_engine.preflight import (
    ScenePreflightError,
    inspect_episode_scenes,
    require_episode_scenes,
)


EPISODE = {
    "episode_id": "scene_preflight_test",
    "scenes": [
        {
            "scene_id": "scene_01",
            "shots": [
                {"shot_id": "S01_B01", "scene": "res://scenes/one.tscn"},
                {"shot_id": "S01_B02", "scene": "res://scenes/two.tscn"},
            ],
        }
    ],
}


class EpisodeScenePreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.project = self.root / "godot"
        (self.project / "scenes").mkdir(parents=True)
        (self.project / "project.godot").write_text(
            'config_version=5\n', encoding="utf-8"
        )
        (self.project / "scenes" / "one.tscn").write_text(
            '[gd_scene format=3]\n', encoding="utf-8"
        )
        (self.project / "scenes" / "two.tscn").write_text(
            '[gd_scene format=3]\n', encoding="utf-8"
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_accepts_all_existing_scene_files(self):
        result = inspect_episode_scenes(self.root, EPISODE)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["checked"]), 2)
        self.assertEqual(result["missing"], [])
        self.assertEqual(result["unsafe"], [])

    def test_reports_missing_scene_before_render(self):
        episode = json.loads(json.dumps(EPISODE))
        episode["scenes"][0]["shots"][1]["scene"] = "res://scenes/missing.tscn"
        result = inspect_episode_scenes(self.root, episode)
        self.assertFalse(result["valid"])
        self.assertEqual(result["missing"][0]["shot_id"], "S01_B02")
        with self.assertRaisesRegex(ScenePreflightError, "no shots were rendered"):
            require_episode_scenes(self.root, episode)

    def test_rejects_malformed_and_traversal_paths(self):
        for value in (
            "scenes/one.tscn",
            "res://",
            "res://../outside.tscn",
            "res://scenes/../outside.tscn",
            "res://scenes\\\\outside.tscn",
            "res:///scenes/one.tscn",
        ):
            with self.subTest(value=value):
                episode = json.loads(json.dumps(EPISODE))
                episode["scenes"][0]["shots"][0]["scene"] = value
                result = inspect_episode_scenes(self.root, episode)
                self.assertFalse(result["valid"])
                self.assertEqual(len(result["unsafe"]), 1)

    def test_rejects_scene_symlink(self):
        target = self.project / "scenes" / "one.tscn"
        link = self.project / "scenes" / "linked.tscn"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("File symlinks are unavailable on this platform.")
        episode = json.loads(json.dumps(EPISODE))
        episode["scenes"][0]["shots"][0]["scene"] = "res://scenes/linked.tscn"
        result = inspect_episode_scenes(self.root, episode)
        self.assertFalse(result["valid"])
        self.assertIn("symbolic links", result["unsafe"][0]["reason"])

    def test_cli_blocks_batch_before_creating_render_output(self):
        episode_path = self.root / "episode.json"
        episode = {
            "schema_version": 1,
            "episode_id": EPISODE["episode_id"],
            "title": "Preflight test",
            "render": {"width": 1280, "height": 720, "fps": 24},
            "audio": {"dialogue": None, "music": None},
            "scenes": [{
                "scene_id": "scene_01",
                "shots": [{
                    "shot_id": "S01_B01",
                    "scene": "res://scenes/not-created.tscn",
                    "start_frame": 0,
                    "end_frame": 2,
                    "characters": [],
                    "assets": [],
                }],
            }],
        }
        episode_path.write_text(json.dumps(episode), encoding="utf-8")
        command = [
            sys.executable,
            str(Path(__file__).resolve().parents[1] / "tools" / "holos.py"),
            "--project-root", str(self.root),
            "render-episode",
            "--episode", str(episode_path),
            "--godot-project", "godot",
        ]
        result = subprocess.run(
            command, cwd=self.root, capture_output=True, text=True,
            timeout=30, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no shots were rendered", result.stderr)
        self.assertFalse((self.root / "output" / "renders").exists())
        self.assertFalse((self.root / "output" / "manifests").exists())


if __name__ == "__main__":
    unittest.main()
