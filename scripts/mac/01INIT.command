#!/usr/bin/env bash
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

set -e
cd "$(dirname "$0")"

echo "Making all .command files in this folder executable..."

find . -maxdepth 1 -type f -name "*.command" -exec chmod +x {} \;

echo "All .command scripts are now executable."
read -p "Press [Enter] to close this window."
