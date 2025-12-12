@echo off
REM Windows build script for creating one-file exe using PyInstaller.
REM Usage: Open Developer Command Prompt or regular cmd with virtualenv activated, then run: build_windows_exe.bat

REM 1) Create and activate virtual environment (one-time):
REM python -m venv env
REM env\Scripts\activate

REM 2) Install requirements:
pip install -r requirements.txt
pip install pyinstaller

REM 3) Run PyInstaller to build one-file GUI executable:
REM Note: adjust --add-data syntax if using PowerShell vs cmd. This script uses cmd format.
pyinstaller --noconfirm --onefile --windowed --add-data "assets;assets" run.py

REM Output will be in the dist\ folder as run.exe
echo Build finished. Check the dist\ folder for run.exe
pause
