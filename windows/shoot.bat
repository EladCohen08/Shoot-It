@echo off
:: Force UTF-8 for Hebrew support
chcp 65001 > nul
echo %CD%> "%USERPROFILE%\.shoot_it_dir"
echo 📸 Target set to: %CD%
echo 🚀 Starting background listener... 
echo Press Ctrl+Alt+S to capture. Close this window to stop.
python "%~dp0shoot_it.py"
