import time
from src.swarm.base_agent import BaseAgent
from src.swarm.skills.literature import LiteratureSkill
from src.reactor.event_bus import ArtifactReactor

class LiteratureAgent(BaseAgent):
    """A swarm worker focused on fulfilling literature search needs."""

    def run_cycle(self):
        """Check for open literature needs and fulfill them."""
        needs = self.reactor.get_open_needs()
        for need in needs:
            if need.need_type == "literature_search":
                print(f"[Swarm] Fulfilling need: {need.description}")
                topic = need.context.get("topic")
                
                # Perform search
                results = LiteratureSkill.search_openalex(topic)
                if not results:
                    results = LiteratureSkill.search_arxiv(topic)
                
                # Publish findings
                artifact_id = self.publish(
                    topic=topic,
                    skill="literature_search",
                    data={"results": results}
                )
                
                # Mark need as resolved
                self.reactor.resolve_need(need.id, artifact_id)
                print(f"[Swarm] Resolved need {need.id} with artifact {artifact_id}")

if __name__ == "__main__":
    # Example standalone swarm runner
    reactor = ArtifactReactor()
    agent = LiteratureAgent(agent_id="Literature_Worker_1", reactor=reactor)
    while True:
        agent.run_cycle()
        time.sleep(10)
