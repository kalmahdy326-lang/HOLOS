"""Tests for verified source backup and preservation."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from holos_engine.backup import (
    BackupError,
    create_source_backup,
    restore_source_backup,
)
from holos_engine.inventory import write_inventory_report


class SourceBackupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "holos_engine").mkdir()
        (self.root / "holos_engine" / "module.py").write_text(
            "print('HOLOS')\n", encoding="utf-8"
        )
        (self.root / "README.md").write_text("Project source\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def inventory(self) -> Path:
        path, _ = write_inventory_report(
            self.root, Path("output/reports/source-inventory-test.json")
        )
        return path

    def test_creates_verified_copy_without_modifying_sources(self):
        inventory_path = self.inventory()
        original = (self.root / "holos_engine" / "module.py").read_bytes()
        backup_path, manifest = create_source_backup(
            project_root=self.root,
            inventory_path=inventory_path,
            destination=Path("output/backups/test-backup"),
        )
        self.assertEqual(manifest["status"], "complete")
        self.assertEqual(manifest["file_count"], 2)
        restored = backup_path / "files" / "holos_engine" / "module.py"
        self.assertEqual(restored.read_bytes(), original)
        self.assertEqual(
            hashlib.sha256(restored.read_bytes()).hexdigest(),
            next(item for item in manifest["files"]
                 if item["source_path"] == "holos_engine/module.py")["sha256"],
        )
        self.assertEqual((self.root / "holos_engine" / "module.py").read_bytes(), original)
        saved_manifest = json.loads(
            (backup_path / "backup-manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(saved_manifest["status"], "complete")

    def test_refuses_backup_when_source_changed_since_inventory(self):
        inventory_path = self.inventory()
        (self.root / "README.md").write_text("changed\n", encoding="utf-8")
        with self.assertRaisesRegex(BackupError, "Source changed after inventory"):
            create_source_backup(
                project_root=self.root,
                inventory_path=inventory_path,
                destination=Path("output/backups/should-not-exist"),
            )
        self.assertFalse((self.root / "output" / "backups").exists())

    def test_refuses_existing_backup_destination(self):
        inventory_path = self.inventory()
        destination = self.root / "output" / "backups" / "existing"
        destination.mkdir(parents=True)
        with self.assertRaisesRegex(BackupError, "Refusing to overwrite"):
            create_source_backup(
                project_root=self.root,
                inventory_path=inventory_path,
                destination=destination,
            )

    def test_rejects_inventory_path_traversal(self):
        inventory_path = self.inventory()
        data = json.loads(inventory_path.read_text(encoding="utf-8"))
        data["files"][0]["path"] = "../outside.txt"
        inventory_path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(BackupError, "safe relative path"):
            create_source_backup(
                project_root=self.root,
                inventory_path=inventory_path,
            )

    def test_rejects_inventory_for_another_project(self):
        inventory_path = self.inventory()
        other = self.root.parent / f"{self.root.name}-other"
        other.mkdir()
        try:
            with self.assertRaisesRegex(BackupError, "inside output/reports"):
                create_source_backup(
                    project_root=other,
                    inventory_path=inventory_path,
                )
        finally:
            other.rmdir()

    def test_rejects_secret_path_in_tampered_inventory(self):
        inventory_path = self.inventory()
        data = json.loads(inventory_path.read_text(encoding="utf-8"))
        data["files"][0]["path"] = ".env"
        inventory_path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(BackupError, "Sensitive filename"):
            create_source_backup(
                project_root=self.root,
                inventory_path=inventory_path,
            )

    def test_cli_runs_inventory_then_backup_without_episode_configuration(self):
        source_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(
                source_root / "holos_engine",
                root / "holos_engine",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            (root / "tools").mkdir()
            shutil.copy2(source_root / "tools" / "holos.py", root / "tools" / "holos.py")
            (root / "notes.txt").write_text("backup source", encoding="utf-8")
            inventory_path = "output/reports/backup-cli-inventory.json"
            inventory_run = subprocess.run(
                [
                    sys.executable, str(root / "tools" / "holos.py"),
                    "--project-root", str(root), "inventory", "--output", inventory_path,
                ],
                cwd=root, capture_output=True, text=True, timeout=30, check=False,
            )
            self.assertEqual(
                inventory_run.returncode, 0,
                inventory_run.stderr or inventory_run.stdout,
            )
            backup_run = subprocess.run(
                [
                    sys.executable, str(root / "tools" / "holos.py"),
                    "--project-root", str(root), "backup",
                    "--inventory", inventory_path,
                    "--destination", "output/backups/cli-test",
                ],
                cwd=root, capture_output=True, text=True, timeout=30, check=False,
            )
            self.assertEqual(backup_run.returncode, 0, backup_run.stderr or backup_run.stdout)
            backed_up = root / "output" / "backups" / "cli-test" / "files" / "notes.txt"
            self.assertEqual(backed_up.read_text(encoding="utf-8"), "backup source")
            manifest = json.loads(
                (root / "output" / "backups" / "cli-test" / "backup-manifest.json")
                .read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["status"], "complete")

            restored_dir = root / "output" / "restores" / "cli-restored"
            restore_run = subprocess.run(
                [
                    sys.executable, str(root / "tools" / "holos.py"),
                    "--project-root", str(root), "restore",
                    "--backup", "output/backups/cli-test",
                    "--destination", "output/restores/cli-restored",
                ],
                cwd=root, capture_output=True, text=True, timeout=30, check=False,
            )
            self.assertEqual(restore_run.returncode, 0, restore_run.stderr or restore_run.stdout)
            self.assertEqual(
                (restored_dir / "notes.txt").read_text(encoding="utf-8"),
                "backup source",
            )
            self.assertEqual(
                (root / "output" / "backups" / "cli-test" / "files" / "notes.txt")
                .read_text(encoding="utf-8"),
                "backup source",
            )

    def test_restores_only_to_a_new_directory_and_keeps_backup(self):
        inventory_path = self.inventory()
        backup_path, _ = create_source_backup(
            project_root=self.root,
            inventory_path=inventory_path,
            destination=Path("output/backups/restore-test"),
        )
        restored, manifest = restore_source_backup(
            project_root=self.root,
            backup_path=backup_path,
            destination=Path("output/restores/restore-test"),
        )
        self.assertEqual(manifest["status"], "complete")
        self.assertEqual(
            (restored / "holos_engine" / "module.py").read_bytes(),
            (self.root / "holos_engine" / "module.py").read_bytes(),
        )
        self.assertTrue((backup_path / "backup-manifest.json").is_file())

    def test_rejects_backup_file_and_manifest_record_changed_together(self):
        inventory_path = self.inventory()
        backup_path, _ = create_source_backup(
            project_root=self.root,
            inventory_path=inventory_path,
            destination=Path("output/backups/record-tamper-test"),
        )
        manifest_path = backup_path / "backup-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        record = next(item for item in manifest["files"]
                      if item["source_path"] == "README.md")
        changed = b"replacement payload with a different length"
        backup_file = backup_path / record["backup_path"]
        backup_file.write_bytes(changed)
        # Simulate an accidental or partial manifest rewrite that makes the
        # per-file hash and total-size checks agree with the changed payload.
        record["sha256"] = hashlib.sha256(changed).hexdigest()
        record["size_bytes"] = len(changed)
        manifest["total_size_bytes"] = sum(
            item["size_bytes"] for item in manifest["files"]
        )
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        with self.assertRaisesRegex(
            BackupError, "source inventory aggregate hash"
        ):
            restore_source_backup(
                project_root=self.root,
                backup_path=backup_path,
            )

    def test_refuses_restore_when_backup_file_is_corrupted(self):
        inventory_path = self.inventory()
        backup_path, _ = create_source_backup(
            project_root=self.root,
            inventory_path=inventory_path,
            destination=Path("output/backups/corrupt-test"),
        )
        (backup_path / "files" / "README.md").write_text("corrupt", encoding="utf-8")
        with self.assertRaisesRegex(BackupError, "failed integrity verification"):
            restore_source_backup(project_root=self.root, backup_path=backup_path)

    def test_refuses_existing_restore_directory(self):
        inventory_path = self.inventory()
        backup_path, _ = create_source_backup(
            project_root=self.root,
            inventory_path=inventory_path,
        )
        existing = self.root / "output" / "restores" / "already-here"
        existing.mkdir(parents=True)
        with self.assertRaisesRegex(BackupError, "Refusing to overwrite"):
            restore_source_backup(
                project_root=self.root,
                backup_path=backup_path,
                destination=existing,
            )


if __name__ == "__main__":
    unittest.main()
