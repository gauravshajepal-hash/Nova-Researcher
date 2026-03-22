import os
from dotenv import load_dotenv
load_dotenv()

from src.pi_agent.orchestrator import PIOrchestrator
from src.reactor.event_bus import ArtifactReactor
from src.swarm.skills.literature import LiteratureSkill

def main():
    # Setup
    reactor = ArtifactReactor()
    pi = PIOrchestrator(agent_id="Principal_Investigator", reactor=reactor, model="gemini/gemini-1.5-pro")
    
    print("--- Nova Researcher: Autonomous Cross-Discipline Discovery ---")
    prompt = input("\nResearch Question/Topic: ")
    
    if not prompt:
        prompt = "How can we apply active matter physics to population science models of disease spread?"
        
    print(f"\n[PI] Commencing research on: '{prompt}'...")
    pi.seed_hypothesis(prompt)
    
    print("\n[System] Lab Initialized. To steer agents, use 'start_lab.py'")

if __name__ == "__main__":
    main()
