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
    domain_a = input("Domain A (e.g., Physics): ") or "Physics"
    domain_b = input("Domain B (e.g., Population Science): ") or "Population Science"
    concept = input("Core Concept (e.g., Active Matter): ") or "Active Matter"
    
    print(f"\n[PI] Commencing study: {concept} in {domain_b} context...")
    pi.seed_hypothesis(domain_a, domain_b, concept)
    
    # Simple Heartbeat for Demo
    pi.run_cycle()
    
    print("\n[System] Seeds broadcast to 'unmet_needs.jsonl'.")
    print("[System] Start swarm workers to fulfill these needs.")

if __name__ == "__main__":
    main()
