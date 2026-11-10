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
            self.root / "output" / "renders" / "batch_test" / "production" / "S01_B01" / "frame_000001.png"
        )
        missing.unlink()
        result = render_episode_batch(
            project_root=self.root, episode=EPISODE, mode="production", render_one=renderer,
        )
        self.assertTrue(result["success"])
        self.assertIn("S01_B01", result["completed_this_run"])
        self.assertTrue(list((self.root / "output" / "recovery").glob("S01_B01-*")))


    def test_refuses_shot_output_symlink_without_moving_its_target(self):
        calls = []
        target = self.root / "output" / "preserved"
        target.mkdir(parents=True)
        sentinel = target / "do-not-touch.txt"
        sentinel.write_text("preserve", encoding="utf-8")
        link = (
            self.root / "output" / "renders" / "batch_test"
            / "debug" / "S01_B01"
        )
        link.parent.mkdir(parents=True)
        try:
            link.symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Directory symlinks are unavailable on this platform.")

        with self.assertRaisesRegex(BatchRenderError, "symbolic links"):
            render_episode_batch(
                project_root=self.root, episode=EPISODE, mode="debug",
                render_one=self.make_renderer(calls),
            )
        self.assertTrue(link.is_symlink())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve")
        self.assertEqual(calls, [])

    def test_refuses_manifest_directory_symlink(self):
        preserved = self.root / "output" / "preserved-manifests"
        preserved.mkdir(parents=True)
        marker = preserved / "marker.txt"
        marker.write_text("preserve", encoding="utf-8")
        manifest_link = self.root / "output" / "manifests"
        manifest_link.parent.mkdir(parents=True)
        try:
            manifest_link.symlink_to(preserved, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Directory symlinks are unavailable on this platform.")

        with self.assertRaisesRegex(BatchRenderError, "symbolic links"):
            render_episode_batch(
                project_root=self.root, episode=EPISODE, mode="debug",
                render_one=self.make_renderer([]),
            )
        self.assertEqual(marker.read_text(encoding="utf-8"), "preserve")
        self.assertFalse(list(preserved.glob("*render.json")))

    def test_refuses_recovery_directory_symlink_before_archiving(self):
        calls = []
        renderer = self.make_renderer(calls, fail_once="S01_B02")
        first = render_episode_batch(
            project_root=self.root, episode=EPISODE, mode="debug", render_one=renderer,
        )
        self.assertFalse(first["success"])
        partial = (
            self.root / "output" / "renders" / "batch_test"
            / "debug" / "S01_B02"
        )
        preserved = self.root / "output" / "preserved-recovery"
        preserved.mkdir(parents=True)
        marker = preserved / "marker.txt"
        marker.write_text("preserve", encoding="utf-8")
        recovery_link = self.root / "output" / "recovery"
        try:
            recovery_link.symlink_to(preserved, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Directory symlinks are unavailable on this platform.")

        with self.assertRaisesRegex(BatchRenderError, "symbolic links"):
            render_episode_batch(
                project_root=self.root, episode=EPISODE, mode="debug",
                render_one=renderer,
            )
        self.assertTrue(partial.is_dir())
        self.assertEqual(marker.read_text(encoding="utf-8"), "preserve")


    def test_refuses_manifest_with_duplicate_or_out_of_order_shot_records(self):
        calls = []
        render_episode_batch(
            project_root=self.root, episode=EPISODE, mode="debug",
            render_one=self.make_renderer(calls),
        )
        manifest_path = (
            self.root / "output" / "manifests" / "batch_test-debug-render.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["shots"][1]["shot_id"] = manifest["shots"][0]["shot_id"]
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        with self.assertRaisesRegex(BatchRenderError, "duplicate shot"):
            render_episode_batch(
                project_root=self.root, episode=EPISODE, mode="debug",
                render_one=self.make_renderer([]),
            )

    def test_refuses_manifest_with_invalid_attempt_metadata(self):
        calls = []
        render_episode_batch(
            project_root=self.root, episode=EPISODE, mode="debug",
            render_one=self.make_renderer(calls),
        )
        manifest_path = (
            self.root / "output" / "manifests" / "batch_test-debug-render.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["shots"][0]["attempts"] = -1
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        with self.assertRaisesRegex(BatchRenderError, "attempt count"):
            render_episode_batch(
                project_root=self.root, episode=EPISODE, mode="debug",
                render_one=self.make_renderer([]),
            )


if __name__ == "__main__":
    unittest.main()
