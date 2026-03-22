from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import os
import json
from src.reactor.models import Artifact, UnmetNeed
from typing import List

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Nova-Researcher Lab API")

# Mount UI
ui_path = Path(__file__).parent.parent.parent / "ui"
app.mount("/dashboard", StaticFiles(directory=ui_path), name="dashboard")

@app.get("/")
async def read_index():
    return FileResponse(ui_path / "index.html")


# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STORAGE_DIR = Path(os.path.expanduser("~/.nova_researcher"))
INDEX_FILE = STORAGE_DIR / "global_index.jsonl"
NEEDS_FILE = STORAGE_DIR / "unmet_needs.jsonl"

class SteeringRequest(BaseModel):
    directive: str
    target_agent: str = "PI"

@app.get("/artifacts")
async def get_artifacts(limit: int = 50):
    artifacts = []
    if not INDEX_FILE.exists():
        return []
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[-limit:]:
            if line.strip():
                artifacts.append(json.loads(line))
    return artifacts[::-1] # Newest first

@app.get("/needs")
async def get_needs():
    needs = []
    if not NEEDS_FILE.exists():
        return []
    with open(NEEDS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                need = json.loads(line)
                if not need.get("resolved_artifact_id"):
                    needs.append(need)
    return needs

@app.post("/steer")
async def post_steering(request: SteeringRequest):
    # In a real implementation, this would write to a 'directives.jsonl' 
    # that agents poll. For now, we'll append to unmet_needs with a special type.
    need = UnmetNeed(
        id=f"steer_{int(os.times()[4])}",
        parent_artifact_id="HITL",
        description=f"HUMAN STEERING: {request.directive}",
        need_type="steering_directive",
        target_role=request.target_agent
    )
    with open(NEEDS_FILE, "a", encoding="utf-8") as f:
        f.write(need.model_dump_json() + "\n")
    return {"status": "dispatched", "id": need.id}

@app.get("/status")
async def get_status():
    # Basic swarm health check
    return {
        "lab_name": "Nova-Researcher Alpha",
        "storage_path": str(STORAGE_DIR),
        "active": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
