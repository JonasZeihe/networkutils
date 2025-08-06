#!/usr/bin/env python
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

import os
import sys
import subprocess


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    src_path = os.path.join(root, "src")
    current_path = os.environ.get("PYTHONPATH", "")
    if src_path not in current_path:
        os.environ["PYTHONPATH"] = f"{src_path}{os.pathsep}{current_path}".strip(
            os.pathsep
        )

    args = sys.argv[1:]
    default_logging = True

    if "--no-logging" in args:
        default_logging = False
        args.remove("--no-logging")

    if "--logging" in args:
        default_logging = True

    if default_logging and "--logging" not in args:
        args.append("--logging")

    cmd = [sys.executable, "-m", "app.main"] + args
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
