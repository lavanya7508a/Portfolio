@echo off
title Smart Dustbin Monitoring System - Goundanur Pilot
echo =========================================================================
echo  Smart Dustbin - AI-Enabled Fill-Level Monitoring System
echo  Field Study Pilot: Goundanur, Coimbatore
echo  Presenter: Lavanya A (25105116 - CSE)
echo =========================================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    if exist "C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe" (
        set "PYTHON_EXE=C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe"
    ) else (
        echo [ERROR] Python not found in PATH or standard location.
        pause
        exit /b 1
    )
) else (
    set "PYTHON_EXE=python"
)

echo [*] Using Python: %PYTHON_EXE%
echo [*] Starting Flask Server on http://127.0.0.1:5000...
echo [*] Press Ctrl+C in this terminal to stop the server.
echo.

start "" http://127.0.0.1:5000
"%PYTHON_EXE%" app.py

pause
