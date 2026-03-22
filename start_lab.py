import time
import subprocess
import sys
import os
from src.reactor.event_bus import ArtifactReactor
from src.pi_agent.orchestrator import PIOrchestrator

def start_lab():
    print("--- Nova Researcher Lab: Initializing Swarm ---")
    reactor = ArtifactReactor()
    
    # 1. Initialize PI
    pi = PIOrchestrator(agent_id="Lab_PI", reactor=reactor)
    pi.seed_hypothesis("Physics", "Population Science", "Active Matter")
    
    # 2. Define the Team
    team = [
        {"id": "Postdoc_Alpha", "role": "Postdoc"},
        {"id": "PhD_Student_1", "role": "PhD_Student"},
        {"id": "PhD_Student_2", "role": "PhD_Student"},
        {"id": "Data_Analyst_1", "role": "Data_Analyst"}
    ]
    
    print(f"[Lab Manager] Spawning {len(team)} staff members...")
    
    # In a real environment, these would be separate processes.
    # For this demo, we'll create a simple launch script for the workers.
    
    # 3. Main Lab Loop
    try:
        iteration = 0
        while iteration < 5:
            iteration += 1
            print(f"\n--- Lab Day {iteration} ---")
            
            # PI Cycle
            pi.run_cycle()
            
            # Simulate Worker Cycles (In real usage, these run independently)
            # We will use a subprocess call to a worker runner for the demo
            worker_cmd = f"{sys.executable} -m src.swarm.literature_worker"
            # (Just run 1 worker for the demo visibility)
            subprocess.run(worker_cmd, shell=True, timeout=15)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n[Lab Manager] Lab shutting down safely.")

if __name__ == "__main__":
    start_lab()
