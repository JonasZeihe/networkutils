#!/usr/bin/env bash
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

set -e
cd "$(dirname "$0")"
cd ../../

if [ ! -d "venv" ]; then
  echo "No virtual environment found. Nothing to deactivate."
  read -p "Press [Enter] to close this window."
  exit 0
fi

echo "Attempting to deactivate the virtual environment..."
if [[ -n "$VIRTUAL_ENV" ]]; then
  deactivate
  echo "Virtual environment deactivated successfully."
else
  echo "No active virtual environment found."
fi

read -p "Press [Enter] to close this window."
