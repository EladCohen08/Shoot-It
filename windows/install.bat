@echo off
echo =========================================
echo Installing Shoot-It
echo =========================================

:: Ensure pip runs on the correct Python
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [Error] Failed to install dependencies.
    pause
    exit /b 1
)

:: Get current directory and strip trailing backslash
set "SHOOT_DIR=%~dp0"
if "%SHOOT_DIR:~-1%"=="\" set "SHOOT_DIR=%SHOOT_DIR:~0,-1%"

powershell -Command "$p = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($p -notlike '*%SHOOT_DIR%*') { [Environment]::SetEnvironmentVariable('Path', $p + ';%SHOOT_DIR%', 'User') }"

echo.
echo [Success] Setup complete.
echo IMPORTANT: Close this terminal and open a NEW one, then type 'shoot'
pause