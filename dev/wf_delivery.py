#!/usr/bin/env python3
"""wf_delivery.py - Development script for building and publishing a release.
Name, Organisation:         Markus Breuer, STMB
Created, Last updated:      11.07.2026, 11.07.2026
"""

import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SYNC_BUILD_SCRIPT = REPO_ROOT / "dev" / "sync_build.py"
DIST_DIR = REPO_ROOT / "dist"


def run_step(title, command):
    """Run one step and stream its output directly to the terminal."""
    print(f"\n=== {title} ===")
    print("$", " ".join(command))
    process = subprocess.run(command, cwd=str(REPO_ROOT), check=False)
    if process.returncode == 0:
        print(f"[OK] {title}")
    else:
        print(f"[ERROR] {title} (Exit code {process.returncode})")
    return process.returncode


def remove_dist_directory():
    """Remove the existing dist directory if it exists."""
    print("\n=== 2) Removing old build artifacts ===")
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
        print(f"Removed {DIST_DIR}")
    else:
        print(f"No existing build directory found at {DIST_DIR}")


def ask_publish_choice():
    """Ask the user how the build should be published."""
    print("\n=== Publishing choice ===")
    print("1) Publish to TestPyPI only")
    print("2) Publish to PyPI only")
    print("3) Publish to both TestPyPI and PyPI")
    print("4) Skip publishing")
    while True:
        choice = input("Select an option [1-4]: ").strip()
        if choice in {"1", "2", "3", "4"}:
            return choice
        print("Invalid input. Please enter 1, 2, 3 or 4.")


def main():
    """Run the delivery workflow."""
    print("Starting delivery workflow...")

    steps = [
        {"title": "1) Locking dependencies with poetry", "command": ["poetry", "lock"]},
        {"title": "2) Installing dependencies with poetry", "command": ["poetry", "install"]},
        {
            "title": "3) Updating version data with sync_build.py",
            "command": ["poetry", "run", "python", str(SYNC_BUILD_SCRIPT)],
        },
    ]

    has_errors = False
    for step in steps:
        return_code = run_step(step["title"], step["command"])
        if return_code != 0:
            has_errors = True

    remove_dist_directory()

    build_steps = [
        {"title": "4) Building the distribution with poetry", "command": ["poetry", "build"]},
    ]

    for step in build_steps:
        return_code = run_step(step["title"], step["command"])
        if return_code != 0:
            has_errors = True

    choice = ask_publish_choice()
    publish_steps = []
    if choice in {"1", "3"}:
        publish_steps.append({"title": "6) Publishing to TestPyPI", "command": ["poetry", "publish", "-r", "testpypi"]})
    if choice in {"2", "3"}:
        publish_steps.append({"title": "7) Publishing to PyPI", "command": ["poetry", "publish"]})

    for step in publish_steps:
        return_code = run_step(step["title"], step["command"])
        if return_code != 0:
            has_errors = True

    print("\n=== Summary ===")
    if has_errors:
        print("At least one step failed.")
        return 1
    print("Delivery workflow completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
