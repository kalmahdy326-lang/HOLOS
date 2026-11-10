"""Tests for the read-only Godot resource dependency audit."""

from pathlib import Path
import tempfile
import unittest

from holos_engine.godot_assets import (
    GodotAssetAuditError,
    audit_godot_project,
)


class GodotAssetAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.project = self.root / "godot"
        self.project.mkdir()
        (self.project / "project.godot").write_text(
            '[application]\nconfig/name="Audit Test"\n', encoding="utf-8"
        )
        (self.project / "scenes").mkdir()
        (self.project / "scripts").mkdir()
        (self.project / "assets").mkdir()
        (self.project / "assets" / "texture.png").write_bytes(b"texture")
        (self.project / "scripts" / "actor.gd").write_text(
            'const TEXTURE = preload("res://assets/texture.png")\n'
            'const UID_SCENE = "uid://abc123"\n',
            encoding="utf-8",
        )
        (self.project / "scenes" / "actor.tscn").write_text(
            '[gd_scene load_steps=2 format=3]\n'
            '[ext_resource type="Script" path="res://scripts/actor.gd" id="1"]\n',
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_resolves_existing_literal_resource_paths(self):
        report = audit_godot_project(
            project_root=self.root, godot_project=Path("godot")
        )
        self.assertEqual(report["status"], "complete")
        self.assertEqual(report["summary"]["missing_reference_count"], 0)
        self.assertEqual(report["summary"]["resolved_reference_count"], 2)
        self.assertEqual(report["summary"]["uid_reference_count"], 1)

    def test_reports_missing_resource_reference(self):
        scene = self.project / "scenes" / "actor.tscn"
        scene.write_text(
            scene.read_text(encoding="utf-8")
            + '[ext_resource type="Texture2D" path="res://assets/missing.png" id="2"]\n',
            encoding="utf-8",
        )
        report = audit_godot_project(project_root=self.root, godot_project=Path("godot"))
        self.assertEqual(report["status"], "issues_found")
        self.assertEqual(report["summary"]["missing_reference_count"], 1)
        self.assertEqual(report["missing"][0]["resource_path"], "assets/missing.png")

    def test_reports_unsafe_traversal_reference(self):
        scene = self.project / "scenes" / "actor.tscn"
        scene.write_text(
            scene.read_text(encoding="utf-8")
            + '[ext_resource path="res://../outside.tres" id="2"]\n',
            encoding="utf-8",
        )
        report = audit_godot_project(project_root=self.root, godot_project=Path("godot"))
        self.assertEqual(report["summary"]["unsafe_reference_count"], 1)
        self.assertEqual(
            report["unsafe"][0]["reason"],
            "resource_path_is_not_a_safe_project_relative_path",
        )

    def test_refuses_project_path_symlink(self):
        link = self.root / "linked-godot"
        try:
            link.symlink_to(self.project, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Directory symlinks are unavailable on this platform.")
        with self.assertRaisesRegex(GodotAssetAuditError, "symbolic links"):
            audit_godot_project(project_root=self.root, godot_project=Path("linked-godot"))

    def test_reports_resource_symlink_as_unsafe(self):
        target = self.project / "assets" / "texture.png"
        link = self.project / "assets" / "linked.png"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("File symlinks are unavailable on this platform.")
        (self.project / "scripts" / "actor.gd").write_text(
            'const LINK = preload("res://assets/linked.png")\n',
            encoding="utf-8",
        )
        report = audit_godot_project(project_root=self.root, godot_project=Path("godot"))
        self.assertEqual(report["summary"]["unsafe_reference_count"], 1)

    def test_ignores_generated_cache_directories(self):
        cache = self.project / ".godot"
        cache.mkdir()
        (cache / "generated.gd").write_text(
            'const MISSING = preload("res://assets/not-real.png")\n',
            encoding="utf-8",
        )
        report = audit_godot_project(project_root=self.root, godot_project=Path("godot"))
        self.assertEqual(report["summary"]["missing_reference_count"], 0)
        self.assertTrue(any(
            item["path"] == ".godot" for item in report["skipped"]
        ))


if __name__ == "__main__":
    unittest.main()
