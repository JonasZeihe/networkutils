#!/usr/bin/env python
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

import os
import sys
import platform
import subprocess
import shutil


def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    os.chdir(root)

    if not os.path.isdir("venv"):
        print("Creating virtual environment...")
        _run([sys.executable, "-m", "venv", "--upgrade-deps", "venv"])
    else:
        print("Virtual environment already exists.")

    _run_in_venv(
        [
            "python",
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
            "--break-system-packages",
        ]
    )

    if not _has_module("pipreqsnb"):
        print("Installing pipreqsnb...")
        _run_in_venv(
            ["python", "-m", "pip", "install", "--break-system-packages", "pipreqsnb"]
        )

    print("Generating requirements.txt with pipreqsnb (ignoring venv)...")
    _run_in_venv_cmd("pipreqsnb . --force --ignore venv")

    if os.path.isfile("requirements.txt"):
        print("Installing from requirements.txt...")
        _run_in_venv(
            [
                "python",
                "-m",
                "pip",
                "install",
                "--no-cache-dir",
                "--break-system-packages",
                "-r",
                "requirements.txt",
            ]
        )

    if platform.system() == "Darwin" and not _has_tkinter():
        print("tkinter not found, attempting brew install python-tk...")
        _maybe_brew_install_tk()

    print("Freezing final requirements.txt...")
    _run_in_venv(["python", "-m", "pip", "freeze"], output="requirements.txt")

    print("Initialization complete.")


def _run(cmd, check=True):
    if cmd[0] == "python":
        cmd[0] = sys.executable
    subprocess.run(cmd, check=check)


def _run_in_venv(cmd, output=None):
    if cmd[0] == "python":
        cmd[0] = sys.executable

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


def _run_in_venv_cmd(cmd_str):
    if os.name == "nt":
        act = os.path.join("venv", "Scripts", "activate.bat")
        full_cmd = f'call "{act}" && {cmd_str}'
    else:
        act = "./venv/bin/activate"
        full_cmd = f'. "{act}" && {cmd_str}'
    subprocess.run(full_cmd, shell=True, check=True)


def _has_module(mod):
    try:
        _run_in_venv(["python", "-c", f"import {mod}"])
        return True
    except subprocess.CalledProcessError:
        return False


def _has_tkinter():
    try:
        _run_in_venv_cmd('python -c "import tkinter"')
        return True
    except subprocess.CalledProcessError:
        return False


def _maybe_brew_install_tk():
    if shutil.which("brew") is None:
        print("Homebrew not found. Can't install tkinter via brew.")
        return
    _run(["brew", "install", "python-tk"])
    act = os.path.join("venv", "bin", "activate")
    with open(act, "a", encoding="utf-8") as f:
        f.write('\nexport PATH="/opt/homebrew/opt/tcl-tk/bin:$PATH"\n')
        f.write('export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"\n')
        f.write('export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"\n')
        f.write('export PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk/lib/pkgconfig"\n')
    _run_in_venv_cmd('python -c "import tkinter"')


if __name__ == "__main__":
    main()
