#!/usr/bin/env bash
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

set -e
cd "$(dirname "$0")"
cd ../../

if [ ! -f "venv/bin/activate" ]; then
  echo "No virtual environment found."
  read -p "Press [Enter] to close this window."
  exit 1
fi

source venv/bin/activate
python3 scripts/logic/run_logic.py "$@"
echo "Done."
deactivate

read -p "Press [Enter] to close this window."
