"""Tests for verified source backup and preservation."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from holos_engine.backup import (
    BackupError,
    create_source_backup,
    restore_source_backup,
    inspect_restore_staging,
    _rename_directory_noreplace,
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

    def test_interrupted_restore_preserves_partial_stage_and_allows_safe_retry(self):
        inventory_path = self.inventory()
        backup_path, _ = create_source_backup(
            project_root=self.root,
            inventory_path=inventory_path,
            destination=Path("output/backups/interrupted-restore-test"),
        )

        real_copy2 = shutil.copy2
        copied_destinations = []

        def interrupt_after_one_copy(source, destination, *args, **kwargs):
            if len(copied_destinations) == 1:
                raise KeyboardInterrupt("simulated interruption during restore")
            result = real_copy2(source, destination, *args, **kwargs)
            copied_destinations.append(Path(destination))
            return result

        with patch("holos_engine.backup.shutil.copy2", side_effect=interrupt_after_one_copy):
            with self.assertRaisesRegex(KeyboardInterrupt, "simulated interruption"):
                restore_source_backup(
                    project_root=self.root,
                    backup_path=backup_path,
                    destination=Path("output/restores/interrupted-target"),
                )

        self.assertEqual(len(copied_destinations), 1)
        restores_root = self.root / "output" / "restores"
        interrupted_dirs = sorted(restores_root.glob("INTERRUPTED-*"))
        self.assertEqual(len(interrupted_dirs), 1)
        interrupted_dir = interrupted_dirs[0]
        interruption = json.loads(
            (interrupted_dir / "restore-interruption.json").read_text(encoding="utf-8")
        )
        self.assertEqual(interruption["status"], "interrupted")
        self.assertEqual(len(interruption["verified_files_before_failure"]), 1)
        self.assertIn("new, unused", interruption["recovery_guidance"])
        self.assertTrue(any(interrupted_dir.rglob("*") ))

        restored, manifest = restore_source_backup(
            project_root=self.root,
            backup_path=backup_path,
            destination=Path("output/restores/retry-after-interruption"),
        )
        self.assertEqual(manifest["status"], "complete")
        self.assertEqual(manifest["file_count"], 2)
        self.assertTrue((restored / "README.md").is_file())
        self.assertTrue((restored / "holos_engine" / "module.py").is_file())
        self.assertTrue(interrupted_dir.is_dir())
        self.assertTrue((backup_path / "backup-manifest.json").is_file())


    def test_restore_staging_inspection_is_read_only_and_classifies_lease_states(self):
        restores_root = self.root / "output" / "restores"
        restores_root.mkdir(parents=True)
        active = restores_root / ".restore-staging-active"
        expired = restores_root / ".restore-staging-expired"
        extended = restores_root / ".restore-staging-extended"
        wrong_ttl = restores_root / ".restore-staging-wrong-ttl"
        malformed = restores_root / ".restore-staging-malformed"
        missing = restores_root / ".restore-staging-missing"
        for directory in (active, expired, extended, wrong_ttl, malformed, missing):
            directory.mkdir()

        def lease_for(stage, expires, heartbeat, ttl=86400):
            return {
                "schema_version": 1,
                "stage_name": stage.name,
                "pid": 987654,
                "hostname": "another-host",
                "process_start_token": None,
                "heartbeat_at_epoch": heartbeat,
                "heartbeat_at_utc": "1970-01-01T00:00:00Z",
                "lease_expires_at_epoch": expires,
                "lease_ttl_seconds": ttl,
            }

        active_marker = active / ".restore-lease.json"
        expired_marker = expired / ".restore-lease.json"
        extended_marker = extended / ".restore-lease.json"
        wrong_ttl_marker = wrong_ttl / ".restore-lease.json"
        malformed_marker = malformed / ".restore-lease.json"
        active_marker.write_text(json.dumps(lease_for(active, 87300, 900)), encoding="utf-8")
        expired_marker.write_text(json.dumps(lease_for(expired, 950, -85450)), encoding="utf-8")
        extended_marker.write_text(json.dumps(lease_for(extended, 200000, 800)), encoding="utf-8")
        wrong_ttl_marker.write_text(json.dumps(lease_for(wrong_ttl, 900, 800, ttl=172800)), encoding="utf-8")
        malformed_marker.write_text("{not-json", encoding="utf-8")
        before = {
            path.name: tuple(sorted(item.name for item in path.iterdir()))
            for path in (active, expired, extended, wrong_ttl, malformed, missing)
        }

        findings = inspect_restore_staging(project_root=self.root, now_epoch=1000)
        by_name = {item["stage_name"]: item for item in findings}

        self.assertEqual(by_name[active.name]["status"], "active_lease")
        self.assertEqual(by_name[expired.name]["status"], "expired_candidate")
        self.assertEqual(by_name[extended.name]["status"], "unknown")
        self.assertEqual(by_name[wrong_ttl.name]["status"], "unknown")
        self.assertEqual(by_name[malformed.name]["status"], "unknown")
        self.assertEqual(by_name[missing.name]["status"], "unknown")
        self.assertIn("manual-review", by_name[expired.name]["reason"])
        after = {
            path.name: tuple(sorted(item.name for item in path.iterdir()))
            for path in (active, expired, extended, wrong_ttl, malformed, missing)
        }
        self.assertEqual(after, before)
        self.assertTrue(all(path.is_dir() for path in (active, expired, extended, wrong_ttl, malformed, missing)))
        self.assertFalse(any(path.name.startswith(("FAILED-", "INTERRUPTED-")) for path in restores_root.iterdir()))

    def test_restore_staging_inspection_checks_process_start_identity(self):
        restores_root = self.root / "output" / "restores"
        stage = restores_root / ".restore-staging-owner"
        stage.mkdir(parents=True)
        (stage / ".restore-lease.json").write_text(json.dumps({
            "schema_version": 1,
            "stage_name": stage.name,
            "pid": 12345,
            "hostname": "local-host",
            "process_start_token": "recorded-start",
            "heartbeat_at_epoch": 900,
            "heartbeat_at_utc": "1970-01-01T00:15:00Z",
            "lease_expires_at_epoch": 87300,
            "lease_ttl_seconds": 86400,
        }), encoding="utf-8")

        with patch("holos_engine.backup.socket.gethostname", return_value="local-host"):
            with patch("holos_engine.backup._process_start_token", return_value="recorded-start"):
                active = inspect_restore_staging(project_root=self.root, now_epoch=1000)
            with patch("holos_engine.backup._process_start_token", return_value="reused-pid-start"):
                mismatch = inspect_restore_staging(project_root=self.root, now_epoch=1000)

        self.assertEqual(active[0]["status"], "active_process")
        self.assertEqual(mismatch[0]["status"], "owner_identity_mismatch")
        self.assertIn("manual review", mismatch[0]["reason"])

    def test_restore_staging_inspection_rejects_invalid_inspection_time(self):
        with self.assertRaisesRegex(ValueError, "finite numeric epoch"):
            inspect_restore_staging(project_root=self.root, now_epoch=float("nan"))

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


    def test_cli_inspect_restores_reports_expired_stage_without_mutation(self):
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

            stage = root / "output" / "restores" / ".restore-staging-expired"
            stage.mkdir(parents=True)
            marker_path = stage / ".restore-lease.json"
            marker_path.write_text(json.dumps({
                "schema_version": 1,
                "stage_name": stage.name,
                "pid": 987654,
                "hostname": "another-host",
                "process_start_token": None,
                "heartbeat_at_epoch": -86398,
                "heartbeat_at_utc": "1970-01-01T00:00:01Z",
                "lease_expires_at_epoch": 2,
                "lease_ttl_seconds": 86400,
            }), encoding="utf-8")
            before = {
                path.name: path.read_bytes()
                for path in stage.iterdir()
            }

            result = subprocess.run(
                [
                    sys.executable, str(root / "tools" / "holos.py"),
                    "--project-root", str(root), "inspect-restores",
                ],
                cwd=root, capture_output=True, text=True, timeout=30, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            report = json.loads(result.stdout)
            self.assertTrue(report["read_only"])
            self.assertEqual(report["stage_count"], 1)
            self.assertEqual(report["status_counts"], {"expired_candidate": 1})
            self.assertEqual(
                report["stages"][0]["stage_name"], ".restore-staging-expired"
            )
            self.assertEqual(report["stages"][0]["status"], "expired_candidate")
            after = {path.name: path.read_bytes() for path in stage.iterdir()}
            self.assertEqual(after, before)
            self.assertTrue(stage.is_dir())
            self.assertFalse(any(
                path.name.startswith(("FAILED-", "INTERRUPTED-"))
                for path in stage.parent.iterdir()
            ))


    def test_concurrent_directory_promotion_never_replaces_destination(self):
        if not sys.platform.startswith("linux"):
            self.skipTest("The atomic renameat2 race test requires Linux.")
        parent = self.root / "output" / "restores"
        parent.mkdir(parents=True)
        destination = parent / "race-target"
        stages = [parent / ".race-stage-a", parent / ".race-stage-b"]
        for stage, payload in zip(stages, ("A", "B")):
            stage.mkdir()
            (stage / "payload.txt").write_text(payload, encoding="utf-8")

        barrier = threading.Barrier(2)
        results = []
        results_lock = threading.Lock()

        def promote(stage):
            barrier.wait(timeout=5)
            try:
                _rename_directory_noreplace(stage, destination)
                outcome = "moved"
            except BackupError as exc:
                outcome = (
                    "refused" if "Refusing to overwrite existing destination" in str(exc)
                    else f"unexpected:{exc}"
                )
            with results_lock:
                results.append((outcome, stage))

        workers = [
            threading.Thread(target=promote, args=(stage,))
            for stage in stages
        ]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(timeout=10)
        self.assertTrue(all(not worker.is_alive() for worker in workers))
        self.assertCountEqual([outcome for outcome, _ in results], ["moved", "refused"])

        winner = next(stage for outcome, stage in results if outcome == "moved")
        loser = next(stage for outcome, stage in results if outcome == "refused")
        self.assertTrue(destination.is_dir())
        self.assertFalse(winner.exists())
        self.assertTrue(loser.is_dir())
        self.assertTrue((loser / "payload.txt").is_file())
        self.assertEqual(
            (destination / "payload.txt").read_text(encoding="utf-8"),
            "A" if winner.name.endswith("a") else "B",
        )
        self.assertEqual(
            (loser / "payload.txt").read_text(encoding="utf-8"),
            "B" if loser.name.endswith("b") else "A",
        )


if __name__ == "__main__":
    unittest.main()
