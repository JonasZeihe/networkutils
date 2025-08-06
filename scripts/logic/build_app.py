#!/usr/bin/env python
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

"""
Build script for creating a standalone executable of the application
via PyInstaller or similar tools.
"""

import os
import sys
import subprocess
import shutil


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    os.chdir(root)

    if not os.path.isdir("venv"):
        print("No virtual environment found. Please initialize the project first.")
        input("Press Enter to exit...")
        sys.exit(1)

    _run_in_venv(["python", "-m", "pip", "install", "--upgrade", "pip"])
    _run_in_venv(["pip", "install", "-r", "requirements.txt"])
    _run_in_venv(["python", "-m", "pip", "show", "pyinstaller"], check_install=True)

    dist_path = os.path.join(root, "dist")
    build_path = os.path.join(root, "build")
    _rmdir(dist_path)
    _rmdir(build_path)

    image_path = os.path.join(root, "images", "background.jpeg")
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",
        "--name",
        "Application",
        "src/app/main.py",
    ]

    if os.path.exists(image_path):
        pyinstaller_cmd.append(f"--add-data={image_path}{os.pathsep}images")

    print("Building with PyInstaller...")
    _run_in_venv(pyinstaller_cmd)
    print("Build complete. Executable is in 'dist' folder.")


def _run_in_venv(cmd, check_install=False):
    """
    Runs a command inside the virtual environment. If check_install=True and
    the module isn't installed, it installs it before continuing.
    """
    activate = (
        os.path.join("venv", "Scripts", "activate.bat")
        if os.name == "nt"
        else "./venv/bin/activate"
    )
    shell_prefix = (
        f'call "{activate}" && ' if os.name == "nt" else f'. "{activate}" && '
    )

    if check_install and "show" in cmd:
        ret = subprocess.run(
            shell_prefix + " ".join(cmd), shell=True, capture_output=True, text=True
        )
        if "Name: PyInstaller" not in ret.stdout:
            _install_pyinstaller(activate)

    subprocess.run(shell_prefix + " ".join(cmd), shell=True, check=True)


def _install_pyinstaller(activate):
    install_cmd = (
        f'call "{activate}" && python -m pip install pyinstaller'
        if os.name == "nt"
        else f'. "{activate}" && python -m pip install pyinstaller'
    )
    subprocess.run(install_cmd, shell=True, check=True)


def _rmdir(path):
    if os.path.isdir(path):
        print(f"Removing {path}...")
        shutil.rmtree(path)


if __name__ == "__main__":
    main()
