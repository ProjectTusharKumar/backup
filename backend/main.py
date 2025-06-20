from fastapi import FastAPI, Response, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
# import shutil
# from datetime import datetime
import subprocess
import json

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BACKUP_FOLDER = os.path.join(os.path.dirname(__file__), "backups")
SERVICE_STATUS = {"running": False}
BAT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "bat_config.json")

# API: Check if the backup service is running
@app.get("/status")
def check_status():
    """Return the running status of the backup service."""
    return {"running": SERVICE_STATUS["running"]}

# API: Set the backup service as running (not used in new flow)
@app.post("/start")
def start_service():
    """Set the backup service status to running (legacy/manual use)."""
    SERVICE_STATUS["running"] = True
    return {"status": "started"}

# API: Run a .bat file as admin (Windows only)
@app.post("/run_bat")
async def run_bat(request: Request):
    """Run a specified .bat file as admin (Windows only) based on the name provided in the request body."""
    data = await request.json()
    name = data.get("name")
    if not name:
        return JSONResponse({"error": "No bat name provided"}, status_code=400)
    # Load bat config
    if not os.path.exists(BAT_CONFIG_PATH):
        return JSONResponse({"error": "bat_config.json not found"}, status_code=500)
    with open(BAT_CONFIG_PATH) as f:
        bat_map = json.load(f)
    bat_file = bat_map.get(name)
    if not bat_file:
        return JSONResponse({"error": "Unknown bat name"}, status_code=400)
    bat_path = os.path.join(os.path.dirname(__file__), bat_file)
    if not os.path.exists(bat_path):
        return JSONResponse({"error": f"Bat file {bat_file} not found"}, status_code=404)
    try:
        # Run as admin (Windows only)
        if os.name == 'nt':
            subprocess.Popen(["runas", "/user:Administrator", bat_path], shell=True)
        # If the .bat is to start the server, update status
        if name == "start_server":
            SERVICE_STATUS["running"] = True
        return {"status": f"{bat_file} started"}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

