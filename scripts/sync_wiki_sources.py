#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
WEBSITE_DIR = SCRIPT_DIR.parent
PUBLIC_ROOT = WEBSITE_DIR / "public_html"
IMAGE_DIR = PUBLIC_ROOT / "assets" / "images"
FONT_DIR = PUBLIC_ROOT / "assets" / "fonts"
SOURCE_DOC_DIR = WEBSITE_DIR / "docs" / "source"
SOURCE_REPO_URL = os.getenv("TATER_TUBE_SOURCE_REPO", "https://github.com/TaterTotterson/Tater-Tube.git")
SOURCE_REF = os.getenv("TATER_TUBE_SOURCE_REF", "main")
SOURCE_CACHE_DIR = WEBSITE_DIR / ".cache" / "tater-tube-source"


def run_git(args: list[str], *, cwd: Path | None = None) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True)


def ensure_source_cache() -> Path:
    SOURCE_CACHE_DIR.parent.mkdir(parents=True, exist_ok=True)

    if not (SOURCE_CACHE_DIR / ".git").exists():
        if SOURCE_CACHE_DIR.exists():
            shutil.rmtree(SOURCE_CACHE_DIR)
        run_git(["clone", "--depth", "1", "--branch", SOURCE_REF, SOURCE_REPO_URL, str(SOURCE_CACHE_DIR)])
    else:
        run_git(["remote", "set-url", "origin", SOURCE_REPO_URL], cwd=SOURCE_CACHE_DIR)
        run_git(["fetch", "--depth", "1", "origin", SOURCE_REF], cwd=SOURCE_CACHE_DIR)
        run_git(["reset", "--hard", f"origin/{SOURCE_REF}"], cwd=SOURCE_CACHE_DIR)

    return SOURCE_CACHE_DIR.resolve()


def resolve_source_dir() -> Path:
    override = os.getenv("TATER_TUBE_SOURCE_DIR", "").strip()
    if override:
        return Path(override).expanduser().resolve()

    return ensure_source_cache()


def copy_if_exists(source: Path, target: Path) -> None:
    if not source.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    source_dir = resolve_source_dir()
    if not (source_dir / "README.md").exists() or not (source_dir / "assets").exists():
        raise SystemExit(f"Tater Tube source repo is missing expected files: {source_dir}")

    SOURCE_DOC_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    FONT_DIR.mkdir(parents=True, exist_ok=True)

    for name in ["README.md", "INSTALL.md", "BUILDING.md"]:
        copy_if_exists(source_dir / name, SOURCE_DOC_DIR / name)

    copy_if_exists(source_dir / "assets/images/tater-tube-readme.png", IMAGE_DIR / "tater-tube-logo.png")
    copy_if_exists(source_dir / "assets/images/tater-tube-boot.png", IMAGE_DIR / "tater-tube-boot.png")
    copy_if_exists(source_dir / "assets/images/static-noise-strip.png", IMAGE_DIR / "static-noise-strip.png")
    copy_if_exists(source_dir / "assets/fonts/VCR_OSD_MONO_1.001.ttf", FONT_DIR / "vcr-osd-mono.ttf")

    mascot_dir = source_dir / "assets/images/mascots"
    if mascot_dir.exists():
        for image in mascot_dir.glob("*.png"):
            copy_if_exists(image, IMAGE_DIR / image.name)

    print(f"Synced Tater Tube docs and assets from {source_dir}")


if __name__ == "__main__":
    main()
