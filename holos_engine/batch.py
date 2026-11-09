"""Ordered, resumable multi-shot rendering with a persistent manifest.

The controller never deletes partial output. An incomplete shot directory is
moved into output/recovery before that shot is retried.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from typing import Any, Callable


class BatchRenderError(RuntimeError):
    """Raised when a batch manifest or project path is unsafe or inconsistent."""


def _inside(root: Path, path: Path) -> bool:
    return path == root or root in path.parents


def _safe_component(value: str, label: str) -> str:
    if not value or value in {".", ".."} or "/" in value or "\\\\" in value:
        raise BatchRenderError(f"{label} must be a single safe path component: {value!r}")
    if Path(value).is_absolute():
        raise BatchRenderError(f"{label} must not be an absolute path: {value!r}")
    return value


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _config_digest(episode: dict[str, Any]) -> str:
    encoded = json.dumps(episode, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _expected_names(frame_count: int) -> list[str]:
    return [f"frame_{index:06d}.png" for index in range(frame_count)]


def _has_valid_frames(output_dir: Path, frame_count: int) -> bool:
    if not output_dir.is_dir():
        return False
    frames = sorted(output_dir.glob("frame_*.png"))
    if [item.name for item in frames] != _expected_names(frame_count):
        return False
    return all(item.is_file() and item.stat().st_size > 0 for item in frames)


def _archive_output(root: Path, output_dir: Path, shot_id: str) -> str | None:
    if not output_dir.exists():
        return None
    recovery_root = (root / "output" / "recovery").resolve()
    if not _inside(root, recovery_root):
        raise BatchRenderError("Recovery directory must remain inside project root.")
    recovery_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    destination = recovery_root / f"{shot_id}-{stamp}"
    suffix = 1
    while destination.exists():
        destination = recovery_root / f"{shot_id}-{stamp}-{suffix}"
        suffix += 1
    shutil.move(str(output_dir), str(destination))
    return str(destination.relative_to(root))


def _write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest["updated_at"] = _timestamp()
    handle, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(manifest, stream, indent=2)
            stream.write("\\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def render_episode_batch(
    *,
    project_root: Path,
    episode: dict[str, Any],
    mode: str,
    render_one: Callable[[dict[str, Any], dict[str, Any], Path], dict[str, Any]],
) -> dict[str, Any]:
    """Render shots in configuration order, resuming only verified completions.

    render_one receives (scene, shot, absolute_output_directory). It must raise
    on failure and return a result after successfully producing the shot.
    """
    root = project_root.resolve()
    episode_id = _safe_component(episode["episode_id"], "episode_id")
    if mode not in {"debug", "production"}:
        raise BatchRenderError(f"Unsupported render mode: {mode}")

    jobs: list[tuple[dict[str, Any], dict[str, Any], int]] = []
    seen: set[str] = set()
    for scene in episode["scenes"]:
        for shot in scene["shots"]:
            shot_id = _safe_component(shot["shot_id"], "shot_id")
            if shot_id in seen:
                raise BatchRenderError(f"Duplicate shot_id in batch: {shot_id}")
            seen.add(shot_id)
            jobs.append((scene, shot, shot["end_frame"] - shot["start_frame"]))

    render_root = (root / "output" / "renders" / episode_id).resolve()
    manifest_path = (
        root / "output" / "manifests" / f"{episode_id}-{mode}-render.json"
    ).resolve()
    if not _inside(root, render_root) or not _inside(root, manifest_path):
        raise BatchRenderError("Batch output paths must remain inside project root.")

    digest = _config_digest(episode)
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise BatchRenderError(f"Cannot read existing batch manifest: {exc}") from exc
        if not isinstance(manifest, dict):
            raise BatchRenderError("Existing batch manifest must contain a JSON object.")
        if manifest.get("schema_version") != 1:
            raise BatchRenderError("Existing batch manifest has an unsupported schema version.")
        if manifest.get("episode_config_sha256") != digest or manifest.get("mode") != mode:
            raise BatchRenderError(
                "Existing batch manifest belongs to a different episode configuration "
                "or render mode. Preserve it and use a new episode ID for a new run."
            )
        records = manifest.get("shots")
        if not isinstance(records, list):
            raise BatchRenderError("Existing batch manifest has an invalid shots list.")
        previous = {
            item.get("shot_id"): item
            for item in records
            if isinstance(item, dict) and isinstance(item.get("shot_id"), str)
        }
    else:
        previous = {}
        manifest = {
            "schema_version": 1,
            "episode_id": episode_id,
            "mode": mode,
            "episode_config_sha256": digest,
            "created_at": _timestamp(),
            "shots": [],
        }

    current_records: list[dict[str, Any]] = []
    for scene, shot, frame_count in jobs:
        shot_id = shot["shot_id"]
        output_dir = (render_root / shot_id).resolve()
        if not _inside(root, output_dir):
            raise BatchRenderError(f"Shot output path escapes project root: {output_dir}")
        prior = previous.get(shot_id, {})
        record = {
            "scene_id": scene["scene_id"],
            "shot_id": shot_id,
            "start_frame": shot["start_frame"],
            "end_frame": shot["end_frame"],
            "expected_frame_count": frame_count,
            "output_dir": str(output_dir.relative_to(root)),
            "status": prior.get("status", "pending"),
            "error": None,
            "result": prior.get("result"),
            "recovered_output": None,
        }
        current_records.append(record)

    manifest["shots"] = current_records
    _write_manifest(manifest_path, manifest)

    completed_now: list[str] = []
    skipped: list[str] = []
    failed: list[str] = []

    for index, (scene, shot, frame_count) in enumerate(jobs):
        record = current_records[index]
        output_dir = (root / record["output_dir"]).resolve()

        if record["status"] == "completed" and _has_valid_frames(output_dir, frame_count):
            skipped.append(shot["shot_id"])
            continue

        if output_dir.exists():
            record["recovered_output"] = _archive_output(root, output_dir, shot["shot_id"])
        record["status"] = "running"
        record["error"] = None
        record["result"] = None
        _write_manifest(manifest_path, manifest)

        try:
            result = render_one(scene, shot, output_dir)
            if not _has_valid_frames(output_dir, frame_count):
                raise BatchRenderError(
                    f"Renderer did not produce the exact {frame_count}-frame sequence "
                    f"for shot {shot['shot_id']}."
                )
            record["status"] = "completed"
            record["result"] = {
                key: result[key]
                for key in ("return_code", "frame_count", "first_frame", "last_frame")
                if isinstance(result, dict) and key in result
            }
            completed_now.append(shot["shot_id"])
        except Exception as exc:
            record["status"] = "failed"
            record["error"] = f"{type(exc).__name__}: {exc}"
            failed.append(shot["shot_id"])
        _write_manifest(manifest_path, manifest)

    status_counts = {
        status: sum(1 for item in current_records if item["status"] == status)
        for status in ("completed", "failed", "pending", "running")
    }
    return {
        "episode_id": episode_id,
        "mode": mode,
        "manifest": str(manifest_path),
        "completed_this_run": completed_now,
        "skipped_verified": skipped,
        "failed_this_run": failed,
        "status_counts": status_counts,
        "success": not failed and status_counts["completed"] == len(jobs),
    }
