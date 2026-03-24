@echo off
echo %CD%> "%USERPROFILE%\.shoot_it_dir"
echo 📸 Target set to: %CD%
echo 🚀 Starting background listener... 
echo Press Ctrl+Alt+S to capture. Close this window to stop.
python "%~dp0shoot_it.py"
