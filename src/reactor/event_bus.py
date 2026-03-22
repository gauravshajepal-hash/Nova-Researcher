import json
import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from filelock import FileLock
from .models import Artifact, UnmetNeed, ResearchState

class ArtifactReactor:
    """The central synchronization point for all research agents."""
    
    def __init__(self, storage_dir: str = "~/.nova_researcher"):
        self.storage_path = Path(os.path.expanduser(storage_dir))
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.index_file = self.storage_path / "global_index.jsonl"
        self.needs_file = self.storage_path / "unmet_needs.jsonl"
        
        self.index_lock = FileLock(str(self.index_file) + ".lock")
        self.needs_lock = FileLock(str(self.needs_file) + ".lock")
        
        # Ensure files exist
        self.index_file.touch(exist_ok=True)
        self.needs_file.touch(exist_ok=True)
        
        self.evermem_api = "http://localhost:1995/api/v1"

    def publish_artifact(self, artifact: Artifact):
        """Persistent write of an artifact to the global index safely."""
        with self.index_lock:
            with open(self.index_file, "a", encoding="utf-8") as f:
                f.write(artifact.model_dump_json() + "\n")
                
        # Shadow-copy to EverMemOS for infinite context retrieval
        try:
            import requests
            requests.post(f"{self.evermem_api}/memories", json={
                "message_id": artifact.id,
                "sender": artifact.agent_id,
                "content": str(artifact.data)
            }, timeout=2)
        except Exception:
            pass  # EverMemOS offline, gracefully continue with standard JSONL
            
        return artifact.id

    def broadcast_need(self, need: UnmetNeed):
        """Broadcast a need to the swarm safely."""
        with self.needs_lock:
            with open(self.needs_file, "a", encoding="utf-8") as f:
                f.write(need.model_dump_json() + "\n")
        return need.id

    def get_latest_artifacts(self, limit: int = 100) -> List[Artifact]:
        """Read the tail of the global index."""
        artifacts = []
        if not self.index_file.exists():
            return []
            
        with open(self.index_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                if line.strip():
                    artifacts.append(Artifact.model_validate_json(line))
        return artifacts

    def get_open_needs(self) -> List[UnmetNeed]:
        """Filter the needs file for unresolved requirements."""
        needs = []
        if not self.needs_file.exists():
            return []
            
        with open(self.needs_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    need = UnmetNeed.model_validate_json(line)
                    if not need.resolved_artifact_id:
                        needs.append(need)
        return needs

    def resolve_need(self, need_id: str, artifact_id: str):
        """Mark a need as resolved by a specific artifact."""
        with self.needs_lock:
            updated_needs = []
            with open(self.needs_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        need = UnmetNeed.model_validate_json(line)
                        if need.id == need_id:
                            need.resolved_artifact_id = artifact_id
                        updated_needs.append(need)
            
            with open(self.needs_file, "w", encoding="utf-8") as f:
                for need in updated_needs:
                    f.write(need.model_dump_json() + "\n")
