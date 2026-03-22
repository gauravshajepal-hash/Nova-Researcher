import json
import os
import litellm
from typing import List, Optional
from src.swarm.base_agent import BaseAgent
from src.reactor.event_bus import ArtifactReactor
from src.reactor.models import Artifact

class PIOrchestrator(BaseAgent):
    """The High-Level PI directing research trajectory with Ralph & Lab Meetings."""

    def __init__(self, agent_id: str, reactor: ArtifactReactor, model: str = "gpt-4o"):
        super().__init__(agent_id, reactor)
        self.model = model
        self.plan_path = "research_plan.json"
        
    def _load_plan(self):
        if os.path.exists(self.plan_path):
            with open(self.plan_path, "r") as f:
                return json.load(f)
        if next_step:
            print(f"[PI] Dispatching Step {next_step['step']}: {next_step['task']}")
            self.ask(
                need_type=next_step["type"],
                description=next_step["task"],
                context={"topic": next_step["task"], "step": next_step["step"]}
            )
            next_step["status"] = "in_progress"
            self._save_plan(plan)

        # Lab Meeting Sync
        artifacts = self.reactor.get_latest_artifacts(limit=20)
        completed_tasks = [a for a in artifacts if a.topic.startswith("Deep Research")] # Simplified trigger
        
        if len(completed_tasks) >= 2:
            print(f"\n[PI] --- LAB MEETING IN SESSION ---")
            print(f"[PI] Reviewing {len(completed_tasks)} new reports from the swarm...")
            # Here PI would use LLM to synthesize meeting notes
            print(f"[PI] Learnings shared. Iterating on next research phase.")
            # Mark steps as complete in plan based on artifacts
            for step in plan:
                if step["status"] == "in_progress":
                    step["status"] = "completed"
            self._save_plan(plan)
            print("[PI] --- MEETING ADJOURNED ---\n")
