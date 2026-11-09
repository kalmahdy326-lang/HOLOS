"""Safe staging of ordered, separate shot folders for episode assembly."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
from typing import Any


class EpisodeAssemblyError(RuntimeError):
    """Raised when shot frames cannot be staged safely."""


def _inside(root: Path, path: Path) -> bool:
    return path == root or root in path.parents


def stage_episode_frames(
    *,
    project_root: Path,
    episode: dict[str, Any],
    manifest: dict[str, Any],
    staging_dir: Path,
) -> dict[str, Any]:
    """Create one contiguous frame sequence in configured scene/shot order.

    Hard links avoid duplicating frame data on the same filesystem. If the
    filesystem does not support hard links, files are copied instead. Source
    shot frames are never modified.
    """
    root = project_root.resolve()
    staging = staging_dir.resolve()
    if not _inside(root, staging):
        raise EpisodeAssemblyError("Temporary frame staging must remain inside project root.")
    if staging.exists() and (not staging.is_dir() or any(staging.iterdir())):
        raise EpisodeAssemblyError(f"Staging directory must be new or empty: {staging}")
    staging.mkdir(parents=True, exist_ok=True)

    expected = [
        shot
        for scene in episode["scenes"]
        for shot in scene["shots"]
    ]
    records = manifest.get("shots")
    if not isinstance(records, list) or len(records) != len(expected):
        raise EpisodeAssemblyError("Manifest shot list does not match the episode.")

    output_index = 0
    hardlinked = 0
    copied = 0
    ordered_shots: list[str] = []

    for shot, record in zip(expected, records):
        shot_id = shot["shot_id"]
        if not isinstance(record, dict) or record.get("shot_id") != shot_id:
            raise EpisodeAssemblyError("Manifest shot order does not match the episode.")
        if record.get("status") != "completed":
            raise EpisodeAssemblyError(f"Shot {shot_id} is not completed.")
        frame_count = shot["end_frame"] - shot["start_frame"]
        if record.get("expected_frame_count") != frame_count:
            raise EpisodeAssemblyError(f"Manifest frame count mismatch for {shot_id}.")

        relative = Path(record.get("output_dir", ""))
        if relative.is_absolute():
            raise EpisodeAssemblyError(f"Absolute frame directory is not allowed: {relative}")
        source_dir = (root / relative).resolve()
        if not _inside(root, source_dir) or source_dir.is_symlink() or not source_dir.is_dir():
            raise EpisodeAssemblyError(f"Unsafe or missing shot frame directory: {source_dir}")

        for local_index in range(frame_count):
            filename = f"frame_{local_index:06d}.png"
            source = source_dir / filename
            if source.is_symlink() or not source.is_file() or source.stat().st_size == 0:
                raise EpisodeAssemblyError(f"Missing or invalid frame: {source}")
            destination = staging / f"frame_{output_index:06d}.png"
            try:
                os.link(source, destination)
                hardlinked += 1
            except OSError:
                try:
                    shutil.copy2(source, destination)
                    copied += 1
                except OSError as exc:
                    raise EpisodeAssemblyError(
                        f"Could not stage frame {source}: {exc}"
                    ) from exc
            output_index += 1
        ordered_shots.append(shot_id)

    return {
        "frame_count": output_index,
        "ordered_shots": ordered_shots,
        "hardlinked_frames": hardlinked,
        "copied_frames": copied,
        "staging_dir": str(staging),
    }
