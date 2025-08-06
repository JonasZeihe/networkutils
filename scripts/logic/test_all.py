#!/usr/bin/env python
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

"""
Runs all tests for the application with coverage.
"""

import os
import sys
import subprocess


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    os.chdir(root)

    os.environ["PYTHONPATH"] = os.path.join(root, "src")

    venv_python = get_venv_python()

    if not os.path.exists(venv_python):
        print("No virtual environment found. Please initialize the project first.")
        input("Press Enter to exit...")
        sys.exit(1)

    _ensure_coverage_installed(venv_python)
    print("Running tests with coverage...")

    _run_in_venv(
        venv_python, ["coverage", "run", "--source=app", "-m", "pytest", "src/tests"]
    )
    _run_in_venv(venv_python, ["coverage", "report", "-m"])

    print()
    print("Tests completed. Press Enter to exit...")
    input()


def get_venv_python():
    if os.name == "nt":
        return os.path.join("venv", "Scripts", "python.exe")
    else:
        return os.path.join("venv", "bin", "python")


def _ensure_coverage_installed(python_exe):
    try:
        result = subprocess.run(
            [python_exe, "-m", "pip", "show", "coverage"],
            capture_output=True,
            text=True,
            check=True,
            env=os.environ,
        )
        if "Name: coverage" not in result.stdout:
            raise Exception("Coverage not found")
    except Exception:
        print("Coverage not found. Installing...")
        subprocess.run(
            [python_exe, "-m", "pip", "install", "coverage"], check=True, env=os.environ
        )


def _run_in_venv(python_exe, cmd_args):
    # Baue den Befehl: python -m <cmd_args...>
    full_cmd = [python_exe, "-m"] + cmd_args
    subprocess.run(full_cmd, check=True, env=os.environ)


if __name__ == "__main__":
    main()
