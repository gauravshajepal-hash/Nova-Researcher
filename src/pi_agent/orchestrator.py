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
        return []

    def _save_plan(self, plan):
        with open(self.plan_path, "w") as f:
            json.dump(plan, f, indent=2)

    def seed_hypothesis(self, prompt: str):
        """Initial Ralph Planning: Create the research_plan.json based on conversational prompt."""
        print(f"[PI] Decomposing complex prompt into research plan...")
        plan = [
            {"step": 1, "task": f"Analyze core premise: {prompt[:50]}...", "status": "pending", "type": "deep_research"},
            {"step": 2, "task": "Identify 3 specific cross-disciplinary bottlenecks", "status": "pending", "type": "deep_research"},
            {"step": 3, "task": "Synthesize a draft model", "status": "pending", "type": "data_synthesis"}
        ]
        self._save_plan(plan)
        print(f"[PI] Research Plan generated with {len(plan)} steps.")

    def handle_steering(self, directive: str):
        """Inject a human course-correction into the active plan."""
        print(f"[PI] Human Steering Received: '{directive}'")
        plan = self._load_plan()
        plan.insert(0, {
            "step": 0, 
            "task": f"STEER: {directive}", 
            "status": "pending", 
            "type": "deep_research" 
        })
        self._save_plan(plan)

    def run_cycle(self):
        """Standard Ralph Loop + Lab Meeting Logic."""
        plan = self._load_plan()
        next_step = next((s for s in plan if s["status"] == "pending"), None)
        
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
        self.conduct_lab_meeting() # Call the new method
        artifacts = self.reactor.get_latest_artifacts(limit=20)
        # Check if we have progress to report
        if artifacts:
            print(f"[PI] Reviewing {len(artifacts)} artifacts. Monitoring Lab Culture...")
            # Automatically progress steps for the demo
            for step in plan:
                if step["status"] == "in_progress":
                    step["status"] = "completed"
            self._save_plan(plan)
