@echo off
REM (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

cd /d %~dp0
cd ..\..
if not exist venv\Scripts\activate.bat (
  echo No virtual environment found.
  pause > nul
  exit /b 1
)
call venv\Scripts\activate.bat
python scripts\logic\run_logic.py %*
echo Done.
pause > nul
call venv\Scripts\deactivate.bat
