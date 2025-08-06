#!/bin/bash
# =========================================
# Runner for python3 File Collector (macOS)
# =========================================

cd "$(dirname "$0")/../logic"
python3 extract_codebase.py

echo
read -n 1 -s -r -p "✅ Done! Press any key to close..."
