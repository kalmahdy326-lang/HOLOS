"""Tests for read-only HOLOS source inventory generation."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from holos_engine.inventory import (
    InventoryError,
    build_inventory,
    write_inventory_report,
)


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_hashes_regular_source_files_in_sorted_order(self):
        (self.root / "README.md").write_text("HOLOS", encoding="utf-8")
        (self.root / "zeta.txt").write_bytes(b"zeta")
        (self.root / "alpha.txt").write_bytes(b"alpha")

        result = build_inventory(self.root)
        paths = [item["path"] for item in result["files"]]
        self.assertEqual(paths, ["README.md", "alpha.txt", "zeta.txt"])
        alpha = next(item for item in result["files"] if item["path"] == "alpha.txt")
        self.assertEqual(alpha["size_bytes"], 5)
        self.assertEqual(alpha["sha256"], hashlib.sha256(b"alpha").hexdigest())
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["summary"]["file_count"], 3)

    def test_excludes_generated_directories_and_sensitive_file_names(self):
        (self.root / "output" / "renders").mkdir(parents=True)
        (self.root / "output" / "renders" / "frame.png").write_bytes(b"frame")
        (self.root / ".git").mkdir()
        (self.root / ".git" / "config").write_text("git", encoding="utf-8")
        (self.root / "__pycache__").mkdir()
        (self.root / "__pycache__" / "cache.pyc").write_bytes(b"cache")
        (self.root / ".env").write_text("secret", encoding="utf-8")
        (self.root / "signing.pem").write_text("secret", encoding="utf-8")
        (self.root / "source.py").write_text("print('ok')", encoding="utf-8")

        result = build_inventory(self.root)
        self.assertEqual([item["path"] for item in result["files"]], ["source.py"])
        skipped_paths = {item["path"] for item in result["skipped"]}
        self.assertIn("output", skipped_paths)
        self.assertIn(".git", skipped_paths)
        self.assertIn("__pycache__", skipped_paths)
        self.assertIn(".env", skipped_paths)
        self.assertIn("signing.pem", skipped_paths)

    def test_does_not_follow_symlinks(self):
        target = self.root.parent / f"{self.root.name}-outside.txt"
        target.write_text("outside", encoding="utf-8")
        link = self.root / "outside-link.txt"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks are not available on this platform")
        try:
            result = build_inventory(self.root)
            self.assertEqual(result["files"], [])
            self.assertEqual(result["skipped"], [{
                "path": "outside-link.txt",
                "reason": "symlink_file_not_followed",
            }])
        finally:
            target.unlink(missing_ok=True)

    def test_writes_report_atomically_and_refuses_overwrite(self):
        (self.root / "notes.txt").write_text("inventory", encoding="utf-8")
        destination = Path("output/reports/inventory-test.json")
        report_path, result = write_inventory_report(self.root, destination)
        self.assertTrue(report_path.is_file())
        loaded = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(loaded["summary"]["inventory_sha256"],
                         result["summary"]["inventory_sha256"])
        with self.assertRaisesRegex(InventoryError, "Refusing to overwrite"):
            write_inventory_report(self.root, destination)

    def test_rejects_output_path_outside_project(self):
        outside = self.root.parent / f"{self.root.name}-report.json"
        with self.assertRaisesRegex(InventoryError, "Inventory report must be written"):
            write_inventory_report(self.root, outside)


    def test_cli_creates_inventory_without_episode_configuration(self):
        source_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "holos_engine").mkdir()
            (root / "tools").mkdir()
            shutil.copytree(
                source_root / "holos_engine",
                root / "holos_engine",
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            shutil.copy2(source_root / "tools" / "holos.py", root / "tools" / "holos.py")
            (root / "notes.txt").write_text("source record", encoding="utf-8")
            output = Path("output/reports/cli-inventory.json")
            result = subprocess.run(
                [
                    sys.executable,
                    str(root / "tools" / "holos.py"),
                    "--project-root", str(root),
                    "inventory",
                    "--output", str(output),
                ],
                cwd=root,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            report_path = root / output
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "complete")
            self.assertIn(
                "notes.txt", [item["path"] for item in report["files"]]
            )
            self.assertNotIn(
                "output/reports/cli-inventory.json",
                [item["path"] for item in report["files"]],
            )

    def test_rejects_inventory_report_outside_reports_directory(self):
        with self.assertRaisesRegex(InventoryError, "under output/reports"):
            write_inventory_report(self.root, Path("README-inventory.json"))


    def test_inventory_file_list_and_aggregate_hash_are_reproducible(self):
        (self.root / "zeta.txt").write_bytes(b"zeta")
        (self.root / "alpha.txt").write_bytes(b"alpha")
        first = build_inventory(self.root)
        second = build_inventory(self.root)
        self.assertEqual(first["files"], second["files"])
        self.assertEqual(
            first["summary"]["inventory_sha256"],
            second["summary"]["inventory_sha256"],
        )

    def test_hash_read_failure_marks_inventory_partial(self):
        (self.root / "unreadable.txt").write_text("source", encoding="utf-8")
        with patch("holos_engine.inventory._sha256", side_effect=OSError("read denied")):
            result = build_inventory(self.root)
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["summary"]["error_count"], 1)
        self.assertEqual(result["errors"][0]["path"], "unreadable.txt")
        self.assertEqual(result["files"], [])


if __name__ == "__main__":
    unittest.main()
