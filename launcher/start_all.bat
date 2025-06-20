@echo off
REM Batch file to set up Python venv, install requirements, start backend and frontend

REM Set variables
set VENV_DIR=..\backend\venv
set REQUIREMENTS=..\backend\requirements.txt
set PYTHON=python

REM Create virtual environment if it doesn't exist
if not exist %VENV_DIR% (
    echo Creating virtual environment...
    %PYTHON% -m venv %VENV_DIR%
)

REM Activate virtual environment
call %VENV_DIR%\Scripts\activate.bat

REM Install requirements
if exist %REQUIREMENTS% (
    echo Installing requirements...
    pip install -r %REQUIREMENTS%
) else (
    echo requirements.txt not found!
)

REM Start backend server in a new command window
title FastAPI Backend
start cmd /k "cd /d ..\backend && call venv\Scripts\activate.bat && uvicorn main:app --reload --host 127.0.0.1 --port 8000"

REM Wait a few seconds for backend to start
ping 127.0.0.1 -n 4 > nul

REM Start a simple HTTP server for the frontend in a new window
title Frontend Server
start cmd /k "cd /d ..\frontend && %PYTHON% -m http.server 8080"

REM Wait a second for the frontend server to start
ping 127.0.0.1 -n 2 > nul

REM Open frontend in default browser using localhost
start "" "http://localhost:8080"

echo Backend and frontend started.
pause
