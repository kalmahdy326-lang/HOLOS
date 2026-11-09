"""Tests for ordered and resumable batch rendering."""

import json
from pathlib import Path
import tempfile
import unittest

from holos_engine.batch import BatchRenderError, render_episode_batch


EPISODE = {
    "schema_version": 1,
    "episode_id": "batch_test",
    "title": "Batch Test",
    "render": {"width": 320, "height": 180, "fps": 24},
    "audio": {"dialogue": None, "music": None},
    "scenes": [
        {"scene_id": "scene_01", "shots": [
            {"shot_id": "S01_B01", "start_frame": 0, "end_frame": 2},
            {"shot_id": "S01_B02", "start_frame": 2, "end_frame": 5},
        ]},
        {"scene_id": "scene_02", "shots": [
            {"shot_id": "S02_B01", "start_frame": 0, "end_frame": 1},
        ]},
    ],
}


class BatchRenderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def make_renderer(self, calls, fail_once=None):
        failed = set()

        def render(scene, shot, output_dir):
            calls.append((scene["scene_id"], shot["shot_id"]))
            if fail_once == shot["shot_id"] and shot["shot_id"] not in failed:
                failed.add(shot["shot_id"])
                output_dir.mkdir(parents=True, exist_ok=True)
                (output_dir / "partial.tmp").write_text("partial", encoding="utf-8")
                raise RuntimeError("synthetic render failure")
            output_dir.mkdir(parents=True, exist_ok=True)
            count = shot["end_frame"] - shot["start_frame"]
            for index in range(count):
                (output_dir / f"frame_{index:06d}.png").write_bytes(b"png-test")
            return {
                "return_code": 0,
                "frame_count": count,
                "first_frame": str(output_dir / "frame_000000.png"),
                "last_frame": str(output_dir / f"frame_{count - 1:06d}.png"),
            }

        return render

    def test_renders_all_shots_in_scene_order(self):
        calls = []
        result = render_episode_batch(
            project_root=self.root, episode=EPISODE, mode="debug",
            render_one=self.make_renderer(calls),
        )
        self.assertTrue(result["success"])
        self.assertEqual(
            calls,
            [("scene_01", "S01_B01"), ("scene_01", "S01_B02"),
             ("scene_02", "S02_B01")],
        )
        self.assertEqual(result["status_counts"]["completed"], 3)

    def test_resume_skips_only_verified_completed_shots(self):
        calls = []
        renderer = self.make_renderer(calls)
        first = render_episode_batch(
            project_root=self.root, episode=EPISODE, mode="debug", render_one=renderer,
        )
        second = render_episode_batch(
            project_root=self.root, episode=EPISODE, mode="debug", render_one=renderer,
        )
        self.assertTrue(first["success"])
        self.assertTrue(second["success"])
        self.assertEqual(len(calls), 3)
        self.assertEqual(second["skipped_verified"], ["S01_B01", "S01_B02", "S02_B01"])

    def test_failed_partial_output_is_archived_before_retry(self):
        calls = []
        renderer = self.make_renderer(calls, fail_once="S01_B02")
        first = render_episode_batch(
            project_root=self.root, episode=EPISODE, mode="debug", render_one=renderer,
        )
        self.assertFalse(first["success"])
        self.assertEqual(first["failed_this_run"], ["S01_B02"])

        second = render_episode_batch(
            project_root=self.root, episode=EPISODE, mode="debug", render_one=renderer,
        )
        self.assertTrue(second["success"])
        self.assertIn("S01_B02", second["completed_this_run"])
        self.assertTrue(list((self.root / "output" / "recovery").glob("S01_B02-*")))

    def test_config_mismatch_refuses_to_resume(self):
        calls = []
        render_episode_batch(
            project_root=self.root, episode=EPISODE, mode="debug",
            render_one=self.make_renderer(calls),
        )
        changed = json.loads(json.dumps(EPISODE))
        changed["title"] = "Changed title"
        with self.assertRaisesRegex(BatchRenderError, "different episode configuration"):
            render_episode_batch(
                project_root=self.root, episode=changed, mode="debug",
                render_one=self.make_renderer([]),
            )

    def test_completed_shot_with_missing_frame_is_recovered_and_rendered_again(self):
        calls = []
        renderer = self.make_renderer(calls)
        render_episode_batch(
            project_root=self.root, episode=EPISODE, mode="production", render_one=renderer,
        )
        missing = (
            self.root / "output" / "renders" / "batch_test" / "S01_B01" / "frame_000001.png"
        )
        missing.unlink()
        result = render_episode_batch(
            project_root=self.root, episode=EPISODE, mode="production", render_one=renderer,
        )
        self.assertTrue(result["success"])
        self.assertIn("S01_B01", result["completed_this_run"])
        self.assertTrue(list((self.root / "output" / "recovery").glob("S01_B01-*")))


if __name__ == "__main__":
    unittest.main()
