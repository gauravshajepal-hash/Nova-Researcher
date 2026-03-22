import time
import os
from src.swarm.base_agent import BaseAgent
from src.reactor.event_bus import ArtifactReactor
from src.swarm.skills.literature import LiteratureSkill
from src.swarm.skills.deep_research import DeepResearchSkill
from src.reactor.models import Artifact

class LiteratureAgent(BaseAgent):
    """A swarm worker focused on fulfilling literature search needs."""

    def __init__(self, agent_id: str, reactor: ArtifactReactor):
        super().__init__(agent_id, reactor)
        self.lit_skill = LiteratureSkill()
        self.deep_skill = DeepResearchSkill()

    def run_cycle(self):
        """Single execution cycle for swarm processing."""
        needs = self.reactor.get_open_needs()
        
        for need in needs:
            try:
                if need.need_type not in ["literature_search", "deep_research"]:
                    continue
                    
                print(f"[Swarm] Fulfilling need: {need.description}")
                topic = need.context.get("topic", "Deep Research Topic")
                
                # Dynamic Skill Routing
                if need.need_type == "deep_research":
                    findings = self.deep_skill.execute(need.context)
                    skill_used = "DeepResearchSkill"
                else: # literature_search
                    findings = self.lit_skill.execute(topic)
                    skill_used = "LiteratureSkill"
                
                # Publish findings
                artifact_id = self.publish(
                    topic=topic,
                    skill=skill_used,
                    data={"findings": findings}
                )
                
                # Mark need as resolved
                self.reactor.resolve_need(need.id, artifact_id)
                print(f"[Swarm] Resolved need {need.id} with artifact {artifact_id}\n")
            except Exception as e:
                print(f"[Swarm] Error processing need {getattr(need, 'id', 'Unknown')}: {e}")

if __name__ == "__main__":
    # Example standalone swarm runner
    reactor = ArtifactReactor()
    agent = LiteratureAgent(agent_id="Literature_Worker_1", reactor=reactor)
    print(f"[Swarm Worker] Active and listening on Event Bus...")
    while True:
        agent.run_cycle()
        time.sleep(5)
