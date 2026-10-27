@echo off
title Blu Visual Teacher - Local Video Engine
color 0B

echo ======================================================================
echo                BLU VISUAL TEACHER - LOCAL OFFLINE ENGINE
echo ======================================================================
echo.
echo [1/3] Checking Python runtime...
python --version
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo.
echo [2/3] Checking environment dependencies...
python -m pip install -r requirements.txt --quiet

echo.
echo [3/3] Launching Blu Visual Teacher Server...
echo ----------------------------------------------------------------------
echo  App URL:    http://127.0.0.1:5000
echo  Mode:       Local-first / Offline-ready
echo  Resolution: 720p (1280x720 H.264 / AAC)
echo ----------------------------------------------------------------------
echo.

start http://127.0.0.1:5000
python backend\server.py

pause
