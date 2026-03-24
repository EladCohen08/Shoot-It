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
powershell -NoProfile -Command "$p = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($p -notmatch [regex]::Escape('%SHOOT_DIR%')) { [Environment]::SetEnvironmentVariable('Path', $p + ';%SHOOT_DIR%', 'User'); Write-Host 'Added to PATH.' } else { Write-Host 'Already in PATH.' }"
echo.
echo Setup complete.
echo IMPORTANT: Close this terminal and open a NEW one for the changes to take effect.
echo.
echo Your new global commands:
echo   - shoot    (Sets the target folder AND starts listening)
echo   - unshoot  (Clears the target folder)
pause
