"""Verified, non-destructive source backup from a SHA-256 inventory."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import fnmatch
import os
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
        aggregate.update(b"\\0")
        aggregate.update(record["sha256"].encode("ascii"))
        aggregate.update(b"\\n")
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

