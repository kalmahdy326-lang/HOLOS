#!/usr/bin/env python3
"""HOLOS Local Production Engine command-line entry point."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import tempfile

# Allow direct execution as `python tools/holos.py ...` from a clean checkout.
_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))

from holos_engine.backup import (
    BackupError,
    create_source_backup,
    restore_source_backup,
)
from holos_engine.batch import (
    BatchRenderError,
    load_completed_batch_manifest,
    render_episode_batch,
)
from holos_engine.episode_assembly import EpisodeAssemblyError, stage_episode_frames
from holos_engine.config import ConfigError, load_episode
from holos_engine.controller import write_preflight_report
from holos_engine.godot_adapter import GodotAdapterError, render_shot
from holos_engine.godot_assets import GodotAssetAuditError, audit_godot_project
from holos_engine.media import MediaError, assemble_video, probe_media, validate_media
from holos_engine.preflight import run_preflight
from holos_engine.inventory import InventoryError, write_inventory_report


def _episode_frame_count(episode: dict) -> int:
    return sum(
        shot["end_frame"] - shot["start_frame"]
        for scene in episode["scenes"]
        for shot in scene["shots"]
    )


def _find_shot_context(episode: dict, shot_id: str) -> tuple[dict, dict]:
    for scene in episode["scenes"]:
        for shot in scene["shots"]:
            if shot["shot_id"] == shot_id:
                return scene, shot
    raise ConfigError(f"Shot not found in episode configuration: {shot_id}")


def _safe_component(value: str, label: str) -> None:
    if (
        not isinstance(value, str)
        or not value
        or value in {".", ".."}
        or "/" in value
        or "\\" in value
        or Path(value).is_absolute()
    ):
        raise ConfigError(f"{label} must be a single safe path component: {value!r}")


def _inside(root: Path, path: Path) -> bool:
    return path == root or root in path.parents


def _render_configured_shot(
    *,
    root: Path,
    episode: dict,
    scene: dict,
    shot: dict,
    mode: str,
    godot_project: Path,
    godot_executable: str | None,
    display_wrapper: str | None,
    output_dir: Path,
) -> dict:
    episode_id = episode["episode_id"]
    shot_id = shot["shot_id"]
    _safe_component(episode_id, "episode_id")
    _safe_component(shot_id, "shot_id")

    scene_path = shot.get("scene")
    if not isinstance(scene_path, str) or not scene_path.startswith("res://"):
        raise ConfigError(
            f"Shot {shot_id} must define a Godot scene using a res:// path."
        )

    render_settings = episode["render"]
    shot_config = {
        "scene": scene_path,
        "shot_id": shot_id,
        "start_frame": shot["start_frame"],
        "end_frame": shot["end_frame"],
        "fps": render_settings["fps"],
        "width": render_settings["width"],
        "height": render_settings["height"],
        "mode": mode,
        "debug_overlay": (
            mode == "debug" and bool(render_settings.get("debug_overlay", False))
        ),
    }

    absolute_output = output_dir if output_dir.is_absolute() else root / output_dir
    absolute_output = absolute_output.resolve()
    if not _inside(root, absolute_output):
        raise ConfigError(f"Shot output directory must remain inside project root: {absolute_output}")
    relative_output = absolute_output.relative_to(root)

    runtime_root = root / "output" / ".holos_runtime"
    runtime_root.mkdir(parents=True, exist_ok=True)
    prefix = (display_wrapper, "-a") if display_wrapper else ()

    with tempfile.TemporaryDirectory(prefix="shot-config-", dir=runtime_root) as temporary:
        temporary_config = Path(temporary) / "shot.json"
        temporary_config.write_text(
            json.dumps(shot_config, indent=2) + "\n", encoding="utf-8"
        )
        config_relative = temporary_config.relative_to(root)
        result = render_shot(
            project_root=root,
            godot_project=godot_project,
            runner_script="res://holos_shot_runner.gd",
            shot_config=config_relative,
            output_dir=relative_output,
            expected_frame_count=shot["end_frame"] - shot["start_frame"],
            executable=godot_executable,
            headless=False,
            command_prefix=prefix,
        )

    report = {
        "episode_id": episode_id,
        "scene_id": scene["scene_id"],
        "shot_id": shot_id,
        "mode": mode,
        "scene": scene_path,
        "render": {
            "width": render_settings["width"],
            "height": render_settings["height"],
            "fps": render_settings["fps"],
        },
        "output_dir": str(relative_output),
        "result": result,
    }
    report_dir = root / "output" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{episode_id}-{mode}-{shot_id}-render.json"
    if not _inside(root, report_path.resolve()):
        raise ConfigError("Shot report path must remain inside project root.")
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(prog="holos", description="HOLOS local production tools")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory = subparsers.add_parser(
        "inventory", help="Create a read-only SHA-256 inventory of project source files"
    )
    inventory.add_argument(
        "--output", type=Path,
        help="Optional report path under output/reports (default: timestamped report)",
    )

    asset_audit = subparsers.add_parser(
        "audit-godot-assets",
        help="Check literal res:// resource dependencies in the Godot project",
    )
    asset_audit.add_argument("--godot-project", type=Path, default=Path("godot"))
    asset_audit.add_argument(
        "--output", type=Path,
        help="Optional report path under output/reports (default: timestamped report)",
    )

    backup = subparsers.add_parser(
        "backup", help="Create and verify a source copy from a complete inventory"
    )
    backup.add_argument("--inventory", required=True, type=Path)
    backup.add_argument(
        "--destination", type=Path,
        help="Optional new directory under output/backups (default: timestamped)",
    )

    restore = subparsers.add_parser(
        "restore", help="Verify a source backup and restore it into a new directory"
    )
    restore.add_argument("--backup", required=True, type=Path)
    restore.add_argument(
        "--destination", type=Path,
        help="Optional new directory under output/restores (default: timestamped)",
    )

    for name in ("validate", "preflight"):
        command = subparsers.add_parser(name)
        command.add_argument("--episode", required=True, type=Path)
        command.add_argument("--mode", choices=("debug", "production"), default="production")

    for name in ("render", "render-episode"):
        command = subparsers.add_parser(name)
        command.add_argument("--episode", required=True, type=Path)
        command.add_argument("--mode", choices=("debug", "production"), default="production")
        command.add_argument("--godot-project", type=Path, default=Path("godot"))
        command.add_argument("--godot-executable")
        command.add_argument("--display-wrapper", help="Optional wrapper such as xvfb-run")
        if name == "render":
            command.add_argument("--shot", required=True)

    assemble = subparsers.add_parser("assemble")
    assemble.add_argument("--episode", required=True, type=Path)
    assemble.add_argument("--frames-dir", required=True, type=Path)
    assemble.add_argument("--output", required=True, type=Path)
    assemble.add_argument("--mode", choices=("debug", "production"), default="production")

    assemble_episode = subparsers.add_parser(
        "assemble-episode", help="Assemble verified shot renders into one episode video"
    )
    assemble_episode.add_argument("--episode", required=True, type=Path)
    assemble_episode.add_argument("--output", required=True, type=Path)
    assemble_episode.add_argument("--mode", choices=("debug", "production"), default="production")

    args = parser.parse_args()
    root = args.project_root.resolve()

    try:
        if args.command == "inventory":
            report_path, report = write_inventory_report(root, args.output)
            print(json.dumps(report["summary"], indent=2))
            print(f"Inventory status: {report['status']}")
            print(f"Inventory report: {report_path}")
            return 0 if report["status"] == "complete" else 1

        if args.command == "audit-godot-assets":
            report = audit_godot_project(
                project_root=root, godot_project=args.godot_project
            )
            report_dir = root / "output" / "reports"
            current = root
            for part in report_dir.relative_to(root).parts:
                current = current / part
                if current.is_symlink():
                    raise GodotAssetAuditError(
                        f"Audit report directory must not traverse symbolic links: {current}"
                    )
            report_dir.mkdir(parents=True, exist_ok=True)
            if args.output is None:
                stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
                report_path = report_dir / f"godot-asset-audit-{stamp}.json"
            else:
                report_path = (
                    args.output if args.output.is_absolute()
                    else root / args.output
                )
            report_path = Path(os.path.abspath(report_path))
            if not _inside(root, report_path) or report_dir not in report_path.parents:
                raise GodotAssetAuditError(
                    "Godot asset audit report must be under output/reports."
                )
            current = root
            for part in report_path.relative_to(root).parts:
                current = current / part
                if current.is_symlink():
                    raise GodotAssetAuditError(
                        f"Audit report path must not traverse symbolic links: {current}"
                    )
            if report_path.exists():
                raise GodotAssetAuditError(
                    f"Refusing to overwrite existing audit report: {report_path}"
                )
            temporary_path = None
            try:
                with tempfile.NamedTemporaryFile(
                    mode="w", encoding="utf-8", prefix=".godot-audit-",
                    suffix=".tmp", dir=report_dir, delete=False
                ) as stream:
                    json.dump(report, stream, indent=2)
                    stream.write("\n")
                    stream.flush()
                    os.fsync(stream.fileno())
                    temporary_path = Path(stream.name)
                os.replace(temporary_path, report_path)
            except Exception:
                if temporary_path is not None:
                    temporary_path.unlink(missing_ok=True)
                raise
            print(json.dumps(report["summary"], indent=2))
            print(f"Godot asset audit status: {report['status']}")
            print(f"Godot asset audit report: {report_path}")
            return 0 if report["status"] == "complete" else 1

        if args.command == "backup":
            inventory_path = (
                args.inventory if args.inventory.is_absolute()
                else root / args.inventory
            )
            backup_path, manifest = create_source_backup(
                project_root=root,
                inventory_path=inventory_path,
                destination=args.destination,
            )
            print(json.dumps({
                "backup_path": str(backup_path),
                "status": manifest["status"],
                "file_count": manifest["file_count"],
                "total_size_bytes": manifest["total_size_bytes"],
                "source_inventory_sha256": manifest["source_inventory_sha256"],
            }, indent=2))
            return 0

        if args.command == "restore":
            backup_path = args.backup if args.backup.is_absolute() else root / args.backup
            restored_path, manifest = restore_source_backup(
                project_root=root,
                backup_path=backup_path,
                destination=args.destination,
            )
            print(json.dumps({
                "restore_path": str(restored_path),
                "status": manifest["status"],
                "file_count": manifest["file_count"],
                "total_size_bytes": manifest["total_size_bytes"],
                "source_backup": manifest["source_backup"],
            }, indent=2))
            return 0

        config_path = args.episode
        if not config_path.is_absolute():
            config_path = root / config_path

        episode = load_episode(config_path)
        print(f"Configuration valid: {episode['episode_id']}")

        if args.command == "validate":
            return 0

        if args.command == "preflight":
            result = run_preflight(root, episode)
            print(json.dumps(result, indent=2))
            report = write_preflight_report(root, episode)
            print(f"Preflight report: {report}")
            return 1 if result["missing_assets"] else 0

        if args.command == "render":
            scene, shot = _find_shot_context(episode, args.shot)
            output_dir = (
                Path("output") / "renders" / episode["episode_id"] / args.mode / shot["shot_id"]
            )
            result = _render_configured_shot(
                root=root,
                episode=episode,
                scene=scene,
                shot=shot,
                mode=args.mode,
                godot_project=args.godot_project,
                godot_executable=args.godot_executable,
                display_wrapper=args.display_wrapper,
                output_dir=output_dir,
            )
            print(json.dumps(result, indent=2))
            return 0

        if args.command == "render-episode":
            def render_one(scene: dict, shot: dict, output_dir: Path) -> dict:
                return _render_configured_shot(
                    root=root,
                    episode=episode,
                    scene=scene,
                    shot=shot,
                    mode=args.mode,
                    godot_project=args.godot_project,
                    godot_executable=args.godot_executable,
                    display_wrapper=args.display_wrapper,
                    output_dir=output_dir,
                )

            result = render_episode_batch(
                project_root=root,
                episode=episode,
                mode=args.mode,
                render_one=render_one,
            )
            report = {
                "episode_id": episode["episode_id"],
                "mode": args.mode,
                "batch": result,
            }
            report_dir = root / "output" / "reports"
            report_dir.mkdir(parents=True, exist_ok=True)
            report_path = report_dir / f"{episode['episode_id']}-{args.mode}-batch.json"
            if not _inside(root, report_path.resolve()):
                raise ConfigError("Batch report path must remain inside project root.")
            report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(report, indent=2))
            print(f"Batch report: {report_path}")
            return 0 if result["success"] else 1

        if args.command == "assemble-episode":
            _safe_component(episode["episode_id"], "episode_id")
            output = args.output if args.output.is_absolute() else root / args.output
            output = output.resolve()
            if not _inside(root, output):
                raise MediaError("Episode output path must remain inside project root.")
            if output.exists():
                raise MediaError(f"Refusing to overwrite existing output: {output}")

            manifest_path, manifest = load_completed_batch_manifest(
                project_root=root, episode=episode, mode=args.mode,
            )
            audio = episode.get("audio", {})
            dialogue = (root / audio["dialogue"]).resolve() if audio.get("dialogue") else None
            music = (root / audio["music"]).resolve() if audio.get("music") else None
            for label, path in (("dialogue", dialogue), ("music", music)):
                if path is not None and not _inside(root, path):
                    raise MediaError(f"{label} path must remain inside project root.")

            render_settings = episode["render"]
            frame_count = _episode_frame_count(episode)
            runtime_root = root / "output" / ".holos_runtime"
            runtime_root.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(
                prefix="episode-assembly-", dir=runtime_root
            ) as temporary:
                temporary_root = Path(temporary)
                staged_dir = temporary_root / "frames"
                staged = stage_episode_frames(
                    project_root=root,
                    episode=episode,
                    manifest=manifest,
                    staging_dir=staged_dir,
                )
                if staged["frame_count"] != frame_count:
                    raise EpisodeAssemblyError(
                        f"Staged {staged['frame_count']} frames; expected {frame_count}."
                    )
                temporary_output = temporary_root / "episode.mp4"
                assembly = assemble_video(
                    frames_dir=staged_dir,
                    fps=render_settings["fps"],
                    frame_count=frame_count,
                    output=temporary_output,
                    dialogue=dialogue,
                    music=music,
                )
                metadata = probe_media(temporary_output)
                validation = validate_media(
                    metadata,
                    width=render_settings["width"],
                    height=render_settings["height"],
                    fps=render_settings["fps"],
                    expected_duration=frame_count / float(render_settings["fps"]),
                    require_audio=(dialogue is not None or music is not None),
                    sync_tolerance_seconds=(
                        float(audio.get("sync_tolerance_ms", 80)) / 1000.0
                    ),
                )
                if not validation["valid"]:
                    raise MediaError(
                        "Episode output failed validation: "
                        + "; ".join(validation["errors"])
                    )
                if output.exists():
                    raise MediaError(
                        f"Refusing to overwrite output created during assembly: {output}"
                    )
                output.parent.mkdir(parents=True, exist_ok=True)
                temporary_output.replace(output)
                assembly["output"] = str(output)

            report = {
                "episode_id": episode["episode_id"],
                "mode": args.mode,
                "manifest": str(manifest_path),
                "ordered_shots": staged["ordered_shots"],
                "frame_staging": {
                    "frame_count": staged["frame_count"],
                    "hardlinked_frames": staged["hardlinked_frames"],
                    "copied_frames": staged["copied_frames"],
                },
                "assembly": assembly,
                "validation": validation,
            }
            report_dir = root / "output" / "reports"
            report_dir.mkdir(parents=True, exist_ok=True)
            report_path = (
                report_dir / f"{episode['episode_id']}-{args.mode}-episode-assembly.json"
            )
            if not _inside(root, report_path.resolve()):
                raise ConfigError("Episode assembly report path must remain inside project root.")
            report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(report, indent=2))
            print(f"Episode assembly report: {report_path}")
            return 0 if validation["valid"] else 1

        if args.command == "assemble":
            frames_dir = (root / args.frames_dir).resolve()
            output = (root / args.output).resolve()
            if not _inside(root, frames_dir) or not _inside(root, output):
                raise MediaError("Frames and output paths must remain inside project root.")
            if output.exists():
                raise MediaError(f"Refusing to overwrite existing output: {output}")

            audio = episode.get("audio", {})
            dialogue = (root / audio["dialogue"]).resolve() if audio.get("dialogue") else None
            music = (root / audio["music"]).resolve() if audio.get("music") else None
            for label, path in (("dialogue", dialogue), ("music", music)):
                if path is not None and not _inside(root, path):
                    raise MediaError(f"{label} path must remain inside project root.")

            render_settings = episode["render"]
            frame_count = _episode_frame_count(episode)
            runtime_root = root / "output" / ".holos_runtime"
            runtime_root.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(
                prefix="frame-assembly-", dir=runtime_root
            ) as temporary:
                temporary_output = Path(temporary) / "assembled.mp4"
                result = assemble_video(
                    frames_dir=frames_dir,
                    fps=render_settings["fps"],
                    frame_count=frame_count,
                    output=temporary_output,
                    dialogue=dialogue,
                    music=music,
                )
                metadata = probe_media(temporary_output)
                validation = validate_media(
                    metadata,
                    width=render_settings["width"],
                    height=render_settings["height"],
                    fps=render_settings["fps"],
                    expected_duration=frame_count / float(render_settings["fps"]),
                    require_audio=(dialogue is not None or music is not None),
                    sync_tolerance_seconds=(
                        float(audio.get("sync_tolerance_ms", 80)) / 1000.0
                    ),
                )
                if not validation["valid"]:
                    raise MediaError(
                        "Assembled output failed validation: "
                        + "; ".join(validation["errors"])
                    )
                if output.exists():
                    raise MediaError(
                        f"Refusing to overwrite output created during assembly: {output}"
                    )
                output.parent.mkdir(parents=True, exist_ok=True)
                temporary_output.replace(output)
                result["output"] = str(output)

            report = {
                "episode_id": episode["episode_id"],
                "mode": args.mode,
                "assembly": result,
                "validation": validation,
            }
            report_dir = root / "output" / "reports"
            report_dir.mkdir(parents=True, exist_ok=True)
            report_path = report_dir / f"{episode['episode_id']}-{args.mode}-media-validation.json"
            if not _inside(root, report_path.resolve()):
                raise ConfigError("Media validation report path must remain inside project root.")
            report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(report, indent=2))
            print(f"Media validation report: {report_path}")
            return 0


    except (
        BatchRenderError,
        EpisodeAssemblyError,
        GodotAssetAuditError,
        InventoryError,
        BackupError,
        ConfigError,
        GodotAdapterError,
        MediaError,
        OSError,
        KeyError,
        ValueError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
