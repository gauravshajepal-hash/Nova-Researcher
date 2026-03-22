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
        """Kick off a cross-disciplinary investigation using Agentic Tree Search."""
        prompt = f"""
        Role: Senior Principal Scientist (AI Scientist v2 Paradigm)
        Goal: Formulate a novel cross-disciplinary hypothesis.
        Domain A: {domain_a}
        Domain B: {domain_b}
        Concept: Apply {core_concept} from {domain_a} to {domain_b}.
        
        Task:
        1. [Breadth] Generate 5 distinct, diverse hypotheses linking these domains.
        2. [Depth] Score them and select the highest plausibility hypothesis.
        3. [Red-Team] Attack your selected hypothesis to find flaws, then refine it.
        4. [Output] Break the final refined hypothesis into exactly 3 orthogonal sub-topics for a Swarm to research.
        Format your final specific output lines precisely as: DEEP_RESEARCH_TOPIC: <topic>
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
            print(f"[PI] Tree Search Ideation Complete.\n\n{content}\n")
        except litellm.exceptions.AuthenticationError:
            print("[PI] AuthenticationError caught. Proceeding with Mock Agentic Tree Search logic.")
            content = f"DEEP_RESEARCH_TOPIC: Epigenetic mapping of {core_concept} in {domain_a}\nDEEP_RESEARCH_TOPIC: {core_concept} longitudinal studies in {domain_b}\nDEEP_RESEARCH_TOPIC: Algorithmic convergence of {core_concept}"
        except Exception as e:
            print(f"[PI] LLM error: {e}. Fallback to basic search.")
            content = f"DEEP_RESEARCH_TOPIC: {core_concept}\nDEEP_RESEARCH_TOPIC: {domain_a} and {domain_b}"
            
        topics_found = 0
        for line in content.split("\n"):
            if "DEEP_RESEARCH_TOPIC:" in line:
                topic = line.split("DEEP_RESEARCH_TOPIC:")[1].strip()
                # Broadcast the need for deep research
                self.ask(
                    need_type="deep_research",
                    description=f"Deep dive investigation for: {topic}",
                    context={"topic": topic, "domains": [domain_a, domain_b]}
                )
                topics_found += 1
        print(f"[System] {topics_found} Deep Research requests broadcasted.")

    def run_cycle(self):
        """Observe the DAG and decide next steps."""
        artifacts = self.reactor.get_latest_artifacts(limit=50)
        # TODO: Implement complex reasoning to synthesize artifacts
        print(f"[PI] {len(artifacts)} artifacts visible. Monitoring swarm...")
