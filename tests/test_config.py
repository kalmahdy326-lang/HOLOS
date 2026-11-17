"""Configuration validation tests using only the Python standard library."""

import unittest

from holos_engine.config import ConfigError, validate_episode


VALID = {
    "schema_version": 1,
    "episode_id": "episode_test",
    "title": "Test Episode",
    "render": {"width": 1280, "height": 720, "fps": 24},
    "audio": {"dialogue": None, "music": None},
    "scenes": [{
        "scene_id": "scene_01",
        "shots": [{
            "shot_id": "S01_B01",
            "scene": "res://scenes/test_shot.tscn",
            "start_frame": 0,
            "end_frame": 24,
            "characters": ["khaled"],
            "assets": []
        }]
    }]
}


class EpisodeConfigTests(unittest.TestCase):
    def test_valid_episode(self):
        validate_episode(VALID)

    def test_accepts_background_music_gain_setting(self):
        data = {**VALID, "audio": {"dialogue": None, "music": None, "music_gain_db": -18}}
        validate_episode(data)

    def test_accepts_scene_config_object(self):
        shot = {**VALID["scenes"][0]["shots"][0],
                "scene_config": {"card_mode": "title", "episode_title": "Episode 1"}}
        data = {**VALID, "scenes": [{"scene_id": "scene_01", "shots": [shot]}]}
        validate_episode(data)

    def test_rejects_missing_scene_path(self):
        shot = dict(VALID["scenes"][0]["shots"][0])
        del shot["scene"]
        data = {**VALID, "scenes": [{"scene_id": "scene_01", "shots": [shot]}]}
        with self.assertRaisesRegex(ConfigError, r"\.scene must be a non-empty Godot res://"):
            validate_episode(data)

    def test_rejects_invalid_scene_paths(self):
        for value in ("", "scenes/test_shot.tscn", "/scenes/test_shot.tscn", "res://"):
            with self.subTest(value=value):
                shot = {**VALID["scenes"][0]["shots"][0], "scene": value}
                data = {**VALID, "scenes": [{"scene_id": "scene_01", "shots": [shot]}]}
                with self.assertRaisesRegex(ConfigError, r"\.scene must be a non-empty Godot res://"):
                    validate_episode(data)

    def test_rejects_invalid_scene_config(self):
        for value in ([], {"": "invalid"}):
            with self.subTest(value=value):
                shot = {**VALID["scenes"][0]["shots"][0], "scene_config": value}
                data = {**VALID, "scenes": [{"scene_id": "scene_01", "shots": [shot]}]}
                with self.assertRaisesRegex(ConfigError, "scene_config"):
                    validate_episode(data)

    def test_rejects_out_of_range_music_gain_setting(self):
        for value in (-61, 1, True):
            with self.subTest(value=value):
                data = {**VALID, "audio": {"dialogue": None, "music": None, "music_gain_db": value}}
                with self.assertRaisesRegex(ConfigError, "music_gain_db"):
                    validate_episode(data)

    def test_rejects_duplicate_shot_ids(self):
        data = {**VALID, "scenes": [dict(VALID["scenes"][0])]}
        data["scenes"][0]["shots"] = [
            dict(VALID["scenes"][0]["shots"][0]),
            dict(VALID["scenes"][0]["shots"][0]),
        ]
        with self.assertRaisesRegex(ConfigError, "Duplicate shot_id"):
            validate_episode(data)

    def test_rejects_invalid_frame_range(self):
        data = {**VALID, "scenes": [dict(VALID["scenes"][0])]}
        data["scenes"][0]["shots"] = [dict(VALID["scenes"][0]["shots"][0])]
        data["scenes"][0]["shots"][0]["end_frame"] = 0
        with self.assertRaisesRegex(ConfigError, "end_frame"):
            validate_episode(data)

    def test_rejects_boolean_frame_numbers(self):
        for field in ("start_frame", "end_frame"):
            with self.subTest(field=field):
                shot = {**VALID["scenes"][0]["shots"][0], field: True}
                data = {**VALID, "scenes": [{"scene_id": "scene_01", "shots": [shot]}]}
                with self.assertRaisesRegex(ConfigError, field):
                    validate_episode(data)

    def test_rejects_unsupported_schema(self):
        data = {**VALID, "schema_version": 99}
        with self.assertRaisesRegex(ConfigError, "schema_version"):
            validate_episode(data)

    def test_rejects_negative_audio_sync_tolerance(self):
        data = {**VALID, "audio": {"dialogue": None, "music": None,
                                  "sync_tolerance_ms": -1}}
        with self.assertRaisesRegex(ConfigError, "sync_tolerance_ms"):
            validate_episode(data)

    def test_rejects_boolean_audio_sync_tolerance(self):
        data = {**VALID, "audio": {"dialogue": None, "music": None,
                                  "sync_tolerance_ms": True}}
        with self.assertRaisesRegex(ConfigError, "sync_tolerance_ms"):
            validate_episode(data)

    def test_rejects_non_boolean_debug_overlay_setting(self):
        data = {**VALID, "render": {**VALID["render"], "debug_overlay": "true"}}
        with self.assertRaisesRegex(ConfigError, "render.debug_overlay"):
            validate_episode(data)


if __name__ == "__main__":
    unittest.main()
