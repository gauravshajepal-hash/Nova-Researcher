import litellm
from typing import List, Optional
from src.swarm.base_agent import BaseAgent
from src.swarm.skills.literature import LiteratureSkill
from src.reactor.event_bus import ArtifactReactor

class PIOrchestrator(BaseAgent):
    """The High-Level PI directing research trajectory."""

    def __init__(self, agent_id: str, reactor: ArtifactReactor, model: str = "gpt-4o"):
        super().__init__(agent_id, reactor)
        self.model = model

    def seed_hypothesis(self, domain_a: str, domain_b: str, core_concept: str):
        """Kick off a cross-disciplinary investigation."""
        prompt = f"""
        Role: Senior Principal Scientist
        Goal: Formulate a novel cross-disciplinary hypothesis.
        Domain A: {domain_a}
        Domain B: {domain_b}
        Concept: Apply {core_concept} from {domain_a} to {domain_b}.
        
        Task: 
        1. Identify 3 specific sub-topics for literature search.
        2. Format response as: SEARCH_TOPIC: <topic>
        """
        
        try:
            from tenacity import retry, stop_after_attempt, wait_exponential
            
            @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
            def _call_llm():
                return litellm.completion(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
            
            response = _call_llm()
            content = response.choices[0].message.content
        except litellm.exceptions.AuthenticationError:
            print("[PI] AuthenticationError caught. Proceeding with Mock synthesis logic for testing.")
            content = f"SEARCH_TOPIC: {core_concept} in {domain_a}\nSEARCH_TOPIC: {core_concept} in {domain_b}\nSEARCH_TOPIC: Mathematical bridging for {core_concept}"
        except Exception as e:
            print(f"[PI] LLM error: {e}. Fallback to basic search.")
            content = f"SEARCH_TOPIC: {core_concept}\nSEARCH_TOPIC: {domain_a} and {domain_b}"
            
        for line in content.split("\n"):
            if "SEARCH_TOPIC:" in line:
                topic = line.split("SEARCH_TOPIC:")[1].strip()
                # Broadcast the need for literature
                self.ask(
                    need_type="literature_search",
                    description=f"Search for {topic} at intersection of {domain_a} and {domain_b}",
                    context={"topic": topic, "domains": [domain_a, domain_b]}
                )

    def run_cycle(self):
        """Observe the DAG and decide next steps."""
        artifacts = self.reactor.get_latest_artifacts(limit=50)
        # TODO: Implement complex reasoning to synthesize artifacts
        print(f"[PI] {len(artifacts)} artifacts visible. Monitoring swarm...")
