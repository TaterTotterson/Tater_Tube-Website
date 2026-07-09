#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
WEBSITE_DIR = SCRIPT_DIR.parent
BUILD_SCRIPT = SCRIPT_DIR / "build_wiki.py"
SYNC_SCRIPT = SCRIPT_DIR / "sync_wiki_sources.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def log(message: str) -> None:
    print(f"[{utc_now()}] {message}", flush=True)


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(args, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    return completed


def git_status() -> str:
    if not (WEBSITE_DIR / ".git").exists():
        return ""
    return run(["git", "status", "--short", "--", "."], cwd=WEBSITE_DIR).stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh the generated Tater Tube website.")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if generated files are dirty after build.")
    parser.add_argument("--skip-sync", action="store_true", help="Do not copy source docs/assets before building.")
    parser.add_argument("--skip-build", action="store_true", help="Only run the optional generated-output check.")
    args = parser.parse_args()

    if not args.skip_sync:
        log("Syncing Tater Tube docs and assets")
        run([sys.executable, str(SYNC_SCRIPT)], cwd=WEBSITE_DIR)

    if not args.skip_build:
        log("Building static website")
        run([sys.executable, str(BUILD_SCRIPT)], cwd=WEBSITE_DIR)

    if args.check:
        log("Checking generated website status")
        status = git_status()
        if status:
            print(status)
            raise SystemExit("Generated website files differ from the committed tree.")

    log("Website update complete")


if __name__ == "__main__":
    main()

