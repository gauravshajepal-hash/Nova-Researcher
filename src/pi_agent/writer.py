import litellm
from src.reactor.event_bus import ArtifactReactor

class PIWriter:
    """Synthesizes the Artifact DAG into an academic paper."""
    
    def __init__(self, reactor: ArtifactReactor, model: str = "gpt-4o"):
        self.reactor = reactor
        self.model = model

    def synthesize_paper(self, title: str) -> str:
        """Reads all completed artifacts and writes a coherent paper."""
        artifacts = self.reactor.get_latest_artifacts(limit=100)
        
        context = ""
        for art in artifacts:
            context += f"\n- [Agent {art.agent_id} | Skill {art.skill_used}]: {str(art.data)[:500]}..."
            
        prompt = f"""
        Role: Academic Editor
        Task: Write an outline and summary for a research paper exploring '{title}'.
        Base your synthesis strictly on the following Swarm findings:
        
        {context}
        """
        try:
            response = litellm.completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except litellm.exceptions.AuthenticationError:
            print("[PI Writer] AuthenticationError: using Mock Paper.")
            return f"# Paper: {title}\n\n## Abstract\nMock synthesis of swarm findings based on {len(artifacts)} experiments."
        except Exception as e:
            print(f"[PI Writer] Generation failed: {e}")
            return "Paper generation failed."
