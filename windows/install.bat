@echo off
echo =========================================
echo Installing Shoot-It
echo =========================================
echo.

:: Detect Python automatically
set "PYTHON="
for %%P in (
    python
    python3
) do (
    where %%P >nul 2>nul
    if not errorlevel 1 set PYTHON=%%P
)

if "%PYTHON%"=="" (
    echo [Error] Python not found. Please install Python 3.10+ and add it to PATH.
    pause
    exit /b 1
)

:: Install dependencies
"%PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [Error] Pip failed.
    pause
    exit /b 1
)

:: Get current folder
set "SHOOT_DIR=%~dp0"
if "%SHOOT_DIR:~-1%"=="\" set "SHOOT_DIR=%SHOOT_DIR:~0,-1%"

:: Add Shoot-It to User PATH safely
powershell -Command "$p = [Environment]::GetEnvironmentVariable('Path','User'); if ($p -notlike '*%SHOOT_DIR%*') { [Environment]::SetEnvironmentVariable('Path', $p + ';%SHOOT_DIR%','User') }"

echo.
echo [Success] Setup complete.
echo IMPORTANT: Close this terminal and open a NEW one to use 'shoot'.
pause