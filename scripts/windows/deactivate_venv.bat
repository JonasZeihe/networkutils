@echo off
REM (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

cd /d %~dp0
cd ..\..
if not exist venv (
  echo No virtual environment found. Nothing to deactivate.
  pause > nul
  exit /b 0
)

echo Attempting to deactivate the virtual environment...
call venv\Scripts\deactivate.bat 2>nul || echo No active virtual environment found.

pause > nul
