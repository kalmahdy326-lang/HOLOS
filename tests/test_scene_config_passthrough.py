"""Tests that approved scene configuration reaches Godot safely."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import holos


class SceneConfigPassthroughTests(unittest.TestCase):
    def test_scene_config_is_forwarded_as_nested_data(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            observed: dict = {}

            def capture_config(**kwargs):
                config_path = kwargs["project_root"] / kwargs["shot_config"]
                observed.update(json.loads(config_path.read_text(encoding="utf-8")))
                return {"success": True, "frame_count": 3}

            episode = {
                "episode_id": "bookend_test",
                "render": {"width": 320, "height": 180, "fps": 24},
            }
            scene = {"scene_id": "opening"}
            shot = {
                "shot_id": "S00_TITLE",
                "scene": "res://scenes/episode_bookend_card.tscn",
                "start_frame": 0,
                "end_frame": 3,
                "scene_config": {
                    "card_mode": "title",
                    "series_title": "HOLOS",
                    "episode_title": "Episode 1",
                },
            }

            with patch.object(holos, "render_shot", side_effect=capture_config):
                holos._render_configured_shot(
                    root=root,
                    episode=episode,
                    scene=scene,
                    shot=shot,
                    mode="debug",
                    godot_project=root / "godot",
                    godot_executable=None,
                    display_wrapper=None,
                    output_dir=root / "output" / "renders" / "title",
                )

            self.assertEqual(observed["scene_config"], shot["scene_config"])
            self.assertEqual(observed["width"], 320)
            self.assertEqual(observed["fps"], 24)


if __name__ == "__main__":
    unittest.main()
