"""Verified, non-destructive source backup from a SHA-256 inventory."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import fnmatch
import os
import math
import socket
import time
from pathlib import Path, PurePosixPath
import shutil

from holos_engine.inventory import EXCLUDED_DIRECTORIES, SENSITIVE_FILE_PATTERNS
import tempfile
from typing import Any


class BackupError(RuntimeError):
    """Raised when a source backup cannot be completed safely."""


def _inside(root: Path, path: Path) -> bool:
    return path == root or root in path.parents


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative_path(value: Any) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value:
        raise BackupError(f"Invalid inventory path: {value!r}")
    relative = PurePosixPath(value)
    if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
        raise BackupError(f"Inventory path is not a safe relative path: {value!r}")
    if relative.parts and ":" in relative.parts[0]:
        raise BackupError(f"Drive-qualified inventory path is not allowed: {value!r}")
    return relative


def _validated_inventory(
    *,
    root: Path,
    inventory_path: Path,
) -> tuple[dict[str, Any], list[tuple[dict[str, Any], Path, PurePosixPath]]]:
    output_lexical = root / "output"
    reports_lexical = output_lexical / "reports"
    if output_lexical.is_symlink() or reports_lexical.is_symlink():
        raise BackupError("Inventory report directory must not use symbolic links.")
    reports_root = reports_lexical.resolve()
    candidate = inventory_path if inventory_path.is_absolute() else root / inventory_path
    if candidate.is_symlink():
        raise BackupError("Inventory report must not be a symbolic link.")
    resolved = candidate.resolve()
    if not _inside(root, resolved) or reports_root not in resolved.parents:
        raise BackupError("Inventory report must be inside output/reports.")
    if not resolved.is_file():
        raise BackupError(f"Inventory report does not exist: {resolved}")
    try:
        inventory = json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BackupError(f"Could not read inventory report: {exc}") from exc

    if not isinstance(inventory, dict) or inventory.get("schema_version") != 1:
        raise BackupError("Inventory report has an invalid or unsupported schema.")
    if Path(str(inventory.get("project_root", ""))).resolve() != root:
        raise BackupError("Inventory report belongs to a different project root.")
    if inventory.get("status") != "complete" or inventory.get("errors"):
        raise BackupError("Only a complete inventory with no traversal errors can be backed up.")
    records = inventory.get("files")
    if not isinstance(records, list):
        raise BackupError("Inventory report does not contain a valid files list.")

    validated: list[tuple[dict[str, Any], Path, PurePosixPath]] = []
    seen: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            raise BackupError("Inventory contains a malformed file record.")
        relative = _safe_relative_path(record.get("path"))
        normalized = relative.as_posix()
        if any(part in EXCLUDED_DIRECTORIES for part in relative.parts):
            raise BackupError(f"Generated or dependency path is not eligible for backup: {normalized}")
        if any(
            fnmatch.fnmatchcase(relative.name, pattern)
            for pattern in SENSITIVE_FILE_PATTERNS
        ):
            raise BackupError(f"Sensitive filename is not eligible for backup: {normalized}")
        if normalized in seen:
            raise BackupError(f"Duplicate path in inventory: {normalized}")
        seen.add(normalized)

        source = root.joinpath(*relative.parts)
        current = root
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise BackupError(f"Symbolic-link source is not allowed: {normalized}")
        resolved_source = source.resolve()
        if not _inside(root, resolved_source) or not resolved_source.is_file():
            raise BackupError(f"Inventory source file is missing or unsafe: {normalized}")
        if (
            not isinstance(record.get("size_bytes"), int)
            or isinstance(record.get("size_bytes"), bool)
            or record["size_bytes"] < 0
        ):
            raise BackupError(f"Invalid file size in inventory: {normalized}")
        checksum = record.get("sha256")
        if (
            not isinstance(checksum, str)
            or len(checksum) != 64
            or any(character not in "0123456789abcdef" for character in checksum)
        ):
            raise BackupError(f"Invalid SHA-256 value in inventory: {normalized}")
        if _sha256(resolved_source) != record["sha256"]:
            raise BackupError(f"Source changed after inventory: {normalized}")
        validated.append((record, resolved_source, relative))

    summary = inventory.get("summary")
    if not isinstance(summary, dict):
        raise BackupError("Inventory report is missing its summary.")
    aggregate = hashlib.sha256()
    for record, _, relative in validated:
        aggregate.update(relative.as_posix().encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(record["sha256"].encode("ascii"))
        aggregate.update(b"\n")
    if aggregate.hexdigest() != summary.get("inventory_sha256"):
        raise BackupError("Inventory aggregate hash does not match its file records.")

    return inventory, validated


def create_source_backup(
    *,
    project_root: Path,
    inventory_path: Path,
    destination: Path | None = None,
) -> tuple[Path, dict[str, Any]]:
    """Copy and verify every inventoried file; never overwrite source or backup."""
    root = project_root.resolve()
    if not root.is_dir():
        raise BackupError(f"Project root is not a directory: {root}")

    inventory, files = _validated_inventory(
        root=root,
        inventory_path=inventory_path,
    )

    output_lexical = root / "output"
    backups_lexical = output_lexical / "backups"
    if output_lexical.is_symlink() or backups_lexical.is_symlink():
        raise BackupError("Backup directory must not use symbolic links.")
    backups_root = backups_lexical.resolve()
    if not _inside(root, backups_root) or backups_root == root:
        raise BackupError("Backup directory must remain inside project root.")
    backups_root.mkdir(parents=True, exist_ok=True)

    if destination is None:
        final_dir = backups_root / f"source-backup-{_stamp()}"
    else:
        final_dir = destination if destination.is_absolute() else root / destination
        final_dir = final_dir.resolve()

    if final_dir.parent != backups_root:
        raise BackupError("Backup destination must be a direct child of output/backups.")
    if final_dir.exists() or final_dir.is_symlink():
        raise BackupError(f"Refusing to overwrite existing backup: {final_dir}")

    stage = Path(tempfile.mkdtemp(prefix=".backup-staging-", dir=backups_root))
    copied_records: list[dict[str, Any]] = []
    try:
        files_root = stage / "files"
        files_root.mkdir()
        for record, source, relative in files:
            destination_file = files_root.joinpath(*relative.parts)
            if not _inside(files_root, destination_file):
                raise BackupError(f"Backup path escapes staging directory: {relative}")
            destination_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination_file)
            copied_hash = _sha256(destination_file)
            copied_size = destination_file.stat().st_size
            if copied_hash != record["sha256"] or copied_size != record["size_bytes"]:
                raise BackupError(f"Backup verification failed for {relative.as_posix()}.")
            copied_records.append({
                "source_path": relative.as_posix(),
                "backup_path": (Path("files") / Path(*relative.parts)).as_posix(),
                "size_bytes": copied_size,
                "sha256": copied_hash,
            })

        backup_manifest = {
            "schema_version": 1,
            "created_at_utc": _timestamp(),
            "status": "complete",
            "project_root": str(root),
            "source_inventory_path": str(
                (inventory_path if inventory_path.is_absolute()
                 else root / inventory_path).resolve().relative_to(root)
            ),
            "source_inventory_sha256": inventory["summary"]["inventory_sha256"],
            "file_count": len(copied_records),
            "total_size_bytes": sum(item["size_bytes"] for item in copied_records),
            "files": copied_records,
        }
        manifest_path = stage / "backup-manifest.json"
        with manifest_path.open("x", encoding="utf-8") as stream:
            json.dump(backup_manifest, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())

        if final_dir.exists():
            raise BackupError(f"Refusing to overwrite existing backup: {final_dir}")
        os.replace(stage, final_dir)
        return final_dir, backup_manifest

    except Exception as exc:
        if stage.exists():
            failed_dir = backups_root / f"FAILED-{_stamp()}"
            suffix = 1
            while failed_dir.exists():
                failed_dir = backups_root / f"FAILED-{_stamp()}-{suffix}"
                suffix += 1
            try:
                failure = {
                    "schema_version": 1,
                    "created_at_utc": _timestamp(),
                    "status": "incomplete",
                    "error": f"{type(exc).__name__}: {exc}",
                    "verified_files_before_failure": copied_records,
                }
                with (stage / "backup-failure.json").open("w", encoding="utf-8") as stream:
                    json.dump(failure, stream, indent=2)
                    stream.write("\n")
                os.replace(stage, failed_dir)
            except OSError:
                # Leave the staging directory in place if preservation itself fails.
                pass
            raise BackupError(
                f"Backup failed; partial staging was preserved at "
                f"{failed_dir if failed_dir.exists() else stage}: {exc}"
            ) from exc
        raise




RESTORE_LEASE_FILENAME = ".restore-lease.json"
RESTORE_LEASE_TTL_SECONDS = 24 * 60 * 60


def _process_start_token(pid: int) -> str | None:
    """Return Linux /proc start-time ticks to distinguish PID reuse when available."""
    stat_path = Path(f"/proc/{pid}/stat")
    try:
        stat_text = stat_path.read_text(encoding="utf-8")
        closing = stat_text.rfind(")")
        if closing < 0:
            return None
        fields = stat_text[closing + 1:].strip().split()
        return fields[19] if len(fields) > 19 else None
    except (OSError, UnicodeError):
        return None


def _write_restore_lease(stage: Path) -> None:
    """Atomically refresh a long-lived lease for one active restore staging directory."""
    now = time.time()
    payload = {
        "schema_version": 1,
        "stage_name": stage.name,
        "pid": os.getpid(),
        "hostname": socket.gethostname(),
        "process_start_token": _process_start_token(os.getpid()),
        "heartbeat_at_epoch": now,
        "heartbeat_at_utc": _timestamp(),
        "lease_expires_at_epoch": now + RESTORE_LEASE_TTL_SECONDS,
        "lease_ttl_seconds": RESTORE_LEASE_TTL_SECONDS,
    }
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=".restore-lease-",
            suffix=".tmp",
            dir=stage,
            delete=False,
        ) as stream:
            temporary_path = Path(stream.name)
            json.dump(payload, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, stage / RESTORE_LEASE_FILENAME)
        temporary_path = None
        try:
            directory_fd = os.open(stage, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except OSError:
            # Directory fsync is not supported by every platform/filesystem.
            pass
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except OSError:
                pass


def inspect_restore_staging(
    *,
    project_root: Path,
    now_epoch: float | None = None,
) -> list[dict[str, Any]]:
    """Read-only inventory of hidden restore stages and their lease state.

    An expired lease is only a manual-review candidate, never proof that a
    process is dead. This function never renames, deletes, resumes, or promotes
    a staging directory.
    """
    root = project_root.resolve()
    output_lexical = root / "output"
    restores_lexical = output_lexical / "restores"
    if output_lexical.is_symlink() or restores_lexical.is_symlink():
        raise BackupError("Restore staging inspection does not follow symbolic links.")
    if not restores_lexical.exists():
        return []
    restores_root = restores_lexical.resolve()
    if not _inside(root, restores_root) or not restores_root.is_dir():
        raise BackupError("Restore staging directory must remain inside project root.")
    if now_epoch is None:
        now = time.time()
    else:
        if (
            isinstance(now_epoch, bool)
            or not isinstance(now_epoch, (int, float))
            or not math.isfinite(now_epoch)
        ):
            raise ValueError("Inspection time must be a finite numeric epoch.")
        now = float(now_epoch)

    results: list[dict[str, Any]] = []
    for stage in sorted(restores_root.iterdir(), key=lambda item: item.name):
        if not stage.name.startswith(".restore-staging-"):
            continue
        result: dict[str, Any] = {
            "stage_name": stage.name,
            "status": "unknown",
            "reason": "Lease evidence is missing or cannot be trusted.",
        }
        if stage.is_symlink() or not stage.is_dir():
            result.update(status="unsafe", reason="Staging entry is not a real directory.")
            results.append(result)
            continue
        lease_path = stage / RESTORE_LEASE_FILENAME
        if lease_path.is_symlink() or not lease_path.is_file():
            results.append(result)
            continue
        try:
            lease = json.loads(lease_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            results.append(result)
            continue
        if not isinstance(lease, dict):
            results.append(result)
            continue
        pid = lease.get("pid")
        hostname = lease.get("hostname")
        process_token = lease.get("process_start_token")
        heartbeat = lease.get("heartbeat_at_epoch")
        expires = lease.get("lease_expires_at_epoch")
        if (
            lease.get("schema_version") != 1
            or lease.get("stage_name") != stage.name
            or isinstance(pid, bool) or not isinstance(pid, int) or pid < 1
            or not isinstance(hostname, str) or not hostname
            or (process_token is not None and not isinstance(process_token, str))
            or isinstance(heartbeat, bool) or not isinstance(heartbeat, (int, float))
            or not math.isfinite(heartbeat)
            or isinstance(expires, bool) or not isinstance(expires, (int, float))
            or not math.isfinite(expires)
            or expires <= heartbeat
        ):
            results.append(result)
            continue

        current_token = (
            _process_start_token(pid)
            if hostname == socket.gethostname() and process_token is not None
            else None
        )
        if current_token is not None and current_token == process_token:
            status = "active_process"
            reason = "The recorded process identity is still present on this host."
        elif current_token is not None and current_token != process_token:
            status = "expired_candidate" if now >= expires else "owner_identity_mismatch"
            reason = (
                "The recorded PID now belongs to a different process; manual review is required."
            )
        elif now < expires:
            status = "active_lease"
            reason = "The lease has not expired; the stage must be treated as active."
        else:
            status = "expired_candidate"
            reason = (
                "The lease expired; this is only a manual-review candidate, not an "
                "automatic cleanup or recovery instruction."
            )
        result.update({
            "status": status,
            "reason": reason,
            "pid": pid,
            "hostname": hostname,
            "heartbeat_at_epoch": heartbeat,
            "lease_expires_at_epoch": expires,
        })
        results.append(result)
    return results

def restore_source_backup(
    *,
    project_root: Path,
    backup_path: Path,
    destination: Path | None = None,
) -> tuple[Path, dict[str, Any]]:
    """Verify a backup and restore it into a new, separate source snapshot folder.

    No existing project files are overwritten. The restore is a source snapshot:
    Git metadata, output folders, caches, and excluded secret files are not part
    of the inventory/backup and therefore are not recreated.
    """
    root = project_root.resolve()
    output_lexical = root / "output"
    backups_lexical = output_lexical / "backups"
    restores_lexical = output_lexical / "restores"
    if (
        output_lexical.is_symlink()
        or backups_lexical.is_symlink()
        or restores_lexical.is_symlink()
    ):
        raise BackupError("Backup and restore directories must not use symbolic links.")

    backups_root = backups_lexical.resolve()
    restores_root = restores_lexical.resolve()
    if not _inside(root, backups_root) or not _inside(root, restores_root):
        raise BackupError("Backup and restore directories must remain inside project root.")

    candidate = backup_path if backup_path.is_absolute() else root / backup_path
    if candidate.is_symlink():
        raise BackupError("Backup directory must not be a symbolic link.")
    backup_dir = candidate.resolve()
    if backup_dir.parent != backups_root or not backup_dir.is_dir():
        raise BackupError("Backup must be a direct child directory of output/backups.")

    manifest_path = backup_dir / "backup-manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise BackupError("Backup manifest is missing or unsafe.")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BackupError(f"Could not read backup manifest: {exc}") from exc

    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise BackupError("Backup manifest has an invalid or unsupported schema.")
    if manifest.get("status") != "complete":
        raise BackupError("Only a complete verified backup can be restored.")
    if Path(str(manifest.get("project_root", ""))).resolve() != root:
        raise BackupError("Backup was created from a different project root.")

    records = manifest.get("files")
    if not isinstance(records, list):
        raise BackupError("Backup manifest does not contain a valid files list.")
    if manifest.get("file_count") != len(records):
        raise BackupError("Backup manifest file count does not match its records.")

    validated: list[tuple[dict[str, Any], Path, PurePosixPath]] = []
    seen: set[str] = set()
    total_size = 0
    for record in records:
        if not isinstance(record, dict):
            raise BackupError("Backup manifest contains a malformed file record.")
        relative = _safe_relative_path(record.get("source_path"))
        normalized = relative.as_posix()
        if normalized in seen:
            raise BackupError(f"Duplicate source path in backup manifest: {normalized}")
        seen.add(normalized)
        if any(part in EXCLUDED_DIRECTORIES for part in relative.parts):
            raise BackupError(f"Excluded path found in backup manifest: {normalized}")
        if any(
            fnmatch.fnmatchcase(relative.name, pattern)
            for pattern in SENSITIVE_FILE_PATTERNS
        ):
            raise BackupError(f"Sensitive filename found in backup manifest: {normalized}")

        expected_backup = (PurePosixPath("files") / relative).as_posix()
        if record.get("backup_path") != expected_backup:
            raise BackupError(f"Backup path mismatch for {normalized}.")

        source = backup_dir.joinpath(*PurePosixPath(expected_backup).parts)
        current = backup_dir
        for part in PurePosixPath(expected_backup).parts:
            current = current / part
            if current.is_symlink():
                raise BackupError(f"Symbolic-link backup input is not allowed: {expected_backup}")
        source = source.resolve()
        files_root = (backup_dir / "files").resolve()
        if not _inside(files_root, source) or not source.is_file():
            raise BackupError(f"Backup source is missing or unsafe: {expected_backup}")

        size = record.get("size_bytes")
        checksum = record.get("sha256")
        if (
            not isinstance(size, int)
            or isinstance(size, bool)
            or size < 0
            or not isinstance(checksum, str)
            or len(checksum) != 64
            or any(character not in "0123456789abcdef" for character in checksum)
        ):
            raise BackupError(f"Invalid integrity metadata for {normalized}.")
        if source.stat().st_size != size or _sha256(source) != checksum:
            raise BackupError(f"Backup file failed integrity verification: {normalized}.")
        total_size += size
        validated.append((record, source, relative))

    if total_size != manifest.get("total_size_bytes"):
        raise BackupError("Backup total size does not match its records.")

    source_inventory_hash = manifest.get("source_inventory_sha256")
    if (
        not isinstance(source_inventory_hash, str)
        or len(source_inventory_hash) != 64
        or any(character not in "0123456789abcdef" for character in source_inventory_hash)
    ):
        raise BackupError("Backup manifest has an invalid source inventory SHA-256.")

    # Reconstruct the inventory's canonical path/hash digest. This catches
    # record edits that also update a copied file's checksum and byte count,
    # which per-file checks and the total-size check alone cannot detect.
    aggregate = hashlib.sha256()
    for record, _, relative in sorted(
        validated, key=lambda item: item[2].as_posix()
    ):
        aggregate.update(relative.as_posix().encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(record["sha256"].encode("ascii"))
        aggregate.update(b"\n")
    if aggregate.hexdigest() != source_inventory_hash:
        raise BackupError(
            "Backup file records do not match the source inventory aggregate hash."
        )

    restores_root.mkdir(parents=True, exist_ok=True)
    if destination is None:
        final_dir = restores_root / f"restored-source-{_stamp()}"
    else:
        final_dir = destination if destination.is_absolute() else root / destination
        final_dir = final_dir.resolve()
    if final_dir.parent != restores_root:
        raise BackupError("Restore destination must be a direct child of output/restores.")
    if final_dir.exists() or final_dir.is_symlink():
        raise BackupError(f"Refusing to overwrite existing restore directory: {final_dir}")

    stage = Path(tempfile.mkdtemp(prefix=".restore-staging-", dir=restores_root))
    restored_records: list[dict[str, Any]] = []
    try:
        _write_restore_lease(stage)
        for record, source, relative in validated:
            _write_restore_lease(stage)
            target = stage.joinpath(*relative.parts)
            if not _inside(stage, target):
                raise BackupError(f"Restore path escapes staging directory: {relative}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            restored_hash = _sha256(target)
            restored_size = target.stat().st_size
            if restored_hash != record["sha256"] or restored_size != record["size_bytes"]:
                raise BackupError(f"Restored file verification failed: {relative.as_posix()}.")
            restored_records.append({
                "path": relative.as_posix(),
                "size_bytes": restored_size,
                "sha256": restored_hash,
            })
            _write_restore_lease(stage)

        restore_manifest = {
            "schema_version": 1,
            "created_at_utc": _timestamp(),
            "status": "complete",
            "source_backup": str(backup_dir.relative_to(root)),
            "source_inventory_sha256": manifest["source_inventory_sha256"],
            "file_count": len(restored_records),
            "total_size_bytes": sum(item["size_bytes"] for item in restored_records),
            "files": restored_records,
            "notes": [
                "Restored to a new directory; no existing project files were overwritten.",
                "Git metadata, generated output, caches, and excluded secret files are not included.",
            ],
        }
        with (stage / "restore-manifest.json").open("x", encoding="utf-8") as stream:
            json.dump(restore_manifest, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())

        if final_dir.exists():
            raise BackupError(f"Refusing to overwrite existing restore directory: {final_dir}")
        _write_restore_lease(stage)
        os.replace(stage, final_dir)
        try:
            (final_dir / RESTORE_LEASE_FILENAME).unlink()
        except OSError:
            # A completed restore is no longer scanned as a staging directory.
            pass
        return final_dir, restore_manifest

    except BaseException as exc:
        if not stage.exists():
            raise

        interrupted = not isinstance(exc, Exception)
        prefix = "INTERRUPTED" if interrupted else "FAILED"
        status = "interrupted" if interrupted else "incomplete"
        failed_dir = restores_root / f"{prefix}-{_stamp()}"
        suffix = 1
        while failed_dir.exists():
            failed_dir = restores_root / f"{prefix}-{_stamp()}-{suffix}"
            suffix += 1
        try:
            failure = {
                "schema_version": 1,
                "created_at_utc": _timestamp(),
                "status": status,
                "error": f"{type(exc).__name__}: {exc}",
                "verified_files_before_failure": restored_records,
                "recovery_guidance": (
                    "The staging directory is diagnostic evidence, not a resumable "
                    "restore. Retry from the verified backup into a new, unused "
                    "output/restores destination. The incomplete staging directory "
                    "is preserved and is never promoted or overwritten automatically."
                ),
            }
            report_name = (
                "restore-interruption.json" if interrupted else "restore-failure.json"
            )
            with (stage / report_name).open("x", encoding="utf-8") as stream:
                json.dump(failure, stream, indent=2)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(stage, failed_dir)
        except OSError:
            # Keep the original exception and leave any surviving stage in place.
            pass

        if interrupted:
            # Preserve KeyboardInterrupt/SystemExit semantics after recording evidence.
            raise
        raise BackupError(
            f"Restore failed; partial staging was preserved at "
            f"{failed_dir if failed_dir.exists() else stage}: {exc}"
        ) from exc
