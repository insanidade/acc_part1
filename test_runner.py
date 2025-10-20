#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Execute DemoQA automation scripts in the prescribed order.

Author: Otávio Augusto
Date: 2025-10-19
Description:
    - Maintain the ordered list of DemoQA workflow scripts to execute.
    - Run each script via the current Python interpreter, halting on failure.
    - Provide console feedback for script start/completion and overall success.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path


def run_script(script_path: Path) -> dict[str, object]:
    """Execute the given Python script using the current interpreter."""

    separator = "#" * 72
    print(f"\n{separator}")
    print(f"\nRunning {script_path.name}...")

    start = time.perf_counter()
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=script_path.parent,
        check=False,
    )
    duration = time.perf_counter() - start

    return {
        "scenario": script_path.name,
        "success": result.returncode == 0,
        "duration": duration,
        "details": (
            "Completed successfully"
            if result.returncode == 0
            else f"Exited with code {result.returncode}"
        ),
    }


def main() -> None:
    base_dir = Path(__file__).resolve().parent

    ordered_scripts = [
        base_dir / "test_create_user.py",
        base_dir / "test_generate_token.py",
        base_dir / "test_authorize_user.py",
        base_dir / "test_fetch_books.py",
        base_dir / "test_rent_book.py",
        base_dir / "test_get_user_and_rent_books.py",
    ]

    summary: list[dict[str, object]] = []

    for script in ordered_scripts:
        if not script.exists():
            raise FileNotFoundError(f"Required script not found: {script}")
        outcome = run_script(script)
        summary.append(outcome)
        if not outcome["success"]:
            break

    separator = "#" * 72
    print(f"\n{separator}")
    print("Execution summary:")
    for entry in summary:
        scenario = entry["scenario"]
        duration = entry["duration"]
        success = entry["success"]
        details = entry["details"]
        print(f"- Scenario: {scenario}")
        print(f"  Duration: {duration:.2f} seconds")
        print(f"  Outcome: {'Success' if success else 'Failure'}")
        if not success:
            print(f"  Details: {details}")

    if all(entry["success"] for entry in summary) and summary:
        print("\nAll DemoQA scripts executed successfully.")
    else:
        print("\nAt least one DemoQA script failed.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Execution failed: {exc}")
        sys.exit(1)

