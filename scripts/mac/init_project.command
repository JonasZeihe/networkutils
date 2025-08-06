#!/usr/bin/env bash
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

set -e
cd "$(dirname "$0")"
cd ../../

python3 scripts/logic/init_project.py

echo "Initialization complete."
read -p "Press [Enter] to close this window."
