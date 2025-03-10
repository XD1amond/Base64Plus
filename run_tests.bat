@echo off
REM Simple wrapper script for run_tests.py

python run_tests.py %*

if errorlevel 1 (
    echo Tests failed with errors.
    pause
    exit /b 1
) else (
    echo All tests completed successfully.
    pause
)