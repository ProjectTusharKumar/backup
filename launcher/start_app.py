import subprocess
import webbrowser
import time
import os

# Path to backend and frontend
BACKEND_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend'))
FRONTEND_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/index.html'))

# Start FastAPI server in background
backend_proc = subprocess.Popen([
    'uvicorn', 'main:app', '--reload', '--host', '127.0.0.1', '--port', '8000'
], cwd=BACKEND_PATH)

# Wait a few seconds for the server to start
print('Starting backend server...')
time.sleep(3)

# Open frontend in default browser
print('Opening frontend...')
webbrowser.open(f'file://{FRONTEND_PATH}')

# Wait for backend process to finish (optional, keeps script running)
try:
    backend_proc.wait()
except KeyboardInterrupt:
    print('Shutting down backend server...')
    backend_proc.terminate()
