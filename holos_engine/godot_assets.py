"""Static audit of literal res:// dependencies in a Godot project."""

from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path, PurePosixPath
import re
from typing import Any

from .inventory import EXCLUDED_DIRECTORIES

RESOURCE_REFERENCE = re.compile(r"""res://([^"'\]\)\r\n]+)""")
UID_REFERENCE = re.compile(r"""uid://[A-Za-z0-9]+""")
TEXT_EXTENSIONS = {
    ".tscn", ".scn", ".tres", ".res", ".gd", ".cs", ".gdshader",
    ".gdshaderinc", ".gdextension", ".godot", ".cfg", ".import",
    ".translation", ".theme",
}


class GodotAssetAuditError(RuntimeError):
    """Raised when a Godot project cannot be audited safely."""


def _inside(root: Path, path: Path) -> bool:
    return path == root or root in path.parents


def _assert_no_symlink_components(root: Path, path: Path, label: str) -> None:
    root = root.resolve()
    candidate = Path(os.path.abspath(path))
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise GodotAssetAuditError(
            f"{label} must remain inside project root: {candidate}"
        ) from exc
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise GodotAssetAuditError(
                f"{label} must not traverse symbolic links: {current}"
            )


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def audit_godot_project(
    *,
    project_root: Path,
    godot_project: Path = Path("godot"),
) -> dict[str, Any]:
    """Resolve literal res:// references without modifying or following symlinks.

    UID references and dynamically constructed paths are reported separately:
    their final resolution requires Godot's own import/resource database.
    """
    root = project_root.resolve()
    candidate = godot_project if godot_project.is_absolute() else root / godot_project
    _assert_no_symlink_components(root, candidate, "Godot project path")
    project = candidate.resolve()
    if not _inside(root, project) or not project.is_dir():
        raise GodotAssetAuditError(
            f"Godot project must be an existing directory inside project root: {project}"
        )
    project_file = project / "project.godot"
    _assert_no_symlink_components(root, project_file, "Godot project configuration")
    if not project_file.is_file():
        raise GodotAssetAuditError(f"project.godot not found: {project_file}")

    references: dict[tuple[str, str], dict[str, str]] = {}
    uid_references: set[tuple[str, str]] = set()
    scan_errors: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []

    def on_walk_error(exc: OSError) -> None:
        scan_errors.append({
            "path": str(getattr(exc, "filename", project)),
            "error": f"{type(exc).__name__}: {exc}",
        })

    for current, directories, filenames in os.walk(
        project, topdown=True, followlinks=False, onerror=on_walk_error
    ):
        current_path = Path(current)
        safe_directories: list[str] = []
        for directory in sorted(directories):
            path = current_path / directory
            if path.is_symlink():
                skipped.append({
                    "path": path.relative_to(project).as_posix(),
                    "reason": "symlink_directory_not_followed",
                })
            elif directory in EXCLUDED_DIRECTORIES:
                skipped.append({
                    "path": path.relative_to(project).as_posix(),
                    "reason": "generated_or_dependency_directory",
                })
            else:
                safe_directories.append(directory)
        directories[:] = safe_directories

        for filename in sorted(filenames):
            source = current_path / filename
            if source.suffix.lower() not in TEXT_EXTENSIONS and filename != "project.godot":
                continue
            relative_source = source.relative_to(project).as_posix()
            if source.is_symlink():
                skipped.append({
                    "path": relative_source,
                    "reason": "symlink_file_not_followed",
                })
                continue
            try:
                content = source.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                skipped.append({
                    "path": relative_source,
                    "reason": "not_utf8_text",
                })
                continue
            except OSError as exc:
                scan_errors.append({
                    "path": relative_source,
                    "error": f"{type(exc).__name__}: {exc}",
                })
                continue

            for match in RESOURCE_REFERENCE.finditer(content):
                raw = match.group(1).strip().rstrip(" ,;")
                if not raw:
                    continue
                resource_path = raw.split("::", 1)[0]
                key = (relative_source, resource_path)
                references[key] = {
                    "source_file": relative_source,
                    "resource_path": resource_path,
                }
            for uid in UID_REFERENCE.findall(content):
                uid_references.add((relative_source, uid))

    resolved: list[dict[str, str]] = []
    missing: list[dict[str, str]] = []
    unsafe: list[dict[str, str]] = []
    for item in sorted(references.values(), key=lambda value: (
        value["source_file"], value["resource_path"]
    )):
        source_file = item["source_file"]
        resource_path = item["resource_path"]
        relative = PurePosixPath(resource_path)
        if (
            "\\" in resource_path
            or relative.is_absolute()
            or not relative.parts
            or any(part in {"", ".", ".."} for part in relative.parts)
            or (relative.parts and ":" in relative.parts[0])
        ):
            unsafe.append({
                **item,
                "reason": "resource_path_is_not_a_safe_project_relative_path",
            })
            continue

        target = project.joinpath(*relative.parts)
        try:
            _assert_no_symlink_components(project, target, "Referenced resource")
        except GodotAssetAuditError:
            unsafe.append({
                **item,
                "reason": "resource_path_traverses_symbolic_link",
            })
            continue
        if not target.exists():
            missing.append({**item, "reason": "referenced_path_does_not_exist"})
        else:
            resolved.append(item)

    uid_records = [
        {"source_file": source, "uid": uid}
        for source, uid in sorted(uid_references)
    ]
    skipped.sort(key=lambda item: item["path"])
    scan_errors.sort(key=lambda item: item["path"])
    status = "complete" if not (missing or unsafe or scan_errors) else "issues_found"

    return {
        "schema_version": 1,
        "generated_at_utc": _timestamp(),
        "project_root": str(root),
        "godot_project": str(project.relative_to(root)),
        "status": status,
        "summary": {
            "literal_resource_reference_count": len(references),
            "resolved_reference_count": len(resolved),
            "missing_reference_count": len(missing),
            "unsafe_reference_count": len(unsafe),
            "uid_reference_count": len(uid_records),
            "scan_error_count": len(scan_errors),
            "skipped_file_or_directory_count": len(skipped),
        },
        "resolved": resolved,
        "missing": missing,
        "unsafe": unsafe,
        "uid_references": uid_records,
        "scan_errors": scan_errors,
        "skipped": skipped,
        "limitations": [
            "Only literal res:// paths in supported UTF-8 text files are statically resolved.",
            "uid:// references require Godot's resource UID database and are listed but not resolved.",
            "Dynamically constructed resource paths cannot be determined by this static scan.",
            "A clean static audit does not replace opening and loading the project in Godot.",
        ],
    }
