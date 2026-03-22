import json
import os
from src.swarm.base_agent import BaseAgent
from src.reactor.models import Artifact
from typing import List

class RalphAgent(BaseAgent):
    """An agent that follows the Ralph Protocol (Plan -> Execute -> Verify -> Cycle)."""
    
    def __init__(self, agent_id: str, reactor, role: str):
        super().__init__(agent_id, reactor)
        self.role = role
        self.backlog_path = f"backlogs/{agent_id}_backlog.json"
        os.makedirs("backlogs", exist_ok=True)
        if not os.path.exists(self.backlog_path):
            self._save_backlog([])

    def _load_backlog(self) -> List[dict]:
        with open(self.backlog_path, "r") as f:
            return json.load(f)

    def _save_backlog(self, tasks: List[dict]):
        with open(self.backlog_path, "w") as f:
            json.dump(tasks, f, indent=2)

    def add_task(self, task_description: str, context: dict):
        backlog = self._load_backlog()
        backlog.append({
            "id": len(backlog) + 1,
            "description": task_description,
            "context": context,
            "status": "pending"
        })
        self._save_backlog(backlog)

    def run_cycle(self):
        """The Ralph Loop with Steering: Steer -> Read -> Plan -> Execute -> Verify."""
        # 1. Check for specific Steering Directives from the User
        steering = [n for n in self.reactor.get_open_needs() 
                    if n.need_type == "steering_directive" and 
                    (n.context.get("target_id") == self.agent_id or n.context.get("target_id") == "all")]
        
        if steering:
            directive = steering[0]
            print(f"[{self.agent_id}] !!! HUMAN STEERING INTERRUPT: {directive.description} !!!")
            self.add_task(f"STEER: {directive.description}", directive.context)
            self.reactor.resolve_need(directive.id, "STEER_ACKNOWLEDGED")

        backlog = self._load_backlog()
        current_task = next((t for t in backlog if t["status"] == "pending"), None)
        
        if not current_task:
            # Check for new broadcasted needs relevant to this role
            new_needs = self.get_relevant_needs()
            for need in new_needs:
                self.add_task(need.description, need.context)
            return

        print(f"[{self.agent_id} | {self.role}] Executing Task: {current_task['description']}")
        
        # Phase: Execute
        result = self.execute_task(current_task)
        
        # Phase: Verify (Simplified for now - can be LLM based)
        if result:
            current_task["status"] = "completed"
            self._save_backlog(backlog)
            print(f"[{self.agent_id}] Task {current_task['id']} completed and verified.")

    def get_relevant_needs(self):
        """Filter the global needs bus for items this role can handle."""
        all_needs = self.reactor.get_open_needs()
        # Subclasses should override this
        return []

    def execute_task(self, task):
        """Subclasses must implement specific execution logic."""
        raise NotImplementedError

class PhdStudentAgent(RalphAgent):
    def __init__(self, agent_id: str, reactor):
        super().__init__(agent_id, reactor, "PhD Student")

    def get_relevant_needs(self):
        return [n for n in self.reactor.get_open_needs() if n.need_type in ["literature_search", "deep_research"]]

    def execute_task(self, task):
        # Implementation logic for literature/search
        return True

class DataAnalystAgent(RalphAgent):
    def __init__(self, agent_id: str, reactor):
        super().__init__(agent_id, reactor, "Data Analyst")

    def get_relevant_needs(self):
        return [n for n in self.reactor.get_open_needs() if n.need_type == "data_synthesis"]

    def execute_task(self, task):
        # Implementation logic for analysis
        return True

class PostdocAgent(RalphAgent):
    def __init__(self, agent_id: str, reactor):
        super().__init__(agent_id, reactor, "Postdoc")

    def get_relevant_needs(self):
        # Postdocs review completed artifacts
        return [n for n in self.reactor.get_open_needs() if n.need_type == "quality_review"]

    def execute_task(self, task):
        # Implementation logic for review
        return True

class InternAgent(RalphAgent):
    def __init__(self, agent_id: str, reactor):
        super().__init__(agent_id, reactor, "Intern")

    def get_relevant_needs(self):
        # Interns handle basic formatting or triage
        return [n for n in self.reactor.get_open_needs() if n.need_type == "data_formatting"]

    def execute_task(self, task):
        # Lightweight execution
        print(f"[{self.agent_id}] Intern performing basic task: {task['description']}")
        return True

