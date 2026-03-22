import litellm
from src.reactor.event_bus import ArtifactReactor

class PIWriter:
    """Synthesizes the Artifact DAG into an academic paper."""
    
    def __init__(self, reactor: ArtifactReactor, model: str = "gpt-4o"):
        self.reactor = reactor
        self.model = model

    def synthesize_paper(self, title: str) -> str:
        """Reads artifacts (via OS or local) and writes a coherent paper."""
        context = ""
        
        # Infinite Context Branch: Attempt EverMemOS retrieval
        try:
            import requests
            response = requests.get(
                "http://localhost:1995/api/v1/memories/search",
                json={
                    "query": f"Research regarding {title}",
                    "user_id": "Principal_Investigator",
                    "retrieve_method": "hybrid"
                },
                timeout=3
            )
            if response.status_code == 200:
                memories = response.json().get("result", {}).get("memories", [])
                for mem in memories:
                    context += f"\n- [EverMem Context]: {mem}"
                print("[PI Writer] Successfully loaded context via Infinite Memory (EverMemOS).")
        except Exception:
            pass
            
        # Fallback to Local DAG if EverMemOS is offline or unpopulated
        if not context.strip():
            artifacts = self.reactor.get_latest_artifacts(limit=100)
            for art in artifacts:
                context += f"\n- [Agent {art.agent_id} | Skill {art.skill_used}]: {str(art.data)[:500]}..."
            print("[PI Writer] Using standard DAG context extraction.")
            
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
