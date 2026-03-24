@echo off
echo =========================================
echo   Installing Shoot-It (Windows Edition)
echo =========================================
echo.
echo 1. Installing Python libraries...
pip install -r requirements.txt
echo.
echo 2. Adding Shoot-It to your System PATH...
set "SHOOT_DIR=%~dp0"
if "%SHOOT_DIR:~-1%"=="\" set "SHOOT_DIR=%SHOOT_DIR:~0,-1%"
powershell -NoProfile -Command "$shootDir = '%SHOOT_DIR%'; $pathValue = [Environment]::GetEnvironmentVariable('Path', 'User'); $parts = @(); if ($pathValue) { $parts = $pathValue -split ';' | Where-Object { $_ }; } if ($parts -notcontains $shootDir) { $updatedPath = if ($parts.Count -gt 0) { ($parts + $shootDir) -join ';' } else { $shootDir }; [Environment]::SetEnvironmentVariable('Path', $updatedPath, 'User'); Write-Host ('Added to PATH: ' + $shootDir); } else { Write-Host ('Already in PATH: ' + $shootDir); }"
echo.
echo Setup complete.
echo IMPORTANT: The PATH update applies only to NEW terminal windows.
echo Close this terminal and open a NEW one before running shoot or unshoot.
echo.
echo Your new global commands:
echo   - shoot    (Sets the target folder AND starts listening)
echo   - unshoot  (Clears the target folder)
pause
