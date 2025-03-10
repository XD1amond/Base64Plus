@echo off
REM Simple wrapper script for install.py

python install.py %*

if errorlevel 1 (
    echo Installation failed with errors.
    pause
    exit /b 1
) else (
    echo Installation completed successfully.
    pause
)