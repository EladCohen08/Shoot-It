@echo off
echo =========================================
echo Installing Shoot-It
echo =========================================

:: Install dependencies
pip install -r requirements.txt

:: Add to User PATH
set "SHOOT_DIR=%~dp0"
if "%SHOOT_DIR:~-1%"=="\" set "SHOOT_DIR=%SHOOT_DIR:~0,-1%"

setx PATH "%PATH%;%SHOOT_DIR%"

echo.
echo [Success] Setup complete.
echo Restart your terminal and type 'shoot' to begin.
pause