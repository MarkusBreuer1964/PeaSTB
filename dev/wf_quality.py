#!/usr/bin/env python3
"""wf_quality.py - Development script for formatting, linting, and testing.
Name, Organisation:         Markus Breuer, STMB
Created, Last updated:      12.06.2026, 12.06.2026
"""

import subprocess
from pathlib import Path
import toml

CONFIG_PATH = Path(__file__).with_name("wf_quality.toml")


def load_config():
    """Load workflow configuration from the TOML file."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration file is missing: {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        data = toml.load(config_file)

    if "quality" not in data:
        raise ValueError("Section [quality] is missing in wf_quality.toml")

    line_length = data["quality"].get("line_length")
    if not isinstance(line_length, int) or line_length <= 0:
        raise ValueError("quality.line_length must be a positive integer")

    data.setdefault("paths", {})
    data["paths"].setdefault("format", ["peastb", "tests", "dev"])
    data["paths"].setdefault("lint", ["peastb", "tests", "dev"])
    data["paths"].setdefault("test", ["tests"])
    data["quality"].setdefault("pylint_disable", [])
    return data


def run_step(title, command):
    """Run one step and stream its output directly to the terminal."""
    print(f"\n=== {title} ===")
    print("$", " ".join(command))

    process = subprocess.run(command, check=False)
    if process.returncode == 0:
        print(f"[OK] {title}")
    else:
        print(f"[ERROR] {title} (Exit code {process.returncode})")
    return process.returncode


def main():
    """Run the quality workflow."""
    try:
        config = load_config()
    except (FileNotFoundError, ValueError) as exc:
        print(f"Configuration error: {exc}")
        return 2

    line_length = str(config["quality"]["line_length"])
    black_target_version = config["quality"].get("black_target_version", "py312")
    pylint_disable = ",".join(config["quality"]["pylint_disable"])
    format_paths = config["paths"]["format"]
    lint_paths = config["paths"]["lint"]
    test_paths = config["paths"]["test"]

    steps = [
        {
            "title": "1) Formatting with black",
            "command": ["black", f"--line-length={line_length}", f"--target-version={black_target_version}", *format_paths],
        },
        {"title": "2a) Static analysis with flake8", "command": ["flake8", f"--max-line-length={line_length}", *lint_paths]},
        {
            "title": "2b) Static analysis with pylint",
            "command": ["pylint", f"--max-line-length={line_length}", f"--disable={pylint_disable}", *lint_paths],
        },
        {"title": "3) Testing with pytest", "command": ["pytest", *test_paths]},
    ]

    has_errors = False
    for step in steps:
        return_code = run_step(step["title"], step["command"])
        if return_code != 0:
            has_errors = True

    print("\n=== Summary ===")
    if has_errors:
        print("At least one step failed.")
        return 1

    print("All quality steps passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
