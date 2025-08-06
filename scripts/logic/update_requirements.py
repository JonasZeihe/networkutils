#!/usr/bin/env python
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

import os
import sys
import subprocess


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    os.chdir(root)

    if not os.path.isdir("venv"):
        print("No virtual environment found. Please initialize the project first.")
        input("Press Enter to exit...")
        sys.exit(1)

    print("Updating requirements.txt...")
    _run_in_venv(["pip", "freeze"], output="requirements.txt")
    print("Requirements updated successfully.")


def _run_in_venv(cmd, output=None):
    if os.name == "nt":
        act = os.path.join("venv", "Scripts", "activate.bat")
        full_cmd = f'call "{act}" && ' + " ".join(cmd)
        if output:
            full_cmd += f" > {output}"
        subprocess.run(full_cmd, shell=True, check=True)
    else:
        act = "./venv/bin/activate"
        joined = " ".join(cmd)
        if output:
            joined += f" > {output}"
        full_cmd = f'. "{act}" && {joined}'
        subprocess.run(full_cmd, shell=True, check=True)


if __name__ == "__main__":
    main()
