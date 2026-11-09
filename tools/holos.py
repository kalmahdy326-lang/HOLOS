#!/usr/bin/env python3
"""HOLOS Local Production Engine command-line entry point."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from holos_engine.config import ConfigError, load_episode
from holos_engine.controller import write_preflight_report
from holos_engine.preflight import run_preflight


def main() -> int:
    parser = argparse.ArgumentParser(prog="holos", description="HOLOS local production tools")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("validate", "preflight", "render"):
        command = subparsers.add_parser(name)
        command.add_argument("--episode", required=True, type=Path)
        command.add_argument("--mode", choices=("debug", "production"), default="production")

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

        print(
            "Rendering is not available yet: the Godot shot-render adapter "
            "and FFmpeg assembly stage have not been implemented.",
            file=sys.stderr,
        )
        print("Run 'preflight' to check the local toolchain and configured assets.",
              file=sys.stderr)
        return 2

    except (ConfigError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
