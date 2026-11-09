"""Read-only source inventory for the HOLOS project.

The inventory hashes regular source/project files but never follows symlinks,
reads common secret-file names, or scans generated output and tool caches.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any


class InventoryError(RuntimeError):
    """Raised when a source inventory cannot be completed safely."""


EXCLUDED_DIRECTORIES = {
    ".git",
    ".godot",
    ".import",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
    "output",
    "build",
    "dist",
}

SENSITIVE_FILE_PATTERNS = (
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "*.p12",
    "*.pfx",
    "id_rsa",
    "id_ed25519",
)


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _category(relative_path: str) -> str:
    first = relative_path.split("/", 1)[0]
    if first == "godot":
        return "godot_project"
    if first == "holos_engine" or first == "tools":
        return "production_code"
    if first == "tests":
        return "tests"
    if first == "examples":
        return "examples"
    if first == "docs":
        return "documentation"
    if first == ".github" or relative_path in {"README.md", ".gitignore", "pyproject.toml"}:
        return "project_configuration"
    return "other"


def _is_sensitive_name(name: str) -> bool:
    return any(fnmatch.fnmatchcase(name, pattern) for pattern in SENSITIVE_FILE_PATTERNS)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_inventory(project_root: Path) -> dict[str, Any]:
    """Hash project files without modifying or following source-tree symlinks."""
    root = project_root.resolve()
    if not root.is_dir():
        raise InventoryError(f"Project root is not a directory: {root}")

    files: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    errors: list[dict[str, str]] = []

    for current, directories, filenames in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        safe_directories: list[str] = []
        for directory in sorted(directories):
            candidate = current_path / directory
            relative = candidate.relative_to(root).as_posix()
            if candidate.is_symlink():
                skipped.append({"path": relative, "reason": "symlink_directory_not_followed"})
            elif directory in EXCLUDED_DIRECTORIES:
                skipped.append({"path": relative, "reason": "generated_or_dependency_directory"})
            else:
                safe_directories.append(directory)
        directories[:] = safe_directories

        for filename in sorted(filenames):
            path = current_path / filename
            relative = path.relative_to(root).as_posix()

            if _is_sensitive_name(filename):
                skipped.append({"path": relative, "reason": "sensitive_filename_excluded"})
                continue
            if path.is_symlink():
                skipped.append({"path": relative, "reason": "symlink_file_not_followed"})
                continue
            try:
                if not path.is_file():
                    skipped.append({"path": relative, "reason": "not_a_regular_file"})
                    continue
                size = path.stat().st_size
                files.append({
                    "path": relative,
                    "category": _category(relative),
                    "extension": path.suffix.lower(),
                    "size_bytes": size,
                    "sha256": _sha256(path),
                })
            except OSError as exc:
                errors.append({"path": relative, "error": f"{type(exc).__name__}: {exc}"})

    files.sort(key=lambda item: item["path"])
    skipped.sort(key=lambda item: item["path"])
    errors.sort(key=lambda item: item["path"])

    category_counts = Counter(item["category"] for item in files)
    extension_counts = Counter(item["extension"] or "[no extension]" for item in files)
    aggregate = hashlib.sha256()
    for item in files:
        aggregate.update(item["path"].encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(item["sha256"].encode("ascii"))
        aggregate.update(b"\n")

    return {
        "schema_version": 1,
        "generated_at_utc": _timestamp(),
        "project_root": str(root),
        "status": "complete" if not errors else "partial",
        "policy": {
            "read_only": True,
            "hash": "SHA-256",
            "follow_symlinks": False,
            "excluded_directories": sorted(EXCLUDED_DIRECTORIES),
            "excluded_file_patterns": list(SENSITIVE_FILE_PATTERNS),
        },
        "summary": {
            "file_count": len(files),
            "total_size_bytes": sum(item["size_bytes"] for item in files),
            "skipped_count": len(skipped),
            "error_count": len(errors),
            "category_counts": dict(sorted(category_counts.items())),
            "extension_counts": dict(sorted(extension_counts.items())),
            "inventory_sha256": aggregate.hexdigest(),
        },
        "files": files,
        "skipped": skipped,
        "errors": errors,
    }


def write_inventory_report(
    project_root: Path,
    output_path: Path | None = None,
) -> tuple[Path, dict[str, Any]]:
    """Write an atomic JSON inventory report outside the scanned source tree."""
    root = project_root.resolve()
    inventory = build_inventory(root)
    if output_path is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        destination = root / "output" / "reports" / f"source-inventory-{stamp}.json"
        suffix = 1
        while destination.exists():
            destination = (
                root / "output" / "reports" / f"source-inventory-{stamp}-{suffix}.json"
            )
            suffix += 1
    else:
        destination = output_path if output_path.is_absolute() else root / output_path
        destination = destination.resolve()

    reports_root = (root / "output" / "reports").resolve()
    if not (reports_root == root or root in reports_root.parents):
        raise InventoryError("Inventory report directory must remain inside project root.")
    if destination == reports_root or reports_root not in destination.parents:
        raise InventoryError("Inventory report must be written under output/reports.")
    if destination.exists():
        raise InventoryError(f"Refusing to overwrite existing inventory report: {destination}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(inventory, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, destination)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise
    return destination, inventory
