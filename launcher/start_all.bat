@echo off
REM Batch file to start backend (FastAPI) and frontend (HTML) together

REM Start backend server in a new command window
title FastAPI Backend
start cmd /k "cd /d ..\backend && uvicorn main:app --reload --host 127.0.0.1 --port 8000"

REM Wait a few seconds for backend to start
ping 127.0.0.1 -n 4 > nul

REM Open frontend in default browser
start "" "..\frontend\index.html"

echo Backend and frontend started.
pause
