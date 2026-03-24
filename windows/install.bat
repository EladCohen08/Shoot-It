@echo off
echo =========================================
echo   Installing Shoot-It (Windows Edition)
echo =========================================
echo.
echo 1. Installing Python libraries...
pip install -r requirements.txt
echo.
echo 2. Adding Shoot-It to your System PATH...
set "SHOOT_DIR=%CD%"
powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';%SHOOT_DIR%', 'User')"
echo.
echo ✅ Setup Complete!
echo ⚠️ IMPORTANT: Close this terminal and open a NEW one for the changes to take effect.
echo.
echo Your new global commands:
echo   - shoot    (Sets the target folder AND starts listening)
echo   - unshoot  (Clears the target folder)
pause
