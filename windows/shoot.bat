@echo off
powershell -NoProfile -Command "[System.IO.File]::WriteAllText([System.IO.Path]::Combine($env:USERPROFILE, '.shoot_it_dir'), (Get-Location).Path, [System.Text.UTF8Encoding]::new($false))"
if errorlevel 1 (
    echo Failed to save the target folder.
    exit /b 1
)
echo Target set to: %CD%
echo Starting background listener...
echo Press Ctrl+Alt+S to capture. Close this window to stop.
python "%~dp0shoot_it.py"
