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
import shutil
import tempfile
from typing import Any, Callable


class BatchRenderError(RuntimeError):
    """Raised when a batch manifest or project path is unsafe or inconsistent."""


def _inside(root: Path, path: Path) -> bool:
    return path == root or root in path.parents




def _assert_no_symlink_components(root: Path, path: Path, label: str) -> None:
    """Reject symlinks in every existing component without resolving them first."""
    root = root.resolve()
    candidate = Path(os.path.abspath(path))
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise BatchRenderError(f"{label} must remain inside project root: {candidate}") from exc

    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise BatchRenderError(
                f"{label} must not traverse symbolic links: {current}"
            )

def _safe_component(value: str, label: str) -> str:
    if not isinstance(value, str) or not value or value in {".", ".."}:
        raise BatchRenderError(f"{label} must be a single safe path component: {value!r}")
    if "/" in value or "\\" in value or Path(value).is_absolute():
        raise BatchRenderError(f"{label} must be a single safe path component: {value!r}")
    return value


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _config_digest(episode: dict[str, Any]) -> str:
    encoded = json.dumps(episode, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _expected_names(frame_count: int) -> list[str]:
    return [f"frame_{index:06d}.png" for index in range(frame_count)]


def _frame_integrity(output_dir: Path, frame_count: int) -> list[dict[str, Any]] | None:
    if output_dir.is_symlink() or not output_dir.is_dir():
        return None
    frames = sorted(output_dir.glob("frame_*.png"))
    if [item.name for item in frames] != _expected_names(frame_count):
        return None

    records: list[dict[str, Any]] = []
    for frame in frames:
        if frame.is_symlink() or not frame.is_file() or frame.stat().st_size == 0:
            return None
        digest = hashlib.sha256()
        with frame.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        records.append({
            "name": frame.name,
            "size_bytes": frame.stat().st_size,
            "sha256": digest.hexdigest(),
        })
    return records


def _has_valid_frames(
    output_dir: Path,
    frame_count: int,
    expected_integrity: list[dict[str, Any]] | None = None,
) -> bool:
    actual = _frame_integrity(output_dir, frame_count)
    if actual is None:
        return False
    return expected_integrity is None or actual == expected_integrity


def _archive_output(root: Path, output_dir: Path, shot_id: str) -> str | None:
    _assert_no_symlink_components(root, output_dir, "Shot output directory")
    if not output_dir.exists():
        return None
    recovery_root = root / "output" / "recovery"
    _assert_no_symlink_components(root, recovery_root, "Recovery directory")
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
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _manifest_location(root: Path, episode: dict[str, Any], mode: str) -> Path:
    episode_id = _safe_component(episode["episode_id"], "episode_id")
    if mode not in {"debug", "production"}:
        raise BatchRenderError(f"Unsupported render mode: {mode}")
    path = root / "output" / "manifests" / f"{episode_id}-{mode}-render.json"
    _assert_no_symlink_components(root, path, "Batch manifest path")
    return path


def load_completed_batch_manifest(
    *,
    project_root: Path,
    episode: dict[str, Any],
    mode: str,
) -> tuple[Path, dict[str, Any]]:
    """Load a matching manifest and verify every shot before episode assembly."""
    root = project_root.resolve()
    manifest_path = _manifest_location(root, episode, mode)
    if not manifest_path.is_file():
        raise BatchRenderError(
            f"Completed batch manifest not found. Run render-episode first: {manifest_path}"
        )
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BatchRenderError(f"Cannot read batch manifest: {exc}") from exc

    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise BatchRenderError("Batch manifest has an invalid or unsupported schema.")
    if manifest.get("episode_config_sha256") != _config_digest(episode):
        raise BatchRenderError("Batch manifest does not match the current episode configuration.")
    if manifest.get("mode") != mode:
        raise BatchRenderError("Batch manifest render mode does not match the requested mode.")

    records = manifest.get("shots")
    expected_shots = [
        (scene, shot, shot["end_frame"] - shot["start_frame"])
        for scene in episode["scenes"]
        for shot in scene["shots"]
    ]
    if not isinstance(records, list) or len(records) != len(expected_shots):
        raise BatchRenderError("Batch manifest shot list does not match the episode.")

    for record, (scene, shot, frame_count) in zip(records, expected_shots):
        if not isinstance(record, dict) or record.get("shot_id") != shot["shot_id"]:
            raise BatchRenderError("Batch manifest shot order does not match the episode.")
        shot_id = _safe_component(shot["shot_id"], "shot_id")
        expected_output = (
            Path("output") / "renders" / _safe_component(episode["episode_id"], "episode_id")
            / mode / shot_id
        )
        try:
            recorded_output = Path(record.get("output_dir", ""))
        except TypeError as exc:
            raise BatchRenderError(f"Invalid output path in manifest for {shot_id}.") from exc
        if recorded_output != expected_output:
            raise BatchRenderError(
                f"Manifest output path does not match the expected shot directory for {shot_id}."
            )
        if record.get("status") != "completed":
            raise BatchRenderError(
                f"Shot {shot['shot_id']} is not completed (status: {record.get('status')})."
            )
        if record.get("expected_frame_count") != frame_count:
            raise BatchRenderError(f"Frame-count metadata mismatch for shot {shot['shot_id']}.")
        relative_output = Path(record.get("output_dir", ""))
        if relative_output.is_absolute():
            raise BatchRenderError(f"Absolute shot output path is not allowed: {relative_output}")
        candidate_output = root / relative_output
        _assert_no_symlink_components(root, candidate_output, "Shot output directory")
        output_dir = candidate_output.resolve()
        if not _inside(root, output_dir):
            raise BatchRenderError(f"Shot output path escapes project root: {output_dir}")
        if not _has_valid_frames(
            output_dir, frame_count, record.get("frame_integrity")
        ):
            raise BatchRenderError(
                f"Shot {shot['shot_id']} is marked completed but its frame sequence "
                "is missing, empty, or has changed."
            )
    return manifest_path, manifest


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

    render_root = root / "output" / "renders" / episode_id / mode
    _assert_no_symlink_components(root, render_root, "Batch render directory")
    manifest_path = _manifest_location(root, episode, mode)

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
        expected_ids = [shot["shot_id"] for _, shot, _ in jobs]
        if not isinstance(records, list) or len(records) != len(expected_ids):
            raise BatchRenderError(
                "Existing batch manifest shot list does not match the current episode."
            )
        recorded_ids: list[str] = []
        previous = {}
        for item in records:
            if not isinstance(item, dict) or not isinstance(item.get("shot_id"), str):
                raise BatchRenderError("Existing batch manifest contains a malformed shot record.")
            shot_id = item["shot_id"]
            if shot_id in previous:
                raise BatchRenderError(f"Existing batch manifest has duplicate shot: {shot_id}")
            recorded_ids.append(shot_id)
            previous[shot_id] = item
        if recorded_ids != expected_ids:
            raise BatchRenderError(
                "Existing batch manifest shot order does not match the current episode."
            )
        for shot_id, item in previous.items():
            if item.get("status") not in {"pending", "running", "failed", "completed"}:
                raise BatchRenderError(
                    f"Existing batch manifest has invalid status for {shot_id}."
                )
            attempts = item.get("attempts", 0)
            if not isinstance(attempts, int) or isinstance(attempts, bool) or attempts < 0:
                raise BatchRenderError(
                    f"Existing batch manifest has invalid attempt count for {shot_id}."
                )
            for field in ("errors", "recovered_outputs"):
                value = item.get(field, [])
                if not isinstance(value, list) or not all(isinstance(entry, str) for entry in value):
                    raise BatchRenderError(
                        f"Existing batch manifest has invalid {field} for {shot_id}."
                    )
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
        output_dir = render_root / shot_id
        _assert_no_symlink_components(root, output_dir, "Shot output directory")
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
            "errors": list(prior.get("errors", [])),
            "attempts": int(prior.get("attempts", 0)),
            "result": prior.get("result"),
            "frame_integrity": prior.get("frame_integrity"),
            "recovered_outputs": list(prior.get("recovered_outputs", [])),
        }
        current_records.append(record)

    manifest["shots"] = current_records
    _write_manifest(manifest_path, manifest)

    completed_now: list[str] = []
    skipped: list[str] = []
    failed: list[str] = []

    for index, (scene, shot, frame_count) in enumerate(jobs):
        record = current_records[index]
        output_dir = root / record["output_dir"]
        _assert_no_symlink_components(root, output_dir, "Shot output directory")

        if record["status"] == "completed" and _has_valid_frames(
            output_dir, frame_count, record.get("frame_integrity")
        ):
            skipped.append(shot["shot_id"])
            continue

        archived = _archive_output(root, output_dir, shot["shot_id"])
        if archived:
            record["recovered_outputs"].append(archived)
        record["status"] = "running"
        record["error"] = None
        record["result"] = None
        record["frame_integrity"] = None
        record["attempts"] += 1
        _write_manifest(manifest_path, manifest)

        try:
            result = render_one(scene, shot, output_dir)
            integrity = _frame_integrity(output_dir, frame_count)
            if integrity is None:
                raise BatchRenderError(
                    f"Renderer did not produce the exact {frame_count}-frame sequence "
                    f"for shot {shot['shot_id']}."
                )
            record["status"] = "completed"
            record["frame_integrity"] = integrity
            record["error"] = None
            record["result"] = {
                key: result[key]
                for key in ("return_code", "frame_count", "first_frame", "last_frame")
                if isinstance(result, dict) and key in result
            }
            completed_now.append(shot["shot_id"])
        except Exception as exc:
            record["status"] = "failed"
            record["error"] = f"{type(exc).__name__}: {exc}"
            record["errors"].append(record["error"])
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
