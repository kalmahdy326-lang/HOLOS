#!/usr/bin/env python3
"""HOLOS Local Production Engine command-line entry point."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from holos_engine.config import ConfigError, load_episode
from holos_engine.controller import write_preflight_report
from holos_engine.media import MediaError, assemble_video, probe_media, validate_media
from holos_engine.preflight import run_preflight


def _episode_frame_count(episode: dict) -> int:
    return sum(
        shot["end_frame"] - shot["start_frame"]
        for scene in episode["scenes"]
        for shot in scene["shots"]
    )


def _inside(root: Path, path: Path) -> bool:
    return path == root or root in path.parents


def main() -> int:
    parser = argparse.ArgumentParser(prog="holos", description="HOLOS local production tools")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("validate", "preflight", "render"):
        command = subparsers.add_parser(name)
        command.add_argument("--episode", required=True, type=Path)
        command.add_argument("--mode", choices=("debug", "production"), default="production")

    assemble = subparsers.add_parser("assemble")
    assemble.add_argument("--episode", required=True, type=Path)
    assemble.add_argument("--frames-dir", required=True, type=Path)
    assemble.add_argument("--output", required=True, type=Path)
    assemble.add_argument("--mode", choices=("debug", "production"), default="production")

    args = parser.parse_args()
    root = args.project_root.resolve()
    config_path = args.episode
    if not config_path.is_absolute():
        config_path = root / config_path

    try:
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

        if args.command == "assemble":
            frames_dir = (root / args.frames_dir).resolve()
            output = (root / args.output).resolve()
            if not _inside(root, frames_dir) or not _inside(root, output):
                raise MediaError("Frames and output paths must remain inside project root.")

            audio = episode.get("audio", {})
            dialogue = (root / audio["dialogue"]).resolve() if audio.get("dialogue") else None
            music = (root / audio["music"]).resolve() if audio.get("music") else None
            for label, path in (("dialogue", dialogue), ("music", music)):
                if path is not None and not _inside(root, path):
                    raise MediaError(f"{label} path must remain inside project root.")

            render = episode["render"]
            frame_count = _episode_frame_count(episode)
            result = assemble_video(
                frames_dir=frames_dir,
                fps=render["fps"],
                frame_count=frame_count,
                output=output,
                dialogue=dialogue,
                music=music,
            )
            metadata = probe_media(output)
            validation = validate_media(
                metadata,
                width=render["width"],
                height=render["height"],
                fps=render["fps"],
                expected_duration=frame_count / float(render["fps"]),
                require_audio=(dialogue is not None or music is not None),
            )
            report = {
                "episode_id": episode["episode_id"],
                "mode": args.mode,
                "assembly": result,
                "validation": validation,
            }
            report_dir = root / "output" / "reports"
            report_dir.mkdir(parents=True, exist_ok=True)
            report_path = report_dir / f"{episode['episode_id']}-media-validation.json"
            report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(report, indent=2))
            print(f"Media validation report: {report_path}")
            return 0 if validation["valid"] else 1

        print(
            "Rendering is not available yet: the Godot shot scheduler and "
            "production controller integration are still under development.",
            file=sys.stderr,
        )
        print("Run 'preflight' to check the local toolchain and configured assets.",
              file=sys.stderr)
        return 2

    except (ConfigError, MediaError, OSError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
