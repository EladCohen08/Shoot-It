@echo off
:: Save current directory to state file
echo %CD% > "%USERPROFILE%\.shoot-it-dir"

if errorlevel 1 (
    echo [Error] Failed to save target folder.
    exit /b 1
)

echo [Shoot-It] Target folder: %CD%
echo [Shoot-It] Starting listener...

:: Run python listener
python "%~dp0shoot_it.py"